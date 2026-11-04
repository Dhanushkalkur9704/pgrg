#include <stdio.h>
#include <stdlib.h>

#ifdef _WIN32
#include <windows.h>
static inline double getCurrentTime() {
    LARGE_INTEGER freq, counter;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&counter);
    return (double)counter.QuadPart * 1000.0 / (double)freq.QuadPart;
}
#else
#include <time.h>
static inline double getCurrentTime() {
    struct timespec currentTime;
    clock_gettime(CLOCK_MONOTONIC, &currentTime);
    return (double)currentTime.tv_sec * 1000.0 + (double)currentTime.tv_nsec / 1000000.0;
}
#endif

void pigeonhole_sort(int arr[], int n, int min_val, int range_size, int* sorted_arr) {
    int *pigeonholes = (int *)calloc(range_size, sizeof(int));
    if (!pigeonholes) {
        fprintf(stderr, "Memory allocation error in pigeonhole_sort\n");
        exit(1);
    }

    for (int i = 0; i < n; i++) {
        pigeonholes[arr[i] - min_val]++;
    }

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
    int capacity = 100000;
    int *arr = (int *)malloc(capacity * sizeof(int));

    double startTime = getCurrentTime();
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        file = fopen("../T10I4D100K.dat.txt", "r");
        if (file == NULL) {
            fprintf(stderr, "Could not open the file '%s' for reading.\n", filename);
            free(arr);
            return 1;
        }
    }

    int count = 0;
    while (fscanf(file, "%d", &arr[count]) != EOF) {
        count++;
        if (count >= capacity) {
            capacity *= 2;
            arr = (int *)realloc(arr, capacity * sizeof(int));
        }
    }

    fclose(file);
    double endTime = getCurrentTime();
    double totalTime = endTime - startTime;
    printf("Numbers read: %d\n", count);
    printf("Time taken by the loading: %.5f milliseconds\n", totalTime);

    startTime = getCurrentTime();
    int min_val = arr[0];
    int max_val = arr[0];
    for (int i = 1; i < count; i++) {
        if (arr[i] < min_val) {
            min_val = arr[i];
        }
        if (arr[i] > max_val) {
            max_val = arr[i];
        }
    }

    int range_size = max_val - min_val + 1;
    int *sorted_arr = (int *)malloc(count * sizeof(int));
    
    pigeonhole_sort(arr, count, min_val, range_size, sorted_arr);
    endTime = getCurrentTime();

    totalTime = endTime - startTime;
    printf("Time taken by the sorting: %.5f milliseconds\n", totalTime);

    // Verify sort
    int is_sorted = 1;
    for (int i = 1; i < count; i++) {
        if (sorted_arr[i] < sorted_arr[i - 1]) {
            is_sorted = 0;
            break;
        }
    }
    printf("Verification: %s\n", is_sorted ? "PASSED" : "FAILED");

    free(arr);
    free(sorted_arr);

    return 0;
}
