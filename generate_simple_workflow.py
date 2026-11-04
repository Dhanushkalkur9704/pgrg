"""
Black and White Publication Workflow Diagram Generator
High-Performance Computing Systems (HPCS)
Topic: Parallelization of Pigeonhole Sort across CPU, OpenMP, MPI, and CUDA
Strictly Black and White (Grayscale) for IEEE Transactions / Conference Printing
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

def generate_simple_diagram(output_png="simple_workflow_diagram.png",
                            output_pdf="simple_workflow_diagram.pdf"):
    os.makedirs("figures", exist_ok=True)
    # Figure size: clean wide canvas with ample margins
    fig, ax = plt.subplots(figsize=(16.0, 7.0), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 52)
    ax.axis("off")

    def draw_card(x, y, w, h, bg="#FFFFFF", edge="#000000", rad=1.0, lw=1.5, hatch=None):
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle=f"round,pad=0.2,rounding_size={rad}",
                             facecolor=bg, edgecolor=edge, linewidth=lw, hatch=hatch, zorder=2)
        ax.add_patch(box)
        return box

    def draw_arrow(x1, y1, x2, y2, color="#000000", lw=2.0):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                arrowstyle="-|>,head_width=4.5,head_length=6.0",
                                color=color, linewidth=lw, zorder=3)
        ax.add_patch(arrow)

    # -------------------------------------------------------------
    # 0. HPCS TITLE WITH UNDERLINE (Pure Black / Monochrome)
    # -------------------------------------------------------------
    ax.text(55.0, 49.0, "HPCS: Pigeonhole Sort High-Performance Parallelization Pipeline",
            ha="center", va="center", fontsize=14.5, fontweight="bold", color="#000000")
    ax.text(55.0, 46.5, "High-Performance Computing Systems (HPCS) Architectural Execution Framework",
            ha="center", va="center", fontsize=9.2, color="#333333", style="italic")
    ax.plot([18.0, 92.0], [44.5, 44.5], color="#000000", linewidth=1.4, zorder=3)

    # -------------------------------------------------------------
    # 1. INPUT DATASET CARD (Left)
    # -------------------------------------------------------------
    draw_card(2.0, 12.0, 18.5, 25.5, bg="#F5F5F5", edge="#000000", lw=1.8)
    ax.text(11.25, 33.2, "Input Dataset", ha="center", va="center", fontsize=11.5, fontweight="bold", color="#000000")
    ax.text(11.25, 27.8, "T10I4D100K.dat.txt\nN ≈ 1,010,228 Integers", ha="center", va="center", fontsize=9.0, color="#000000")
    ax.plot([3.5, 19.0], [21.5, 21.5], color="#666666", linestyle="--", linewidth=1.2, zorder=3)
    ax.text(11.25, 16.5, "HPCS Dynamic Range:\n[0, 999] (R = 1000)", ha="center", va="center", fontsize=8.8, color="#000000", fontweight="bold")

    # Connect Input to Branching Bus
    ax.plot([20.5, 24.0], [24.75, 24.75], color="#000000", linewidth=2.0)
    ax.plot([24.0, 24.0], [39.75, 8.25], color="#000000", linewidth=2.0)

    # -------------------------------------------------------------
    # 2. HPCS PARALLEL PARADIGMS (4 Clean Branch Cards - Monochromatic)
    # -------------------------------------------------------------
    engines = [
        {"name": "1. Sequential CPU Baseline", "desc": "Hardened Heap calloc (Unsafe Stack VLA Replaced)", "time": "1.56 ms (1.38x)", "bg": "#FFFFFF", "edge": "#000000", "y": 35.5},
        {"name": "2. OpenMP Multi-Core", "desc": "Thread-Local Histograms & Lock-Free Reduction", "time": "1.00 ms (2.16x)", "bg": "#F5F5F5", "edge": "#000000", "y": 25.0},
        {"name": "3. Distributed MPI (Zero-Merge)", "desc": "Disjoint Range Partitioning & Direct Concat", "time": "0.72 ms (3.01x)", "bg": "#EBEBEB", "edge": "#000000", "y": 14.5},
        {"name": "4. NVIDIA CUDA Many-Core GPU", "desc": "Grid-Stride Atomics & Three-Kernel Pipeline", "time": "0.42 ms (5.15x)", "bg": "#E0E0E0", "edge": "#000000", "y": 4.0},
    ]

    card_w = 37.5
    card_h = 8.5
    for eng in engines:
        draw_arrow(24.0, eng["y"] + card_h/2, 27.5, eng["y"] + card_h/2, color="#000000")
        draw_card(27.5, eng["y"], card_w, card_h, bg=eng["bg"], edge=eng["edge"], lw=1.5)
        ax.text(29.2, eng["y"] + 5.5, eng["name"], fontsize=10.5, fontweight="bold", color="#000000", va="center")
        ax.text(29.2, eng["y"] + 2.5, eng["desc"], fontsize=8.5, color="#333333", va="center")
        ax.text(63.2, eng["y"] + 5.5, eng["time"], fontsize=9.0, fontweight="bold", color="#000000", ha="right", va="center")

        ax.plot([65.0, 68.0], [eng["y"] + card_h/2, eng["y"] + card_h/2], color="#000000", linewidth=2.0)

    # Collector Bus
    ax.plot([68.0, 68.0], [39.75, 8.25], color="#000000", linewidth=2.0)
    draw_arrow(68.0, 24.75, 71.5, 24.75, color="#000000")

    # -------------------------------------------------------------
    # 3. VERIFICATION (Middle-Right)
    # -------------------------------------------------------------
    draw_card(71.5, 12.0, 15.5, 25.5, bg="#F5F5F5", edge="#000000", lw=1.8)
    ax.text(79.25, 32.5, "Sort Verification", ha="center", va="center", fontsize=11.5, fontweight="bold", color="#000000")
    ax.text(79.25, 25.0, "Strict Assertion:\nA[i] <= A[i + 1]\nfor all i in [0, N - 2]", ha="center", va="center", fontsize=8.8, color="#222222")
    ax.plot([73.0, 85.5], [19.0, 19.0], color="#666666", linestyle="--", linewidth=1.0, zorder=3)
    ax.text(79.25, 15.0, "HPCS Status:\nPASSED [✓]", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#000000")

    draw_arrow(87.0, 24.75, 90.5, 24.75, color="#000000")

    # -------------------------------------------------------------
    # 4. PERFORMANCE EVALUATION (Right)
    # -------------------------------------------------------------
    draw_card(90.5, 12.0, 17.5, 25.5, bg="#FFFFFF", edge="#000000", lw=1.8)
    ax.text(99.25, 32.5, "HPCS Performance", ha="center", va="center", fontsize=11.0, fontweight="bold", color="#000000")
    ax.text(92.0, 24.5, "- Sorting Time (ms)\n- Speedup Factor (Sp)\n- Parallel Efficiency (Ep)\n- Multi-Core Scalability", ha="left", va="center", fontsize=8.2, color="#222222")
    ax.plot([92.0, 106.5], [18.0, 18.0], color="#666666", linestyle="--", linewidth=1.0, zorder=3)
    ax.text(99.25, 14.5, "HPCS Benchmark Metrics", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#000000")

    plt.savefig(output_png, dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.savefig(output_pdf, bbox_inches="tight", facecolor="#FFFFFF")
    plt.savefig("figures/fig_pipeline.png", dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.savefig("ieee_workflow_simple.png", dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.savefig("workflow_diagram.png", dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.savefig("workflow.png", dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
    plt.close()
    print("HPCS Black and white workflow diagram regenerated successfully!")

if __name__ == "__main__":
    generate_simple_diagram()
