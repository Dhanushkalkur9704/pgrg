"""
IEEE Paper Publication-Quality Workflow Diagram Generator
High-Performance Computing Systems (HPCS)
Topic: Parallelization of Pigeonhole Sort across CPU, OpenMP, MPI, and CUDA
Strictly Black and White (Monochrome / Grayscale) for IEEE Transactions Printing
Generates:
  1. ieee_pigeonhole_workflow_diagram.png (300 DPI, IEEE standard format)
  2. ieee_pigeonhole_workflow_diagram.pdf (Vector format for LaTeX IEEEtran)
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

def create_ieee_workflow(output_png="ieee_pigeonhole_workflow_diagram.png",
                         output_pdf="ieee_pigeonhole_workflow_diagram.pdf"):
    fig, ax = plt.subplots(figsize=(19, 11), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 100)
    ax.set_ylim(100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    FONT_FAMILY = "sans-serif"
    COLOR_TEXT = "#000000"
    COLOR_MUTED = "#333333"

    # Monochrome tokens for the 4 paradigms
    C_INPUT = {"bg": "#F5F5F5", "edge": "#000000", "title": "#000000"}
    C_SEQ   = {"bg": "#FFFFFF", "edge": "#000000", "title": "#000000", "badge_bg": "#F0F0F0", "badge_txt": "#000000"}
    C_OMP   = {"bg": "#F5F5F5", "edge": "#000000", "title": "#000000", "badge_bg": "#E8E8E8", "badge_txt": "#000000"}
    C_MPI   = {"bg": "#EBEBEB", "edge": "#000000", "title": "#000000", "badge_bg": "#DEDEDE", "badge_txt": "#000000"}
    C_CUDA  = {"bg": "#E0E0E0", "edge": "#000000", "title": "#000000", "badge_bg": "#D5D5D5", "badge_txt": "#000000"}
    C_OUT   = {"bg": "#F8F8F8", "edge": "#000000", "title": "#000000"}

    def draw_card(x, y, w, h, bg, edge, rad=1.2, lw=1.5, zorder=2, hatch=None):
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle=f"round,pad=0.25,rounding_size={rad}",
                             facecolor=bg, edgecolor=edge, linewidth=lw, hatch=hatch, zorder=zorder)
        ax.add_patch(box)
        return box

    def draw_arrow(x1, y1, x2, y2, color="#000000", lw=1.8, style="-|>", rad=0.0):
        connection = f"arc3,rad={rad}" if rad != 0 else "arc3"
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                connectionstyle=connection,
                                arrowstyle=f"{style},head_width=4.5,head_length=6.5",
                                color=color, linewidth=lw, zorder=4)
        ax.add_patch(arrow)

    # 0. FIGURE HEADER (IEEE Academic Format - Black and White)
    ax.text(50, 98.2, "High-Performance Parallelization Workflow of Pigeonhole Sort",
            ha="center", va="top", fontsize=17.5, fontweight="bold", color=COLOR_TEXT, family=FONT_FAMILY)
    ax.text(50, 95.3, "End-to-End Architectural Pipeline across Multi-Core CPU, Distributed Cluster, and Many-Core GPU",
            ha="center", va="top", fontsize=11, color=COLOR_MUTED, family=FONT_FAMILY)

    # 1. STAGE I: INGESTION & PROFILING (Left Column)
    draw_card(2.5, 6, 20.5, 86, "#FFFFFF", "#000000", rad=1.4, lw=1.2, zorder=1)
    ax.text(12.75, 88.8, "STAGE I: INGESTION", ha="center", va="center",
            fontsize=12, fontweight="bold", color=COLOR_TEXT)
    ax.text(12.75, 86.6, "Input & Extrema Profiling", ha="center", va="center",
            fontsize=9.5, color=COLOR_MUTED, style="italic")

    # Card 1.1: Dataset
    draw_card(4.2, 66.5, 17.1, 17.0, C_INPUT["bg"], C_INPUT["edge"])
    ax.text(12.75, 80.5, "Benchmark Dataset", ha="center", va="center", fontsize=10.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(12.75, 76.0, "IBM Quest Synthetic\n(T10I4D100K.dat.txt)", ha="center", va="center", fontsize=9, color=COLOR_TEXT)
    ax.text(12.75, 70.0, "Size: N ≈ 1,010,228\nType: 32-bit Integers", ha="center", va="center", fontsize=8.5, color=COLOR_MUTED)

    draw_arrow(12.75, 66.5, 12.75, 55.5, color="#000000")

    # Card 1.2: Dynamic Range Scanner
    draw_card(4.2, 38.0, 17.1, 17.5, C_INPUT["bg"], C_INPUT["edge"])
    ax.text(12.75, 52.5, "Dynamic Range Scanner", ha="center", va="center", fontsize=10.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(12.75, 48.0, "Min/Max Extrema Profiling", ha="center", va="center", fontsize=9, color=COLOR_TEXT)
    ax.text(12.75, 42.5, "min = min(A), max = max(A)\nRange Size = max - min + 1\n(Range = 1000, [0 .. 999])",
            ha="center", va="center", fontsize=8.2, color=COLOR_TEXT, fontweight="bold")

    draw_arrow(12.75, 38.0, 12.75, 27.0, color="#000000")

    # Card 1.3: Heap Memory
    draw_card(4.2, 9.5, 17.1, 17.5, C_INPUT["bg"], C_INPUT["edge"])
    ax.text(12.75, 23.8, "Memory Allocation", ha="center", va="center", fontsize=10.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(12.75, 18.5, "Safe Heap Allocation (calloc)\nReplaces Unsafe Stack VLAs\nEliminates Segfault Barrier",
            ha="center", va="center", fontsize=8.5, color=COLOR_TEXT)

    # Bus line from Stage I to Stage II
    hub1_x = 22.8
    bus1_x = 26.0
    ax.plot([hub1_x, bus1_x], [46.75, 46.75], color="#000000", linewidth=2.0, zorder=3)
    ax.plot([bus1_x, bus1_x], [74.5, 14.5], color="#000000", linewidth=2.0, zorder=3)

    # 2. STAGE II: PARALLEL ARCHITECTURES (Center Body)
    draw_card(27.5, 6, 49.0, 86, "#FFFFFF", "#000000", rad=1.4, lw=1.2, zorder=1)
    ax.text(52.0, 89.2, "STAGE II: ARCHITECTURAL PARALLELIZATION ENGINES", ha="center", va="center",
            fontsize=12, fontweight="bold", color=COLOR_TEXT)
    ax.text(52.0, 87.0, "Concurrent Histogram Accumulation, Prefix Scan & Parallel Scatter Phases", ha="center", va="center",
            fontsize=9.5, color=COLOR_MUTED, style="italic")

    # TRACK 1: Sequential CPU
    y_seq = 67.5
    draw_arrow(bus1_x, y_seq + 7.5, 29.5, y_seq + 7.5, color="#000000")
    draw_card(29.5, y_seq, 45.0, 15.0, C_SEQ["bg"], C_SEQ["edge"])
    
    ax.text(31.2, y_seq + 12.3, "1. SEQUENTIAL CPU (Baseline pg1.c & Enhanced Heap)", fontsize=10, fontweight="bold", color=COLOR_TEXT)
    ax.text(72.5, y_seq + 12.3, "O(N + Range)", fontsize=8.2, fontweight="bold", color=COLOR_TEXT, ha="right",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#F0F0F0", edgecolor="#000000", lw=0.8))
    
    step_w = 12.8
    draw_card(31.0, y_seq + 1.8, step_w, 8.2, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(31.0 + step_w/2, y_seq + 7.0, "Pigeonhole Count", ha="center", fontsize=8.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(31.0 + step_w/2, y_seq + 3.8, "for x in A:\n  Holes[x - min]++", ha="center", fontsize=7.5, color=COLOR_TEXT)
    draw_arrow(31.0 + step_w, y_seq + 5.9, 46.0, y_seq + 5.9, color="#000000", lw=1.2)

    draw_card(46.0, y_seq + 1.8, step_w, 8.2, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(46.0 + step_w/2, y_seq + 7.0, "Cumulative Scan", ha="center", fontsize=8.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(46.0 + step_w/2, y_seq + 3.8, "Prefix scan on Holes\nCompute write offsets", ha="center", fontsize=7.5, color=COLOR_TEXT)
    draw_arrow(46.0 + step_w, y_seq + 5.9, 61.0, y_seq + 5.9, color="#000000", lw=1.2)

    draw_card(61.0, y_seq + 1.8, step_w - 0.5, 8.2, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(61.0 + (step_w-0.5)/2, y_seq + 7.0, "Linear Scatter", ha="center", fontsize=8.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(61.0 + (step_w-0.5)/2, y_seq + 3.8, "Sequential writeback\nA[idx++] = val", ha="center", fontsize=7.5, color=COLOR_TEXT)

    # TRACK 2: OpenMP Multi-Core
    y_omp = 48.0
    draw_arrow(bus1_x, y_omp + 7.5, 29.5, y_omp + 7.5, color="#000000")
    draw_card(29.5, y_omp, 45.0, 15.5, C_OMP["bg"], C_OMP["edge"])
    
    ax.text(31.2, y_omp + 12.8, "2. MULTI-CORE OPENMP (Shared-Memory CPU Parallelism)", fontsize=10, fontweight="bold", color=COLOR_TEXT)
    ax.text(72.5, y_omp + 12.8, "Threads: 2, 4, 8 cores", fontsize=8.2, fontweight="bold", color=COLOR_TEXT, ha="right",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#E8E8E8", edgecolor="#000000", lw=0.8))

    draw_card(31.0, y_omp + 1.8, step_w, 8.7, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(31.0 + step_w/2, y_omp + 7.6, "Thread Histograms", ha="center", fontsize=8.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(31.0 + step_w/2, y_omp + 4.2, "#pragma omp parallel\nThread-local arrays\nLock-free counting", ha="center", fontsize=7.5, color=COLOR_TEXT)
    draw_arrow(31.0 + step_w, y_omp + 6.1, 46.0, y_omp + 6.1, color="#000000", lw=1.2)

    draw_card(46.0, y_omp + 1.8, step_w, 8.7, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(46.0 + step_w/2, y_omp + 7.6, "Parallel Reduction", ha="center", fontsize=8.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(46.0 + step_w/2, y_omp + 4.2, "Sum thread histograms\nParallel prefix scan\nCalculate thread slices", ha="center", fontsize=7.5, color=COLOR_TEXT)
    draw_arrow(46.0 + step_w, y_omp + 6.1, 61.0, y_omp + 6.1, color="#000000", lw=1.2)

    draw_card(61.0, y_omp + 1.8, step_w - 0.5, 8.7, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(61.0 + (step_w-0.5)/2, y_omp + 7.6, "Parallel Scatter", ha="center", fontsize=8.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(61.0 + (step_w-0.5)/2, y_omp + 4.2, "Non-overlapping writes\nThreads scatter into A\nSpeedup: ~2.16x (4T)", ha="center", fontsize=7.5, color=COLOR_TEXT)

    # TRACK 3: Distributed MPI
    y_mpi = 28.5
    draw_arrow(bus1_x, y_mpi + 7.5, 29.5, y_mpi + 7.5, color="#000000")
    draw_card(29.5, y_mpi, 45.0, 15.5, C_MPI["bg"], C_MPI["edge"])
    
    ax.text(31.2, y_mpi + 12.8, "3. DISTRIBUTED MPI (Zero-Merge Range Partitioned Architecture)", fontsize=10, fontweight="bold", color=COLOR_TEXT)
    ax.text(72.5, y_mpi + 12.8, "Zero-Merge Cluster", fontsize=8.2, fontweight="bold", color=COLOR_TEXT, ha="right",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#DEDEDE", edgecolor="#000000", lw=0.8))

    draw_card(31.0, y_mpi + 1.8, step_w, 8.7, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(31.0 + step_w/2, y_mpi + 7.6, "Range Slicing", ha="center", fontsize=8.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(31.0 + step_w/2, y_mpi + 4.2, "Divide [min..max] into\ndisjoint rank intervals\n[min_r, max_r] for P ranks", ha="center", fontsize=7.5, color=COLOR_TEXT)
    draw_arrow(31.0 + step_w, y_mpi + 6.1, 46.0, y_mpi + 6.1, color="#000000", lw=1.2)

    draw_card(46.0, y_mpi + 1.8, step_w, 8.7, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(46.0 + step_w/2, y_mpi + 7.6, "MPI_Scatterv", ha="center", fontsize=8.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(46.0 + step_w/2, y_mpi + 4.2, "Bucketed send to ranks\nEach rank sorts local\ninterval in memory", ha="center", fontsize=7.5, color=COLOR_TEXT)
    draw_arrow(46.0 + step_w, y_mpi + 6.1, 61.0, y_mpi + 6.1, color="#000000", lw=1.2)

    draw_card(61.0, y_mpi + 1.8, step_w - 0.5, 8.7, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(61.0 + (step_w-0.5)/2, y_mpi + 7.6, "MPI_Gatherv (Zero-Merge)", ha="center", fontsize=8.0, fontweight="bold", color=COLOR_TEXT)
    ax.text(61.0 + (step_w-0.5)/2, y_mpi + 4.2, "Direct concatenation!\nZero post-merge overhead\nSpeedup: ~3.01x (4 Ranks)", ha="center", fontsize=7.5, color=COLOR_TEXT)

    # TRACK 4: NVIDIA CUDA GPU
    y_cuda = 9.0
    draw_arrow(bus1_x, y_cuda + 7.5, 29.5, y_cuda + 7.5, color="#000000")
    draw_card(29.5, y_cuda, 45.0, 15.5, C_CUDA["bg"], C_CUDA["edge"])
    
    ax.text(31.2, y_cuda + 12.8, "4. MASSIVELY PARALLEL CUDA (NVIDIA Many-Core GPU)", fontsize=10, fontweight="bold", color=COLOR_TEXT)
    ax.text(72.5, y_cuda + 12.8, "Grid-Stride Atomics", fontsize=8.2, fontweight="bold", color=COLOR_TEXT, ha="right",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#D5D5D5", edgecolor="#000000", lw=0.8))

    draw_card(31.0, y_cuda + 1.8, step_w, 8.7, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(31.0 + step_w/2, y_cuda + 7.6, "cudaMemcpy (H2D)", ha="center", fontsize=8.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(31.0 + step_w/2, y_cuda + 4.2, "Transfer A to Device\nMulti-block grid launch\nBlocks: 1024, Threads: 256", ha="center", fontsize=7.5, color=COLOR_TEXT)
    draw_arrow(31.0 + step_w, y_cuda + 6.1, 46.0, y_cuda + 6.1, color="#000000", lw=1.2)

    draw_card(46.0, y_cuda + 1.8, step_w, 8.7, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(46.0 + step_w/2, y_cuda + 7.6, "Global atomicAdd", ha="center", fontsize=8.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(46.0 + step_w/2, y_cuda + 4.2, "Grid-stride histogram\nNo 48KB shared barrier\nParallel GPU prefix sum", ha="center", fontsize=7.5, color=COLOR_TEXT)
    draw_arrow(46.0 + step_w, y_cuda + 6.1, 61.0, y_cuda + 6.1, color="#000000", lw=1.2)

    draw_card(61.0, y_cuda + 1.8, step_w - 0.5, 8.7, "#FFFFFF", "#000000", rad=0.7, lw=1.0)
    ax.text(61.0 + (step_w-0.5)/2, y_cuda + 7.6, "cudaMemcpy (D2H)", ha="center", fontsize=8.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(61.0 + (step_w-0.5)/2, y_cuda + 4.2, "Parallel atomic scatter\nTransfer sorted back\nSpeedup: ~4.48x - 5.15x", ha="center", fontsize=7.5, color=COLOR_TEXT)

    # 3. CONVERGENCE BUS & ARROW INTO STAGE III
    bus2_x = 76.5
    ax.plot([74.5, bus2_x], [y_seq + 7.5, y_seq + 7.5], color="#000000", linewidth=2.0, zorder=3)
    ax.plot([74.5, bus2_x], [y_omp + 7.5, y_omp + 7.5], color="#000000", linewidth=2.0, zorder=3)
    ax.plot([74.5, bus2_x], [y_mpi + 7.5, y_mpi + 7.5], color="#000000", linewidth=2.0, zorder=3)
    ax.plot([74.5, bus2_x], [y_cuda + 7.5, y_cuda + 7.5], color="#000000", linewidth=2.0, zorder=3)
    ax.plot([bus2_x, bus2_x], [y_seq + 7.5, y_cuda + 7.5], color="#000000", linewidth=2.0, zorder=3)

    draw_arrow(bus2_x, 46.75, 78.5, 46.75, color="#000000", lw=2.2)

    # 4. STAGE III: CONVERGENCE & VERIFICATION (Right Column)
    draw_card(78.5, 6, 19.0, 86, "#FFFFFF", "#000000", rad=1.4, lw=1.2, zorder=1)
    ax.text(88.0, 88.8, "STAGE III: VERIFICATION", ha="center", va="center",
            fontsize=12, fontweight="bold", color=COLOR_TEXT)
    ax.text(88.0, 86.6, "Correctness & Benchmark Profiling", ha="center", va="center",
            fontsize=9.5, color=COLOR_MUTED, style="italic")

    # Card 3.1: Sorted Output Array
    draw_card(79.8, 66.5, 16.4, 17.0, C_OUT["bg"], "#000000")
    ax.text(88.0, 80.5, "Sorted Output Array", ha="center", va="center", fontsize=10.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(88.0, 75.5, "A_sorted = [a_1, a_2, ... a_N]", ha="center", va="center", fontsize=8.8, color=COLOR_TEXT)
    ax.text(88.0, 70.0, "Monotonically ordered\nIdentical distribution", ha="center", va="center", fontsize=8.2, color=COLOR_MUTED)

    draw_arrow(88.0, 66.5, 88.0, 55.5, color="#000000")

    # Card 3.2: Formal Correctness
    draw_card(79.8, 38.0, 16.4, 17.5, C_OUT["bg"], "#000000")
    ax.text(88.0, 52.5, "Validation Kernel", ha="center", va="center", fontsize=10.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(88.0, 47.5, "Strict Assertion Check:", ha="center", va="center", fontsize=8.8, color=COLOR_TEXT)
    ax.text(88.0, 42.5, "∀ i ∈ [0, N-2]:\nA[i] ≤ A[i+1]\nStatus: PASSED", ha="center", va="center",
            fontsize=8.5, fontweight="bold", color=COLOR_TEXT)

    draw_arrow(88.0, 38.0, 88.0, 27.0, color="#000000")

    # Card 3.3: Metrics Report
    draw_card(79.8, 9.5, 16.4, 17.5, C_OUT["bg"], "#000000")
    ax.text(88.0, 23.8, "IEEE Metrics Report", ha="center", va="center", fontsize=10.5, fontweight="bold", color=COLOR_TEXT)
    ax.text(88.0, 18.0, "• Execution Time (ms)\n• Speedup: S_p = T_seq / T_par\n• Scaling Efficiency (E_p)\n• Automated .PNG Graphs",
            ha="center", va="center", fontsize=8.2, color=COLOR_TEXT)

    # FOOTER: IEEE Paper Caption
    ax.text(50, 2.2, "Fig. 1. Architectural workflow of the parallelized Pigeonhole Sort framework. "
                     "Input data is dynamically profiled and partitioned across Sequential CPU, "
                     "OpenMP multi-core, distributed Zero-Merge MPI, and NVIDIA CUDA many-core GPU engines.",
            ha="center", va="center", fontsize=9.2, color="#333333", style="italic")

    plt.savefig(output_png, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.savefig(output_pdf, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print(f"IEEE Monochrome Workflow Diagram generated successfully:")
    print(f" -> High-res PNG: {output_png}")
    print(f" -> Vector PDF:   {output_pdf}")

if __name__ == "__main__":
    create_ieee_workflow()
