#include <stdio.h>
#include <stdlib.h>

#ifdef _WIN32
#include <windows.h>
static inline double get_time_ms() {
    LARGE_INTEGER freq, counter;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&counter);
    return (double)counter.QuadPart * 1000.0 / (double)freq.QuadPart;
}
#else
#include <time.h>
static inline double get_time_ms() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec * 1000.0 + (double)ts.tv_nsec / 1000000.0;
}
#endif

/**
 * Enhanced Sequential Pigeonhole Sort
 * Features:
 * 1. Safe dynamic heap allocation (calloc) preventing stack overflow on large ranges.
 * 2. Dynamic range detection [min_val, max_val].
 * 3. Buffered streaming I/O with dynamic array resizing.
 * 4. High-precision monotonic timer (Windows QueryPerformanceCounter / POSIX CLOCK_MONOTONIC).
 */

void pigeonhole_sort(const int* arr, int n, int min_val, int range_size, int* sorted_arr) {
    // Dynamically allocate pigeonholes on the heap (zero-initialized)
    int *pigeonholes = (int *)calloc(range_size, sizeof(int));
    if (!pigeonholes) {
        fprintf(stderr, "Error: Memory allocation failed for pigeonholes of size %d\n", range_size);
        exit(EXIT_FAILURE);
    }

    // Step 1: Frequency tallying
    for (int i = 0; i < n; i++) {
        pigeonholes[arr[i] - min_val]++;
    }

    // Step 2: Reconstruct sorted output
    int index = 0;
    for (int i = 0; i < range_size; i++) {
        while (pigeonholes[i] > 0) {
            sorted_arr[index++] = i + min_val;
            pigeonholes[i]--;
        }
    }

    free(pigeonholes);
}

int main(int argc, char** argv) {
    const char* filename = (argc > 1) ? argv[1] : "T10I4D100K.dat.txt";
    
    printf("=============================================================\n");
    printf("  Enhanced Sequential Pigeonhole Sort Benchmark\n");
    printf("=============================================================\n");
    printf("Reading dataset from: %s\n", filename);

    double load_start = get_time_ms();
    FILE *file = fopen(filename, "r");
    if (!file) {
        // Try fallback to parent directory if not found in current directory
        file = fopen("../T10I4D100K.dat.txt", "r");
        if (!file) {
            fprintf(stderr, "Error: Cannot open dataset '%s'. Make sure it is in current or parent directory.\n", filename);
            return 1;
        }
    }

    int capacity = 100000;
    int *arr = (int *)malloc(capacity * sizeof(int));
    if (!arr) {
        fprintf(stderr, "Memory allocation error\n");
        fclose(file);
        return 1;
    }

    int count = 0;
    while (fscanf(file, "%d", &arr[count]) != EOF) {
        count++;
        if (count >= capacity) {
            capacity *= 2;
            int *new_arr = (int *)realloc(arr, capacity * sizeof(int));
            if (!new_arr) {
                fprintf(stderr, "Memory reallocation error\n");
                free(arr);
                fclose(file);
                return 1;
            }
            arr = new_arr;
        }
    }
    fclose(file);
    double load_end = get_time_ms();
    printf("-> Successfully read %d integers in %.3f ms\n", count, load_end - load_start);

    // Compute dynamic min and max
    int min_val = arr[0];
    int max_val = arr[0];
    for (int i = 1; i < count; i++) {
        if (arr[i] < min_val) min_val = arr[i];
        if (arr[i] > max_val) max_val = arr[i];
    }
    int range_size = max_val - min_val + 1;
    printf("-> Dynamic Value Range: [%d, %d] (Range Size: %d)\n", min_val, max_val, range_size);

    int *sorted_arr = (int *)malloc(count * sizeof(int));
    if (!sorted_arr) {
        fprintf(stderr, "Memory allocation error for sorted array\n");
        free(arr);
        return 1;
    }

    // Benchmark sorting phase
    double sort_start = get_time_ms();
    pigeonhole_sort(arr, count, min_val, range_size, sorted_arr);
    double sort_end = get_time_ms();

    printf("-> Sorting Time: %.5f ms\n", sort_end - sort_start);

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
