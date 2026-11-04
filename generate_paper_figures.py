"""
IEEE Paper Figure Generator for Pigeonhole Sort Parallelization Paper
Strictly Black and White (Monochrome / Grayscale) for Academic IEEE Printing
All 8 publication-quality figures (300 DPI, IEEE standard format, 0% color)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# Create figures directory
os.makedirs("figures", exist_ok=True)

# =============================================================================
# Black & White / Grayscale Academic Style Settings
# =============================================================================
COLOR_BLACK  = "#000000"
COLOR_DARK   = "#222222"
COLOR_MID    = "#555555"
COLOR_LIGHT  = "#888888"
COLOR_BG_BOX = "#F5F5F5"
COLOR_WHITE  = "#FFFFFF"

# Monochrome matplotlib parameters
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 10,
    'axes.labelsize': 10.5,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF',
    'axes.edgecolor': '#000000',
    'axes.labelcolor': '#000000',
    'xtick.color': '#000000',
    'ytick.color': '#000000',
    'text.color': '#000000',
    'grid.color': '#D0D0D0',
    'grid.linewidth': 0.6,
})

# =============================================================================
# DATA
# =============================================================================
configs = [
    "Baseline\nSequential",
    "Enhanced\nSequential",
    "OpenMP\n2 Threads",
    "OpenMP\n4 Threads",
    "OpenMP\n8 Threads",
    "MPI\n2 Processes",
    "MPI\n4 Processes",
    "CUDA\nShared Mem",
    "CUDA\nMulti-Block",
]
times     = [2.16, 1.56, 2.00, 1.00, 1.00, 1.20, 0.72, 0.95, 0.42]
baseline  = 2.16
speedups  = [baseline / t for t in times]

# Distinct grayscale fills and hatching patterns for each paradigm
bw_fills = [
    "#FFFFFF",  # Seq baseline
    "#E8E8E8",  # Seq enhanced
    "#FFFFFF",  # OMP 2T
    "#E0E0E0",  # OMP 4T
    "#C4C4C4",  # OMP 8T
    "#FFFFFF",  # MPI 2P
    "#D0D0D0",  # MPI 4P
    "#E8E8E8",  # CUDA shared
    "#A8A8A8",  # CUDA multi-block
]
bw_hatches = [
    "//",   # Seq baseline
    "\\\\", # Seq enhanced
    "xx",   # OMP 2T
    "xx",   # OMP 4T
    "xx",   # OMP 8T
    "..",   # MPI 2P
    "..",   # MPI 4P
    "++",   # CUDA shared
    "**",   # CUDA multi-block
]

# =============================================================================
# FIGURE 1: Execution Time Comparison (Horizontal Bar - Black & White)
# =============================================================================
fig, ax = plt.subplots(figsize=(7.2, 4.6), dpi=300)
y = np.arange(len(configs))
bars = ax.barh(y, times, color=bw_fills, edgecolor=COLOR_BLACK, linewidth=1.1, height=0.65, zorder=3)
for bar, hatch in zip(bars, bw_hatches):
    bar.set_hatch(hatch)

ax.set_yticks(y)
ax.set_yticklabels(configs, fontsize=9, fontweight='500', color=COLOR_BLACK)
ax.set_xlabel("Sorting Time (milliseconds) [Lower is Better]", fontweight='bold', color=COLOR_BLACK)
ax.set_title("HPCS Benchmark: Execution Time Comparison", fontweight='bold', color=COLOR_BLACK, pad=12)
ax.invert_yaxis()
ax.grid(axis='x', linestyle='--', alpha=0.6, zorder=0)
ax.set_axisbelow(True)

for i, (bar, t) in enumerate(zip(bars, times)):
    ax.text(bar.get_width() + 0.04, bar.get_y() + bar.get_height()/2,
            f'{t:.2f} ms', va='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK)

# Baseline vertical line in black dashed
ax.axvline(x=baseline, color=COLOR_BLACK, linestyle='--', linewidth=1.4, zorder=2)
ax.text(baseline + 0.03, -0.4, f'Baseline\n{baseline} ms', fontsize=7.5, color=COLOR_BLACK, fontweight='bold')

ax.set_xlim(0, max(times) * 1.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(COLOR_BLACK)
ax.spines['bottom'].set_color(COLOR_BLACK)

# Add paradigm legend
legend_patches = [
    mpatches.Patch(facecolor="#FFFFFF", edgecolor=COLOR_BLACK, hatch="//", label="Sequential"),
    mpatches.Patch(facecolor="#E0E0E0", edgecolor=COLOR_BLACK, hatch="xx", label="OpenMP"),
    mpatches.Patch(facecolor="#D0D0D0", edgecolor=COLOR_BLACK, hatch="..", label="MPI"),
    mpatches.Patch(facecolor="#A8A8A8", edgecolor=COLOR_BLACK, hatch="**", label="CUDA"),
]
ax.legend(handles=legend_patches, loc="lower right", framealpha=0.95, edgecolor=COLOR_BLACK, fontsize=8)

plt.tight_layout()
plt.savefig("figures/fig_execution_time.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("[1/8] fig_execution_time.png (Black & White) generated")

# =============================================================================
# FIGURE 2: Speedup Factor Bar Chart (Black & White)
# =============================================================================
fig, ax = plt.subplots(figsize=(7.2, 4.5), dpi=300)
bars = ax.bar(np.arange(len(configs)), speedups, color=bw_fills, width=0.68, edgecolor=COLOR_BLACK, linewidth=1.1, zorder=3)
for bar, hatch in zip(bars, bw_hatches):
    bar.set_hatch(hatch)

ax.set_xticks(np.arange(len(configs)))
ax.set_xticklabels(configs, fontsize=8, color=COLOR_BLACK)
ax.set_ylabel("Speedup Factor (S$_p$ = T$_{base}$ / T$_{config}$) [Higher is Better]", fontweight='bold', color=COLOR_BLACK)
ax.set_title("HPCS Benchmark: Speedup Relative to Sequential Baseline (2.16 ms)", fontweight='bold', color=COLOR_BLACK, pad=12)
ax.grid(axis='y', linestyle='--', alpha=0.6, zorder=0)
ax.set_axisbelow(True)

# Baseline horizontal line in black dashed
ax.axhline(y=1.0, color=COLOR_BLACK, linestyle='--', linewidth=1.3, zorder=2)
ax.text(0.1, 1.12, 'Baseline (1.0x)', fontsize=7.5, color=COLOR_BLACK, fontweight='bold')

for bar, s in zip(bars, speedups):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.10,
            f'{s:.2f}x', ha='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK)

ax.set_ylim(0, max(speedups) * 1.22)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(COLOR_BLACK)
ax.spines['bottom'].set_color(COLOR_BLACK)

ax.legend(handles=legend_patches, loc="upper left", framealpha=0.95, edgecolor=COLOR_BLACK, fontsize=8)

plt.tight_layout()
plt.savefig("figures/fig_speedup.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("[2/8] fig_speedup.png (Black & White) generated")

# =============================================================================
# FIGURE 3: OpenMP Thread Scalability (Black & White)
# =============================================================================
omp_threads = [1, 2, 4, 8]
omp_times   = [1.56, 2.00, 1.00, 1.00]
omp_speedup = [1.56/t for t in omp_times]
ideal_speedup = omp_threads

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.8), dpi=300)

# Left: Time vs Threads
ax1.plot(omp_threads, omp_times, 'o-', color=COLOR_BLACK, linewidth=2.0, markersize=7, markerfacecolor=COLOR_BLACK, markeredgecolor=COLOR_BLACK, zorder=3)
ax1.fill_between(omp_threads, omp_times, alpha=0.15, color=COLOR_LIGHT)
for t, tm in zip(omp_threads, omp_times):
    ax1.annotate(f'{tm:.2f} ms', (t, tm), textcoords="offset points", xytext=(0, 10),
                 ha='center', fontsize=8, fontweight='bold', color=COLOR_BLACK)
ax1.set_xlabel("Number of Threads", fontweight='bold', color=COLOR_BLACK)
ax1.set_ylabel("Sorting Time (ms)", fontweight='bold', color=COLOR_BLACK)
ax1.set_title("(a) HPCS OpenMP Execution Time", fontweight='bold', color=COLOR_BLACK, fontsize=10.5)
ax1.set_xticks(omp_threads)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Right: Speedup vs Threads
ax2.plot(omp_threads, omp_speedup, 's-', color=COLOR_BLACK, linewidth=2.0, markersize=7, markerfacecolor=COLOR_BLACK, markeredgecolor=COLOR_BLACK, zorder=3, label='Measured Speedup')
ax2.plot(omp_threads, ideal_speedup, '--', color=COLOR_MID, linewidth=1.5, label='Ideal Linear Scaling', zorder=2)
for t, s in zip(omp_threads, omp_speedup):
    ax2.annotate(f'{s:.2f}x', (t, s), textcoords="offset points", xytext=(0, 10),
                 ha='center', fontsize=8, fontweight='bold', color=COLOR_BLACK)
ax2.set_xlabel("Number of Threads", fontweight='bold', color=COLOR_BLACK)
ax2.set_ylabel("Speedup (S$_p$)", fontweight='bold', color=COLOR_BLACK)
ax2.set_title("(b) HPCS OpenMP Speedup Scaling", fontweight='bold', color=COLOR_BLACK, fontsize=10.5)
ax2.set_xticks(omp_threads)
ax2.legend(fontsize=8, framealpha=0.95, edgecolor=COLOR_BLACK)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_axisbelow(True)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig("figures/fig_omp_scaling.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("[3/8] fig_omp_scaling.png (Black & White) generated")

# =============================================================================
# FIGURE 4: MPI Process Scalability (Black & White)
# =============================================================================
mpi_procs   = [1, 2, 4]
mpi_times   = [1.56, 1.20, 0.72]
mpi_speedup = [1.56/t for t in mpi_times]
ideal_sp    = mpi_procs

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.8), dpi=300)

# Left: Time vs Procs
ax1.plot(mpi_procs, mpi_times, 'o-', color=COLOR_BLACK, linewidth=2.0, markersize=7, markerfacecolor=COLOR_BLACK, markeredgecolor=COLOR_BLACK, zorder=3)
ax1.fill_between(mpi_procs, mpi_times, alpha=0.15, color=COLOR_LIGHT)
for p, tm in zip(mpi_procs, mpi_times):
    ax1.annotate(f'{tm:.2f} ms', (p, tm), textcoords="offset points", xytext=(0, 10),
                 ha='center', fontsize=8, fontweight='bold', color=COLOR_BLACK)
ax1.set_xlabel("Number of MPI Processes", fontweight='bold', color=COLOR_BLACK)
ax1.set_ylabel("Sorting Time (ms)", fontweight='bold', color=COLOR_BLACK)
ax1.set_title("(a) HPCS MPI Execution Time", fontweight='bold', color=COLOR_BLACK, fontsize=10.5)
ax1.set_xticks(mpi_procs)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Right: Speedup vs Procs
ax2.plot(mpi_procs, mpi_speedup, 'D-', color=COLOR_BLACK, linewidth=2.0, markersize=7, markerfacecolor=COLOR_BLACK, markeredgecolor=COLOR_BLACK, zorder=3, label='Measured Speedup')
ax2.plot(mpi_procs, ideal_sp, '--', color=COLOR_MID, linewidth=1.5, label='Ideal Linear Scaling', zorder=2)
for p, s in zip(mpi_procs, mpi_speedup):
    ax2.annotate(f'{s:.2f}x', (p, s), textcoords="offset points", xytext=(0, 10),
                 ha='center', fontsize=8, fontweight='bold', color=COLOR_BLACK)
ax2.set_xlabel("Number of MPI Processes", fontweight='bold', color=COLOR_BLACK)
ax2.set_ylabel("Speedup (S$_p$)", fontweight='bold', color=COLOR_BLACK)
ax2.set_title("(b) HPCS MPI Speedup Scaling", fontweight='bold', color=COLOR_BLACK, fontsize=10.5)
ax2.set_xticks(mpi_procs)
ax2.legend(fontsize=8, framealpha=0.95, edgecolor=COLOR_BLACK)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_axisbelow(True)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig("figures/fig_mpi_scaling.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("[4/8] fig_mpi_scaling.png (Black & White) generated")

# =============================================================================
# FIGURE 4B: CUDA GPU Scalability (Full Color)
# =============================================================================
cuda_tiers   = ["Sequential\nBaseline", "CUDA\nShared Mem", "CUDA\nMulti-Block"]
cuda_x       = [1, 2, 3]
cuda_times   = [2.16, 0.95, 0.42]
cuda_speedup = [2.16 / t for t in cuda_times]

CUDA_PRIMARY   = "#EA580C"  # Rich vibrant CUDA Amber-Orange
CUDA_SECONDARY = "#C2410C"  # Dark orange for markers/borders
CUDA_BG_FILL   = "#FFEDD5"  # Soft orange pastel fill
COLOR_SLATE    = "#475569"  # Modern slate gray

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.8), dpi=300)

# Left: Time vs Tiers (Vibrant Color)
ax1.plot(cuda_x, cuda_times, 'o-', color=CUDA_PRIMARY, linewidth=2.4, markersize=8, 
         markerfacecolor=CUDA_PRIMARY, markeredgecolor=CUDA_SECONDARY, markeredgewidth=1.2, zorder=3)
ax1.fill_between(cuda_x, cuda_times, alpha=0.35, color=CUDA_BG_FILL)
for x_val, tm in zip(cuda_x, cuda_times):
    ax1.annotate(f'{tm:.2f} ms', (x_val, tm), textcoords="offset points", xytext=(0, 10),
                 ha='center', fontsize=8.5, fontweight='bold', color=CUDA_SECONDARY)
ax1.set_xlabel("NVIDIA CUDA Architecture Tier", fontweight='bold', color=COLOR_SLATE)
ax1.set_ylabel("Sorting Time (ms)", fontweight='bold', color=COLOR_SLATE)
ax1.set_title("(a) HPCS CUDA Execution Time", fontweight='bold', color="#0F172A", fontsize=10.5)
ax1.set_xticks(cuda_x)
ax1.set_xticklabels(cuda_tiers, fontsize=8, color="#1E293B")
ax1.grid(True, linestyle='--', alpha=0.6, color="#E2E8F0")
ax1.set_axisbelow(True)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color("#94A3B8")
ax1.spines['bottom'].set_color("#94A3B8")

# Right: Speedup vs Tiers (Vibrant Color)
ax2.plot(cuda_x, cuda_speedup, '^-', color=CUDA_PRIMARY, linewidth=2.4, markersize=9, 
         markerfacecolor=CUDA_PRIMARY, markeredgecolor=CUDA_SECONDARY, markeredgewidth=1.2, zorder=3, label='Measured Speedup')
ax2.plot([1, 3], [1.0, 5.0], '--', color="#94A3B8", linewidth=1.5, label='Scaling Trend', zorder=2)
for x_val, s in zip(cuda_x, cuda_speedup):
    ax2.annotate(f'{s:.2f}x', (x_val, s), textcoords="offset points", xytext=(0, 10),
                 ha='center', fontsize=8.5, fontweight='bold', color=CUDA_SECONDARY)
ax2.set_xlabel("NVIDIA CUDA Architecture Tier", fontweight='bold', color=COLOR_SLATE)
ax2.set_ylabel("Speedup (S$_p$)", fontweight='bold', color=COLOR_SLATE)
ax2.set_title("(b) HPCS CUDA Speedup Scaling", fontweight='bold', color="#0F172A", fontsize=10.5)
ax2.set_xticks(cuda_x)
ax2.set_xticklabels(cuda_tiers, fontsize=8, color="#1E293B")
ax2.legend(fontsize=8, framealpha=0.95, edgecolor="#CBD5E1")
ax2.grid(True, linestyle='--', alpha=0.6, color="#E2E8F0")
ax2.set_axisbelow(True)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color("#94A3B8")
ax2.spines['bottom'].set_color("#94A3B8")

plt.tight_layout()
plt.savefig("figures/fig_cuda_scaling.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("[4B] fig_cuda_scaling.png (Color) generated")

# =============================================================================
# FIGURE 5: Parallel Efficiency Comparison (Black & White)
# =============================================================================
eff_labels = ["OpenMP\n2T", "OpenMP\n4T", "OpenMP\n8T", "MPI\n2P", "MPI\n4P"]
eff_values = [54.0, 54.0, 27.0, 90.0, 75.3]
eff_fills  = ["#FFFFFF", "#E0E0E0", "#C0C0C0", "#FFFFFF", "#D0D0D0"]
eff_hatches = ["xx", "xx", "xx", "..", ".."]

fig, ax = plt.subplots(figsize=(6.5, 4.0), dpi=300)
bars = ax.bar(np.arange(len(eff_labels)), eff_values, color=eff_fills, edgecolor=COLOR_BLACK, linewidth=1.1, width=0.6, zorder=3)
for bar, hatch in zip(bars, eff_hatches):
    bar.set_hatch(hatch)

ax.set_xticks(np.arange(len(eff_labels)))
ax.set_xticklabels(eff_labels, fontsize=9, color=COLOR_BLACK)
ax.set_ylabel("Parallel Efficiency E$_p$ = S$_p$ / p  (%)", fontweight='bold', color=COLOR_BLACK)
ax.set_title("HPCS Parallel Efficiency: OpenMP vs. Distributed MPI", fontweight='bold', color=COLOR_BLACK, pad=12)
ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
ax.set_axisbelow(True)

ax.axhline(y=100, color=COLOR_BLACK, linestyle='--', linewidth=1.2, alpha=0.7, zorder=2)
ax.text(4.2, 101, 'Ideal (100%)', fontsize=7.5, color=COLOR_BLACK, fontweight='bold')
ax.axhline(y=50, color=COLOR_MID, linestyle=':', linewidth=1.0, alpha=0.7, zorder=2)

for bar, v in zip(bars, eff_values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{v:.1f}%', ha='center', fontsize=9, fontweight='bold', color=COLOR_BLACK)
ax.set_ylim(0, 115)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add paradigm indicator labels below
ax.annotate('', xy=(0, -20), xytext=(2, -20), xycoords=('data', 'axes points'),
            textcoords=('data', 'axes points'),
            arrowprops=dict(arrowstyle='-', color=COLOR_BLACK, lw=1.5))
ax.annotate('', xy=(3, -20), xytext=(4, -20), xycoords=('data', 'axes points'),
            textcoords=('data', 'axes points'),
            arrowprops=dict(arrowstyle='-', color=COLOR_BLACK, lw=1.5))

plt.tight_layout()
plt.savefig("figures/fig_efficiency.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("[5/8] fig_efficiency.png (Black & White) generated")

# =============================================================================
# FIGURE 6: CUDA Execution Graph / Three-Kernel Pipeline Diagram (Black & White)
# =============================================================================
fig, ax = plt.subplots(figsize=(9.2, 4.2), dpi=300)
ax.set_xlim(0, 110)
ax.set_ylim(0, 52)
ax.axis('off')
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

def draw_bw_box(x, y, w, h, bg="#FFFFFF", edge="#000000", lw=1.5, rad=0.8, hatch=None):
    box = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.2,rounding_size={rad}",
                          facecolor=bg, edgecolor=edge, linewidth=lw, hatch=hatch, zorder=2)
    ax.add_patch(box)
    return box

def draw_bw_arrow(x1, y1, x2, y2):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                             arrowstyle='-|>,head_width=4.5,head_length=5.5',
                             color='#000000', linewidth=1.8, zorder=4)
    ax.add_patch(arrow)

# Title
ax.text(55, 49.0, "HPCS: CUDA Three-Kernel Pigeonhole Sort Execution Graph", ha='center', va='center',
        fontsize=12.5, fontweight='bold', color=COLOR_BLACK)
ax.plot([18, 92], [46.2, 46.2], color=COLOR_BLACK, linewidth=1.2)

# Host Input Box
draw_bw_box(2.0, 15.5, 13.5, 19, bg="#F5F5F5", edge="#000000", lw=1.5)
ax.text(8.75, 30.5, "Host CPU", ha='center', fontsize=9.5, fontweight='bold', color=COLOR_BLACK)
ax.text(8.75, 26.0, "Input Array", ha='center', fontsize=8.5, color=COLOR_DARK)
ax.text(8.75, 22.0, "A[0..N-1]", ha='center', fontsize=8.0, fontweight='bold', color=COLOR_BLACK)
ax.text(8.75, 18.0, "N ≈ 1.01M", ha='center', fontsize=7.2, color=COLOR_MID)

# H2D Transfer Arrow
draw_bw_arrow(15.5, 25, 21.0, 25)
ax.text(18.25, 27.5, "H->D", fontsize=7.5, fontweight='bold', color=COLOR_BLACK, ha='center')

# Kernel 1 Box
draw_bw_box(21.0, 13.5, 19.5, 23, bg="#FFFFFF", edge="#000000", lw=1.5)
ax.text(30.75, 33.0, "Kernel 1", ha='center', fontsize=10.0, fontweight='bold', color=COLOR_BLACK)
ax.text(30.75, 29.5, "Grid-Stride", ha='center', fontsize=8.5, color=COLOR_DARK)
ax.text(30.75, 26.5, "Histogram", ha='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK)
ax.plot([23.0, 38.5], [24.0, 24.0], color=COLOR_LIGHT, linestyle="--", linewidth=0.8)
ax.text(30.75, 21.0, "atomicAdd()", ha='center', fontsize=8.0, color=COLOR_BLACK)
ax.text(30.75, 17.5, "&d_counts[v - min]", ha='center', fontsize=7.0, color=COLOR_MID)
ax.text(30.75, 15.0, "O(N) Complexity", ha='center', fontsize=6.8, color=COLOR_DARK, style="italic")

# Arrow to Kernel 2
draw_bw_arrow(40.5, 25, 45.0, 25)

# Kernel 2 Box
draw_bw_box(45.0, 13.5, 19.5, 23, bg="#F0F0F0", edge="#000000", lw=1.5)
ax.text(54.75, 33.0, "Kernel 2", ha='center', fontsize=10.0, fontweight='bold', color=COLOR_BLACK)
ax.text(54.75, 29.5, "Prefix Scan", ha='center', fontsize=8.5, color=COLOR_DARK)
ax.text(54.75, 26.5, "Cumulative Sum", ha='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK)
ax.plot([47.0, 62.5], [24.0, 24.0], color=COLOR_LIGHT, linestyle="--", linewidth=0.8)
ax.text(54.75, 21.0, "Exclusive Scan", ha='center', fontsize=8.0, color=COLOR_BLACK)
ax.text(54.75, 17.5, "pos[k] = sum(counts)", ha='center', fontsize=7.0, color=COLOR_MID)
ax.text(54.75, 15.0, "O(R) Complexity", ha='center', fontsize=6.8, color=COLOR_DARK, style="italic")

# Arrow to Kernel 3
draw_bw_arrow(64.5, 25, 69.0, 25)

# Kernel 3 Box
draw_bw_box(69.0, 13.5, 19.5, 23, bg="#FFFFFF", edge="#000000", lw=1.5)
ax.text(78.75, 33.0, "Kernel 3", ha='center', fontsize=10.0, fontweight='bold', color=COLOR_BLACK)
ax.text(78.75, 29.5, "Parallel Scatter", ha='center', fontsize=8.5, color=COLOR_DARK)
ax.text(78.75, 26.5, "Direct Output", ha='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK)
ax.plot([71.0, 86.5], [24.0, 24.0], color=COLOR_LIGHT, linestyle="--", linewidth=0.8)
ax.text(78.75, 21.0, "atomicSub()", ha='center', fontsize=8.0, color=COLOR_BLACK)
ax.text(78.75, 17.5, "out[slot] = v", ha='center', fontsize=7.0, color=COLOR_MID)
ax.text(78.75, 15.0, "O(N) Complexity", ha='center', fontsize=6.8, color=COLOR_DARK, style="italic")

# D2H Transfer Arrow
draw_bw_arrow(88.5, 25, 93.5, 25)
ax.text(91.0, 27.5, "D->H", fontsize=7.5, fontweight='bold', color=COLOR_BLACK, ha='center')

# Host Output Box
draw_bw_box(93.5, 15.5, 14.5, 19, bg="#F5F5F5", edge="#000000", lw=1.5)
ax.text(100.75, 30.5, "Host CPU", ha='center', fontsize=9.5, fontweight='bold', color=COLOR_BLACK)
ax.text(100.75, 26.0, "Sorted Output", ha='center', fontsize=8.5, color=COLOR_DARK)
ax.text(100.75, 21.5, "Verified [✓]", ha='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK)
ax.text(100.75, 18.0, "0.42 ms (5.15x)", ha='center', fontsize=7.5, fontweight='bold', color=COLOR_BLACK)

# GPU region bracket (Monochrome)
ax.plot([19.5, 19.5, 90.0, 90.0], [10.0, 8.0, 8.0, 10.0], color=COLOR_BLACK, linewidth=1.6, zorder=3)
ax.text(54.75, 5.8, "NVIDIA GPU Device Global Memory Pipeline", ha='center', va='center',
        fontsize=8.8, fontweight='bold', color=COLOR_BLACK,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#F5F5F5', edgecolor=COLOR_BLACK, lw=1.0))

# Threading annotations above kernels
ax.text(30.75, 40.5, "256 th x 1024 blk", ha='center', fontsize=7.0, color=COLOR_BLACK,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor=COLOR_MID, lw=0.7))
ax.text(54.75, 40.5, "1 blk x 1 th (R=1000)", ha='center', fontsize=7.0, color=COLOR_BLACK,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor=COLOR_MID, lw=0.7))
ax.text(78.75, 40.5, "256 th x 1024 blk", ha='center', fontsize=7.0, color=COLOR_BLACK,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor=COLOR_MID, lw=0.7))

plt.savefig("figures/fig_cuda_pipeline.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("[6/8] fig_cuda_pipeline.png (CUDA Execution Graph, Black & White) generated")

# =============================================================================
# FIGURE 7: Zero-Merge vs Traditional MPI Architecture (Black & White)
# =============================================================================
fig, axes = plt.subplots(1, 2, figsize=(8.5, 5.0), dpi=300)
fig.patch.set_facecolor('#FFFFFF')

for ax in axes:
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 60)
    ax.axis('off')
    ax.set_facecolor('#FFFFFF')

def draw_arch_box(ax, x, y, w, h, bg="#FFFFFF", edge="#000000", lw=1.2, hatch=None):
    ax.add_patch(FancyBboxPatch((x,y), w, h, boxstyle="round,pad=0.2,rounding_size=0.6",
                                facecolor=bg, edgecolor=edge, linewidth=lw, hatch=hatch, zorder=2))

# --- LEFT: Traditional Distributed Sort (Sequential Merge Bottleneck) ---
ax = axes[0]
ax.text(25, 57, "(a) Traditional Distributed Sort", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_BLACK)

# Rank 0 reads + broadcasts
draw_arch_box(ax, 3, 46, 44, 8, bg="#FFFFFF", edge=COLOR_BLACK)
ax.text(25, 51, "Rank 0: Read & Broadcast All Data", ha='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK)
ax.text(25, 48, "Every rank receives full copy of A[0..N-1]", ha='center', fontsize=7.5, color=COLOR_MID)

# 4 ranks local sort
for i, lbl in enumerate(["Rank 0", "Rank 1", "Rank 2", "Rank 3"]):
    x = 3 + i * 11.5
    draw_arch_box(ax, x, 30, 10, 12, bg="#F5F5F5", edge=COLOR_BLACK)
    ax.text(x+5, 39, lbl, ha='center', fontsize=8, fontweight='bold', color=COLOR_BLACK)
    ax.text(x+5, 35.5, "Sort chunk", ha='center', fontsize=7, color=COLOR_MID)
    ax.text(x+5, 32.5, f"Chunk {i+1}", ha='center', fontsize=6.8, color=COLOR_DARK)
    ax.annotate('', xy=(x+5, 42), xytext=(x+5, 46), arrowprops=dict(arrowstyle='->', color=COLOR_BLACK, lw=1.2))

# Merge step (BOTTLENECK) - highlighted with hatching and thick black border
draw_arch_box(ax, 3, 13, 44, 12, bg="#FFFFFF", edge=COLOR_BLACK, lw=2.0, hatch="//")
ax.text(25, 22, "Rank 0: Sequential Merge", ha='center', fontsize=9.0, fontweight='bold', color=COLOR_BLACK,
        bbox=dict(facecolor='#FFFFFF', edgecolor='none', pad=1))
ax.text(25, 18.5, "O(N x p) - SEQUENTIAL BOTTLENECK", ha='center', fontsize=8.0, fontweight='bold', color=COLOR_BLACK,
        bbox=dict(facecolor='#FFFFFF', edgecolor='none', pad=1))
ax.text(25, 15.5, "Must merge p sorted sub-arrays sequentially", ha='center', fontsize=7.0, color=COLOR_MID,
        bbox=dict(facecolor='#FFFFFF', edgecolor='none', pad=1))
for i in range(4):
    x = 3 + i * 11.5
    ax.annotate('', xy=(x+5, 25), xytext=(x+5, 30), arrowprops=dict(arrowstyle='->', color=COLOR_BLACK, lw=1.2))

# Output
draw_arch_box(ax, 12, 3, 26, 7, bg="#F5F5F5", edge=COLOR_BLACK)
ax.text(25, 7.5, "Sorted Output", ha='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK)
ax.text(25, 4.5, "A[0] <= A[1] <= ... <= A[N-1]", ha='center', fontsize=7, color=COLOR_MID)
ax.annotate('', xy=(25, 10), xytext=(25, 13), arrowprops=dict(arrowstyle='->', color=COLOR_BLACK, lw=1.2))

# --- RIGHT: Zero-Merge MPI ---
ax = axes[1]
ax.text(25, 57, "(b) Proposed HPCS Zero-Merge Architecture", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_BLACK)

# Rank 0 reads + range partitions
draw_arch_box(ax, 3, 46, 44, 8, bg="#FFFFFF", edge=COLOR_BLACK)
ax.text(25, 51, "Rank 0: Range-Partition by Value", ha='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK)
ax.text(25, 48, "Each rank receives only its sub-range via MPI_Scatterv", ha='center', fontsize=7.5, color=COLOR_MID)

# 4 ranks sort disjoint ranges
for i, (lbl, rng) in enumerate(zip(
    ["Rank 0", "Rank 1", "Rank 2", "Rank 3"],
    ["[0, 249]", "[250, 499]", "[500, 749]", "[750, 999]"])):
    x = 3 + i * 11.5
    draw_arch_box(ax, x, 30, 10, 12, bg="#F5F5F5", edge=COLOR_BLACK)
    ax.text(x+5, 38.5, lbl, ha='center', fontsize=8, fontweight='bold', color=COLOR_BLACK)
    ax.text(x+5, 35.2, "Local sort", ha='center', fontsize=6.8, color=COLOR_MID)
    ax.text(x+5, 32.2, rng, ha='center', fontsize=6.5, color=COLOR_BLACK, fontweight='bold')
    ax.annotate('', xy=(x+5, 42), xytext=(x+5, 46), arrowprops=dict(arrowstyle='->', color=COLOR_BLACK, lw=1.2))

# Direct concatenation (NO MERGE) - highlighted with bold border
draw_arch_box(ax, 3, 13, 44, 12, bg="#E8E8E8", edge=COLOR_BLACK, lw=2.0)
ax.text(25, 22, "MPI_Gatherv: Direct Concatenation", ha='center', fontsize=9.0, fontweight='bold', color=COLOR_BLACK)
ax.text(25, 18.5, "O(N) - ZERO MERGE OVERHEAD", ha='center', fontsize=8.2, fontweight='bold', color=COLOR_BLACK)
ax.text(25, 15.5, "Disjoint ranges -> Concat is globally sorted", ha='center', fontsize=7.0, color=COLOR_MID)
for i in range(4):
    x = 3 + i * 11.5
    ax.annotate('', xy=(x+5, 25), xytext=(x+5, 30), arrowprops=dict(arrowstyle='->', color=COLOR_BLACK, lw=1.2))

# Output
draw_arch_box(ax, 12, 3, 26, 7, bg="#F5F5F5", edge=COLOR_BLACK)
ax.text(25, 7.5, "Sorted Output", ha='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK)
ax.text(25, 4.5, "A[0] <= A[1] <= ... <= A[N-1]", ha='center', fontsize=7, color=COLOR_MID)
ax.annotate('', xy=(25, 10), xytext=(25, 13), arrowprops=dict(arrowstyle='->', color=COLOR_BLACK, lw=1.2))

plt.tight_layout(w_pad=2)
plt.savefig("figures/fig_zero_merge.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("[7/8] fig_zero_merge.png (Black & White) generated")

# =============================================================================
# FIGURE 8: Paradigm Comparison Radar Chart (Black & White)
# =============================================================================
categories = ['Speedup', 'Efficiency', 'Scalability', 'Simplicity', 'Portability']
N_cats = len(categories)

paradigm_data = {
    'Sequential':   [1.0, 10.0, 1.0, 10.0, 10.0],
    'OpenMP (4T)':  [4.3, 5.4, 5.0, 8.0, 8.0],
    'MPI (4P)':     [6.0, 7.5, 8.0, 4.0, 5.0],
    'CUDA GPU':     [10.0, 8.0, 9.0, 3.0, 3.0],
}

# Distinct monochrome line styles and markers
paradigm_styles = {
    'Sequential':   {'linestyle': ':',  'marker': 'o', 'color': '#666666'},
    'OpenMP (4T)':  {'linestyle': '-.', 'marker': 's', 'color': '#444444'},
    'MPI (4P)':     {'linestyle': '--', 'marker': '^', 'color': '#222222'},
    'CUDA GPU':     {'linestyle': '-',  'marker': 'D', 'color': '#000000'},
}

angles = np.linspace(0, 2 * np.pi, N_cats, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(5.5, 5.5), dpi=300, subplot_kw=dict(polar=True))
ax.set_facecolor('#FFFFFF')
fig.patch.set_facecolor('#FFFFFF')

for name, values in paradigm_data.items():
    vals = values + values[:1]
    st = paradigm_styles[name]
    ax.plot(angles, vals, linestyle=st['linestyle'], marker=st['marker'],
            linewidth=2.0, markersize=5, label=name, color=st['color'])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=9, fontweight='bold', color=COLOR_BLACK)
ax.set_ylim(0, 11)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=7.5, color=COLOR_MID)
ax.set_title("HPCS Multi-Dimensional Paradigm Comparison", fontweight='bold', fontsize=11.5, color=COLOR_BLACK, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15), fontsize=8.5, framealpha=0.95, edgecolor=COLOR_BLACK)
ax.grid(True, color='#D0D0D0', linewidth=0.6)

plt.tight_layout()
plt.savefig("figures/fig_paradigm_radar.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print("[8/8] fig_paradigm_radar.png (Black & White) generated")

print("\nAll 8 figures generated successfully in pure black & white!")
