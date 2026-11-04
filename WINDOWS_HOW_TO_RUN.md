# How to Run Pigeonhole Sort on Windows

This guide explains how to compile and run the Pigeonhole Sort project on a Windows computer.

---

## ⚡ Quickest Method: Double-Click `run_windows.bat`

If you have a C compiler (`gcc` from MinGW/MSYS2 or `cl` from Visual Studio) installed on your Windows PC:
1. Simply double-click **`run_windows.bat`**.
2. An interactive menu will open in Command Prompt allowing you to compile and run:
   - Enhanced Sequential Sort (Single-core CPU)
   - Enhanced OpenMP Sort (Multi-core CPU)
   - Scalable CUDA Sort (if you have an NVIDIA GPU + CUDA Toolkit installed)
   - Baseline Sequential Sort (`pg1.c`)

---

## 🛠️ Method 1: Using GCC / MinGW (Command Prompt or PowerShell)

If you have MinGW-w64, MSYS2, or w64devkit installed:

### 1. Sequential Sort (Single-Thread CPU)
```cmd
gcc -O3 sequential_pigeonhole.c -o seq_sort.exe
seq_sort.exe T10I4D100K.dat.txt
```

### 2. OpenMP Multi-Core Sort (Multi-Threaded CPU)
```cmd
gcc -O3 -fopenmp openmp_pigeonhole.c -o omp_sort.exe

:: Run with 2 threads
omp_sort.exe T10I4D100K.dat.txt 2

:: Run with 4 threads
omp_sort.exe T10I4D100K.dat.txt 4
```

### 3. Baseline Sequential Sort (`pg1.c`)
```cmd
gcc -O3 pg1.c -o pg1.exe
pg1.exe T10I4D100K.dat.txt
```

---

## 💻 Method 2: Using Microsoft Visual Studio (MSVC `cl.exe`)

Open the **"x64 Native Tools Command Prompt for VS"** from your Start menu:

### 1. Sequential Sort
```cmd
cl /O2 sequential_pigeonhole.c /Fe:seq_sort.exe
seq_sort.exe T10I4D100K.dat.txt
```

### 2. OpenMP Multi-Core Sort
```cmd
cl /O2 /openmp openmp_pigeonhole.c /Fe:omp_sort.exe
omp_sort.exe T10I4D100K.dat.txt 4
```

---

## 🚀 Method 3: Running NVIDIA CUDA GPU Sort (`cuda_scalable_pigeonhole.cu`)

If your Windows laptop has an **NVIDIA GeForce / RTX GPU**:
1. Install the [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads).
2. Open Command Prompt and check your GPU compiler:
   ```cmd
   nvcc --version
   ```
3. Compile and execute:
   ```cmd
   nvcc -O3 cuda_scalable_pigeonhole.cu -o cuda_sort.exe
   cuda_sort.exe T10I4D100K.dat.txt
   ```

---

## 🌐 Method 4: Running Distributed MPI (`mpi_range_partition.c`)

On Windows, MPI requires **Microsoft MPI (MS-MPI)**:
1. Download and install **MS-MPI** (both `msmpisetup.exe` and `msmpisdk.msi`) from [Microsoft's official site](https://www.microsoft.com/en-us/download/details.aspx?id=105260).
2. Or run inside **WSL (Windows Subsystem for Linux)**:
   ```bash
   sudo apt update && sudo apt install -y openmpi-bin libopenmpi-dev gcc
   mpicc -O3 mpi_range_partition.c -o mpi_sort
   mpirun -np 4 ./mpi_sort T10I4D100K.dat.txt
   ```

---

## ☁️ Method 5: 1-Click Google Colab (Runs All with Free Cloud GPU!)

If you do NOT want to install anything on your Windows laptop:
1. Open Google Chrome / Edge and visit: [colab.research.google.com](https://colab.research.google.com)
2. Click **Upload** and upload **`HPCS_Pigeonhole_Sort_Colab.ipynb`**.
3. In Colab, click the **Folder icon** on the left and upload **`T10I4D100K.dat.txt`**.
4. Go to **Runtime** -> **Change runtime type** -> Select **T4 GPU** -> Click **Save**.
5. Click **Runtime** -> **Run all**.
Everything (Sequential, OpenMP, MPI, and CUDA GPU) will compile and run automatically in the cloud!
