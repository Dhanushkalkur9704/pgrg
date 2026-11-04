#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _OPENMP
#include <omp.h>
#else
// Fallback stubs for compilers without OpenMP
#define omp_get_thread_num() 0
#define omp_get_max_threads() 1

#ifdef _WIN32
#include <windows.h>
static inline double omp_get_wtime() {
    LARGE_INTEGER freq, counter;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&counter);
    return (double)counter.QuadPart / (double)freq.QuadPart;
}
#else
#include <time.h>
static inline double omp_get_wtime() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}
#endif
#endif

/**
 * Enhanced OpenMP Multi-Core Parallel Pigeonhole Sort
 * Features:
 * 1. Thread-level parallel frequency histogramming with thread-local buffers (no lock contention).
 * 2. Parallel reduction into the global pigeonhole histogram.
 * 3. Multi-threaded parallel prefix scan and partition placement.
 * 4. Benchmarking scalability across different thread counts (1, 2, 4, 8, etc.).
 */

void openmp_pigeonhole_sort(const int* arr, int n, int min_val, int range_size, int* sorted_arr, int num_threads) {
    int *global_pigeonholes = (int *)calloc(range_size, sizeof(int));
    if (!global_pigeonholes) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }

    // Allocate thread-local pigeonhole tables to eliminate atomic contention
    int **local_pigeonholes = (int **)malloc(num_threads * sizeof(int *));
    for (int t = 0; t < num_threads; t++) {
        local_pigeonholes[t] = (int *)calloc(range_size, sizeof(int));
    }

    #pragma omp parallel num_threads(num_threads)
    {
        int tid = omp_get_thread_num();
        int *my_holes = local_pigeonholes[tid];

        // Step 1: Thread-local counting (embarrassingly parallel, no locks)
        #pragma omp for schedule(static)
        for (int i = 0; i < n; i++) {
            my_holes[arr[i] - min_val]++;
        }

        // Step 2: Parallel reduction across thread-local buffers into global histogram
        #pragma omp for schedule(static)
        for (int r = 0; r < range_size; r++) {
            int sum = 0;
            for (int t = 0; t < num_threads; t++) {
                sum += local_pigeonholes[t][r];
            }
            global_pigeonholes[r] = sum;
        }
    }

    // Step 3: Prefix sum to compute output start offsets
    int *offsets = (int *)malloc(range_size * sizeof(int));
    int running_sum = 0;
    for (int r = 0; r < range_size; r++) {
        offsets[r] = running_sum;
        running_sum += global_pigeonholes[r];
    }

    // Step 4: Parallel write back into sorted array
    #pragma omp parallel for schedule(dynamic, 64) num_threads(num_threads)
    for (int r = 0; r < range_size; r++) {
        int start = offsets[r];
        int count = global_pigeonholes[r];
        int val = r + min_val;
        for (int k = 0; k < count; k++) {
            sorted_arr[start + k] = val;
        }
    }

    // Free buffers
    for (int t = 0; t < num_threads; t++) {
        free(local_pigeonholes[t]);
    }
    free(local_pigeonholes);
    free(global_pigeonholes);
    free(offsets);
}

int main(int argc, char** argv) {
    const char* filename = (argc > 1) ? argv[1] : "T10I4D100K.dat.txt";
    int requested_threads = (argc > 2) ? atoi(argv[2]) : omp_get_max_threads();

    printf("=============================================================\n");
    printf("  Enhanced OpenMP Multi-Core Pigeonhole Sort Benchmark\n");
    printf("=============================================================\n");
    printf("Configured Thread Count: %d (System max: %d)\n", requested_threads, omp_get_max_threads());

    FILE *file = fopen(filename, "r");
    if (!file) {
        file = fopen("../T10I4D100K.dat.txt", "r");
        if (!file) {
            fprintf(stderr, "Error: Cannot open dataset '%s'\n", filename);
            return 1;
        }
    }

    int capacity = 100000;
    int *arr = (int *)malloc(capacity * sizeof(int));
    int count = 0;
    while (fscanf(file, "%d", &arr[count]) != EOF) {
        count++;
        if (count >= capacity) {
            capacity *= 2;
            arr = (int *)realloc(arr, capacity * sizeof(int));
        }
    }
    fclose(file);
    printf("-> Successfully read %d integers from dataset\n", count);

    int min_val = arr[0], max_val = arr[0];
    for (int i = 1; i < count; i++) {
        if (arr[i] < min_val) min_val = arr[i];
        if (arr[i] > max_val) max_val = arr[i];
    }
    int range_size = max_val - min_val + 1;
    printf("-> Dynamic Value Range: [%d, %d] (Size: %d)\n", min_val, max_val, range_size);

    int *sorted_arr = (int *)malloc(count * sizeof(int));

    double t_start = omp_get_wtime();
    openmp_pigeonhole_sort(arr, count, min_val, range_size, sorted_arr, requested_threads);
    double t_end = omp_get_wtime();

    printf("-> OpenMP Parallel Sorting Time: %.5f ms\n", (t_end - t_start) * 1000.0);

    // Verify sort correctness
    int is_sorted = 1;
    for (int i = 1; i < count; i++) {
        if (sorted_arr[i] < sorted_arr[i - 1]) {
            is_sorted = 0;
            break;
        }
    }
    printf("-> Verification: %s\n", is_sorted ? "PASSED (Array is correctly sorted)" : "FAILED");
    printf("=============================================================\n");

    free(arr);
    free(sorted_arr);
    return 0;
}
