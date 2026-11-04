# Makefile for Parallel Pigeonhole Sort Suite
# Compatible with Linux, macOS, and Windows (WSL / MinGW)

CC = gcc
CFLAGS = -O3 -Wall
MPICC = mpicc
NVCC = nvcc

# Detect Windows extension
ifeq ($(OS),Windows_NT)
    EXE = .exe
else
    EXE =
endif

all: seq omp

# 1. Enhanced Sequential Pigeonhole Sort (Runs on any CPU)
seq: sequential_pigeonhole.c
	$(CC) $(CFLAGS) sequential_pigeonhole.c -o seq_sort$(EXE)

# 2. Enhanced OpenMP Multi-Core Pigeonhole Sort (Multi-threaded CPU)
omp: openmp_pigeonhole.c
	$(CC) $(CFLAGS) -fopenmp openmp_pigeonhole.c -o omp_sort$(EXE)

# 3. Enhanced Zero-Merge Distributed MPI Pigeonhole Sort
mpi: mpi_range_partition.c
	$(MPICC) $(CFLAGS) mpi_range_partition.c -o mpi_sort$(EXE)

# 4. Enhanced Scalable Many-Core CUDA Pigeonhole Sort (NVIDIA GPU)
cuda: cuda_scalable_pigeonhole.cu
	$(NVCC) -O3 cuda_scalable_pigeonhole.cu -o cuda_sort$(EXE)

# Baseline Implementations
base_seq: pg1.c
	$(CC) $(CFLAGS) pg1.c -o pg1$(EXE)

base_mpi: mpi_new.c
	$(MPICC) $(CFLAGS) mpi_new.c -o mpi_new$(EXE)

base_cuda: cuda2.cu
	$(NVCC) -O3 cuda2.cu -o cuda2$(EXE)

# Run shortcuts
run_seq: seq
	./seq_sort$(EXE) T10I4D100K.dat.txt

run_omp: omp
	./omp_sort$(EXE) T10I4D100K.dat.txt 4

clean:
	rm -f seq_sort* omp_sort* mpi_sort* cuda_sort* pg1* mpi_new* cuda2* *.o
