#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <string.h>

/**
 * Enhanced MPI Distributed Pigeonhole Sort (Zero-Merge Range-Partitioned Architecture)
 * 
 * Major Enhancements over Baseline:
 * 1. Range-based Partitioning: Each MPI process is assigned a unique value range [proc_min, proc_max].
 * 2. ZERO-MERGE Architecture: Eliminates the sequential O(n*p) merge on Rank 0 entirely.
 *    Concatenating the sorted outputs from Rank 0, 1, ..., p-1 is automatically globally sorted!
 * 3. Dynamic Global Min/Max calculation via MPI_Bcast / MPI_Allreduce.
 * 4. Safe dynamic memory buffers preventing buffer overwrite race conditions.
 */

void local_pigeonhole_sort(const int* local_arr, int local_n, int proc_min, int proc_range, int* sorted_arr) {
    if (local_n == 0 || proc_range <= 0) return;

    int *pigeonholes = (int *)calloc(proc_range, sizeof(int));
    if (!pigeonholes) {
        fprintf(stderr, "Allocation failure in local sort\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    for (int i = 0; i < local_n; i++) {
        pigeonholes[local_arr[i] - proc_min]++;
    }

    int idx = 0;
    for (int r = 0; r < proc_range; r++) {
        while (pigeonholes[r] > 0) {
            sorted_arr[idx++] = r + proc_min;
            pigeonholes[r]--;
        }
    }

    free(pigeonholes);
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int world_rank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int n = 0;
    int *raw_data = NULL;
    int global_min = 0, global_max = 0;
    double t_start = 0.0, t_end = 0.0;

    // Rank 0: Read dataset
    if (world_rank == 0) {
        printf("=============================================================\n");
        printf("  Enhanced MPI Pigeonhole Sort (Zero-Merge Architecture)\n");
        printf("=============================================================\n");
        printf("Total Active MPI Processes: %d\n", world_size);

        const char* filename = (argc > 1) ? argv[1] : "T10I4D100K.dat.txt";
        FILE *file = fopen(filename, "r");
        if (!file) {
            file = fopen("../T10I4D100K.dat.txt", "r");
            if (!file) {
                fprintf(stderr, "Cannot open dataset '%s'\n", filename);
                MPI_Abort(MPI_COMM_WORLD, 1);
            }
        }

        int capacity = 100000;
        raw_data = (int *)malloc(capacity * sizeof(int));
        int count = 0;
        while (fscanf(file, "%d", &raw_data[count]) != EOF) {
            count++;
            if (count >= capacity) {
                capacity *= 2;
                raw_data = (int *)realloc(raw_data, capacity * sizeof(int));
            }
        }
        fclose(file);
        n = count;
        printf("-> Read %d integers from dataset\n", n);

        global_min = raw_data[0];
        global_max = raw_data[0];
        for (int i = 1; i < n; i++) {
            if (raw_data[i] < global_min) global_min = raw_data[i];
            if (raw_data[i] > global_max) global_max = raw_data[i];
        }
        printf("-> Global Range: [%d, %d] (Size: %d)\n", global_min, global_max, global_max - global_min + 1);
    }

    MPI_Barrier(MPI_COMM_WORLD);
    t_start = MPI_Wtime();

    // Broadcast total count and global bounds
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&global_min, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&global_max, 1, MPI_INT, 0, MPI_COMM_WORLD);

    int total_range = global_max - global_min + 1;
    int range_per_rank = (total_range + world_size - 1) / world_size;

    // Calculate this rank's assigned range slice
    int my_min = global_min + world_rank * range_per_rank;
    int my_max = my_min + range_per_rank - 1;
    if (my_max > global_max) my_max = global_max;
    int my_range = (my_min <= my_max) ? (my_max - my_min + 1) : 0;

    // Rank 0 buckets raw data based on value ranges
    int *send_counts = NULL;
    int *displs = NULL;
    int *bucketed_data = NULL;
    int local_n = 0;

    if (world_rank == 0) {
        send_counts = (int *)calloc(world_size, sizeof(int));
        displs = (int *)calloc(world_size, sizeof(int));

        // Count items destined for each rank based on their value range
        for (int i = 0; i < n; i++) {
            int val = raw_data[i];
            int dest = (val - global_min) / range_per_rank;
            if (dest >= world_size) dest = world_size - 1;
            send_counts[dest]++;
        }

        displs[0] = 0;
        for (int p = 1; p < world_size; p++) {
            displs[p] = displs[p - 1] + send_counts[p - 1];
        }

        bucketed_data = (int *)malloc(n * sizeof(int));
        int *current_offset = (int *)malloc(world_size * sizeof(int));
        memcpy(current_offset, displs, world_size * sizeof(int));

        for (int i = 0; i < n; i++) {
            int val = raw_data[i];
            int dest = (val - global_min) / range_per_rank;
            if (dest >= world_size) dest = world_size - 1;
            bucketed_data[current_offset[dest]++] = val;
        }
        free(current_offset);
    }

    // Distribute local counts to each process
    MPI_Scatter(send_counts, 1, MPI_INT, &local_n, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Distribute value-partitioned data
    int *local_arr = (int *)malloc(local_n * sizeof(int));
    MPI_Scatterv(bucketed_data, send_counts, displs, MPI_INT,
                 local_arr, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    // Each rank performs local Pigeonhole Sort on its assigned range
    int *local_sorted = (int *)malloc(local_n * sizeof(int));
    local_pigeonhole_sort(local_arr, local_n, my_min, my_range, local_sorted);

    // Gather locally sorted subarrays back to Rank 0
    int *recv_counts = NULL;
    int *recv_displs = NULL;
    int *final_sorted = NULL;

    if (world_rank == 0) {
        recv_counts = send_counts;
        recv_displs = displs;
        final_sorted = (int *)malloc(n * sizeof(int));
    }

    // Direct Gather - NO MERGING STEP REQUIRED!
    MPI_Gatherv(local_sorted, local_n, MPI_INT,
                final_sorted, recv_counts, recv_displs, MPI_INT,
                0, MPI_COMM_WORLD);

    MPI_Barrier(MPI_COMM_WORLD);
    t_end = MPI_Wtime();

    // Rank 0 verifies results and reports timing
    if (world_rank == 0) {
        double total_ms = (t_end - t_start) * 1000.0;
        printf("-> Zero-Merge MPI Sorting Time: %.5f ms\n", total_ms);

        int is_sorted = 1;
        for (int i = 1; i < n; i++) {
            if (final_sorted[i] < final_sorted[i - 1]) {
                is_sorted = 0;
                break;
            }
        }
        printf("-> Verification: %s\n", is_sorted ? "PASSED (Array is correctly sorted globally)" : "FAILED");
        printf("=============================================================\n");

        free(raw_data);
        free(bucketed_data);
        free(displs);
        free(send_counts);
        free(final_sorted);
    }

    free(local_arr);
    free(local_sorted);
    MPI_Finalize();
    return 0;
}
