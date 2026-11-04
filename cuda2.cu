#include <stdio.h>
#include <stdlib.h>
#include <cuda_runtime.h>

#define CUDA_CHECK(call) \
do { \
    cudaError_t cudaErr = (call); \
    if (cudaErr != cudaSuccess) { \
        fprintf(stderr, "CUDA Error - %s:%d: '%s'\n", __FILE__, __LINE__, cudaGetErrorString(cudaErr)); \
        exit(EXIT_FAILURE); \
    } \
} while (0)

__global__ void pigeonhole_sort_kernel(int* arr, int n, int min_val, int range_size) {
    extern __shared__ int local_pigeonholes[];

    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    int stride = blockDim.x * gridDim.x;

    // Initialize local pigeonholes
    for (int i = threadIdx.x; i < range_size; i += blockDim.x) {
        local_pigeonholes[i] = 0;
    }
    __syncthreads();

    // Count occurrences in local pigeonholes
    while (tid < n) {
        atomicAdd(&local_pigeonholes[arr[tid] - min_val], 1);
        tid += stride;
    }
    __syncthreads();

    // Perform parallel prefix sum (scan) to calculate starting indices
    for (int i = 1; i < range_size; i <<= 1) {
        if (threadIdx.x >= i) {
            local_pigeonholes[threadIdx.x] += local_pigeonholes[threadIdx.x - i];
        }
        __syncthreads();
    }

    // Write sorted values to shared memory in correct order
    tid = threadIdx.x + blockIdx.x * blockDim.x;
    while (tid < n) {
        int index = atomicSub(&local_pigeonholes[arr[tid] - min_val], 1) - 1;
        arr[index] = arr[tid];
        tid += stride;
    }
}

int main(int argc, char** argv) {
    cudaEvent_t sort_start, sort_end;
    float sort_time;

    int n;
    int* arr = NULL;
    const char* filename = (argc > 1) ? argv[1] : "T10I4D100K.dat.txt";

    CUDA_CHECK(cudaEventCreate(&sort_start));
    CUDA_CHECK(cudaEventCreate(&sort_end));
    int capacity = 100000;
    arr = (int*)malloc(capacity * sizeof(int));

    FILE* file = fopen(filename, "r");
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
            arr = (int*)realloc(arr, capacity * sizeof(int));
        }
    }

    fclose(file);
    n = count;

    printf("Numbers read from the file: %d\n", n);

    // Compute dynamic min/max
    int min_val = arr[0];
    int max_val = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] < min_val) min_val = arr[i];
        if (arr[i] > max_val) max_val = arr[i];
    }
    int range_size = max_val - min_val + 1;
    printf("Dynamic range: [%d, %d] (size: %d)\n", min_val, max_val, range_size);

    // Copy data to GPU
    int* d_arr;
    CUDA_CHECK(cudaMalloc((void**)&d_arr, n * sizeof(int)));
    CUDA_CHECK(cudaMemcpy(d_arr, arr, n * sizeof(int), cudaMemcpyHostToDevice));

    // Calculate block and grid dimensions
    int block_size = 256;
    int grid_size = (n + block_size - 1) / block_size;
    if (grid_size > 1024) grid_size = 1024;

    CUDA_CHECK(cudaEventRecord(sort_start));
    pigeonhole_sort_kernel<<<grid_size, block_size, range_size * sizeof(int)>>>(d_arr, n, min_val, range_size);
    CUDA_CHECK(cudaDeviceSynchronize());
    CUDA_CHECK(cudaEventRecord(sort_end));
    CUDA_CHECK(cudaEventSynchronize(sort_end));
    CUDA_CHECK(cudaEventElapsedTime(&sort_time, sort_start, sort_end));

    printf("Sorting kernel execution time: %f ms\n", sort_time);

    // Copy sorted data back to the host
    CUDA_CHECK(cudaMemcpy(arr, d_arr, n * sizeof(int), cudaMemcpyDeviceToHost));

    // Verification
    int is_sorted = 1;
    for (int i = 1; i < n; i++) {
        if (arr[i] < arr[i - 1]) {
            is_sorted = 0;
            break;
        }
    }
    printf("Verification: %s\n", is_sorted ? "PASSED" : "FAILED");

    free(arr);
    CUDA_CHECK(cudaFree(d_arr));
    CUDA_CHECK(cudaEventDestroy(sort_start));
    CUDA_CHECK(cudaEventDestroy(sort_end));

    return 0;
}
