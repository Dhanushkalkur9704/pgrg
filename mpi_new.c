#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <string.h>

void pigeonhole_sort(int local_arr[], int local_n, int min_val, int range_size, int* sorted_arr) {
    int* local_pigeonholes = (int*)calloc(range_size, sizeof(int));
    if (!local_pigeonholes) {
        fprintf(stderr, "Allocation error in pigeonhole_sort\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    for (int i = 0; i < local_n; i++) {
        local_pigeonholes[local_arr[i] - min_val]++;
    }

    int index = 0;
    for (int i = 0; i < range_size; i++) {
        while (local_pigeonholes[i] > 0) {
            sorted_arr[index++] = i + min_val;
            local_pigeonholes[i]--;
        }	
    }

    free(local_pigeonholes);
}

void merge(int arr1[], int arr2[], int size1, int size2, int merged_arr[]) {
    int i = 0, j = 0, k = 0;
    int *temp = (int*)malloc((size1 + size2) * sizeof(int));
    while (i < size1 && j < size2) {
        if (arr1[i] < arr2[j]) {
            temp[k++] = arr1[i++];
        } else {
            temp[k++] = arr2[j++];
        }
    }
    while (i < size1) {
        temp[k++] = arr1[i++];
    }
    while (j < size2) {
        temp[k++] = arr2[j++];
    }
    memcpy(merged_arr, temp, (size1 + size2) * sizeof(int));
    free(temp);
}

int main(int argc, char** argv) {
    double load_start_time, load_end_time;
    double sort_start_time, sort_end_time;
    MPI_Init(&argc, &argv);

    int world_rank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int n = 0;
    int* arr = NULL;
    const char* filename = (argc > 1) ? argv[1] : "T10I4D100K.dat.txt";

    if (world_rank == 0) {
        load_start_time = MPI_Wtime();
        int capacity = 100000;
        arr = (int*)malloc(capacity * sizeof(int));

        FILE* file = fopen(filename, "r");
        if (file == NULL) {
            file = fopen("../T10I4D100K.dat.txt", "r");
            if (file == NULL) {
                fprintf(stderr, "Could not open file '%s' for reading.\n", filename);
                free(arr);
                MPI_Finalize();
                return 1;
            }
        }

        int count = 0;
        while (fscanf(file, "%d", &arr[count]) != EOF) {
            count++;
            if (count >= capacity) {
                capacity *= 2;
                arr = (int*)realloc(arr, capacity * sizeof(int));
            }
        }

        fclose(file);
        n = count;
        load_end_time = MPI_Wtime();
        printf("Numbers read: %d\n", n);
        printf("Data loading time: %f seconds\n", load_end_time - load_start_time);
    }

    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Barrier(MPI_COMM_WORLD);
    sort_start_time = MPI_Wtime();

    int local_n = n / world_size;
    int *local_arr = (int*)malloc(local_n * sizeof(int));

    // Scatter data to all processes
    MPI_Scatter(arr, local_n, MPI_INT, local_arr, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    // Perform pigeonhole sort in parallel
    int range_size = 1000;
    int min_val = 0;
    int *sorted_arr = (int*)malloc(local_n * sizeof(int));
    pigeonhole_sort(local_arr, local_n, min_val, range_size, sorted_arr);

    // Gather the sorted subarrays
    int* sorted_data = NULL;
    if (world_rank == 0) {
        sorted_data = (int*)malloc(n * sizeof(int));
    }

    MPI_Gather(sorted_arr, local_n, MPI_INT, sorted_data, local_n, MPI_INT, 0, MPI_COMM_WORLD);
    sort_end_time = MPI_Wtime();

    // Merge the sorted subarrays
    if (world_rank == 0) {
        int* final_sorted_arr = (int*)malloc(n * sizeof(int));
        int current_merged_size = 0;

        for (int i = 0; i < world_size; i++) {
            int sub_size = (i == world_size - 1) ? (n - i * local_n) : local_n;
            if (i == 0) {
                memcpy(final_sorted_arr, sorted_data, sub_size * sizeof(int));
                current_merged_size = sub_size;
            } else {
                merge(final_sorted_arr, sorted_data + i * local_n, current_merged_size, sub_size, final_sorted_arr);
                current_merged_size += sub_size;
            }
        }

        printf("Sorting function execution time: %f seconds\n", sort_end_time - sort_start_time);

        int is_sorted = 1;
        for (int i = 1; i < n; i++) {
            if (final_sorted_arr[i] < final_sorted_arr[i - 1]) {
                is_sorted = 0;
                break;
            }
        }
        printf("Verification: %s\n", is_sorted ? "PASSED" : "FAILED");

        free(final_sorted_arr);
        free(sorted_data);
        free(arr);
    }

    free(local_arr);
    free(sorted_arr);
    MPI_Finalize();
    return 0;
}
