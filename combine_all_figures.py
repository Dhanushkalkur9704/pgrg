"""
Combine all Black & White HPCS figures into single consolidated files:
1. all_hpcs_figures_combined.png (Single image containing all figures stacked cleanly)
2. HPCS_All_Figures.pdf (Single multi-page PDF document containing all figures)
"""

import os
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

figures_dir = "figures"

figures_list = [
    {
        "file": "fig_pipeline.png",
        "title": "Figure 1: HPCS End-to-End System Execution Pipeline",
        "desc": "Sequential CPU, OpenMP Multi-Core, Distributed MPI (Zero-Merge), and CUDA Many-Core GPU."
    },
    {
        "file": "fig_zero_merge.png",
        "title": "Figure 2: MPI Architectural Comparison - Traditional vs. HPCS Zero-Merge",
        "desc": "Comparison of O(N * p) sequential merge bottleneck vs. O(N) direct concatenation."
    },
    {
        "file": "fig_cuda_pipeline.png",
        "title": "Figure 3: HPCS CUDA Three-Kernel Pigeonhole Sort Execution Graph",
        "desc": "Host-to-Device transfer, Grid-stride histogram, single-block prefix scan, and atomic scatter."
    },
    {
        "file": "fig_execution_time.png",
        "title": "Figure 4: Execution Time Comparison Across All Configurations",
        "desc": "Benchmark on N = 1,010,228 keys. Sequential baseline (2.16 ms) down to CUDA (0.42 ms)."
    },
    {
        "file": "fig_omp_scaling.png",
        "title": "Figure 5a: OpenMP Execution Time & Speedup Scaling",
        "desc": "Multi-threaded shared-memory scaling on 1, 2, 4, and 8 CPU threads."
    },
    {
        "file": "fig_mpi_scaling.png",
        "title": "Figure 5b: Distributed MPI Execution Time & Speedup Scaling",
        "desc": "Distributed-memory scaling across 1, 2, and 4 MPI processes with zero-merge."
    },
    {
        "file": "fig_cuda_scaling.png",
        "title": "Figure 5c: NVIDIA CUDA Execution Time & Speedup Scaling",
        "desc": "Many-core GPU scaling from Sequential Baseline to Shared-Memory (0.95 ms) and Scalable Multi-Block (0.42 ms)."
    },
    {
        "file": "fig_speedup.png",
        "title": "Figure 6: Speedup Relative to Sequential Baseline",
        "desc": "Speedup factors across all parallel execution configurations."
    },
    {
        "file": "fig_efficiency.png",
        "title": "Figure 7: Parallel Efficiency (Ep) Scaling",
        "desc": "Efficiency metrics comparing OpenMP multi-core vs. MPI distributed cluster."
    },
    {
        "file": "fig_paradigm_radar.png",
        "title": "Figure 8: Cross-Paradigm Trade-off Radar Chart",
        "desc": "Evaluating speedup, efficiency, scalability, simplicity, and portability."
    }
]

# =============================================================================
# 1. GENERATE MULTI-PAGE PDF (HPCS_All_Figures.pdf)
# =============================================================================
pdf_path = "HPCS_All_Figures.pdf"
print(f"Creating multi-page PDF: {pdf_path}...")

with PdfPages(pdf_path) as pdf:
    for idx, item in enumerate(figures_list):
        img_path = os.path.join(figures_dir, item["file"])
        if not os.path.exists(img_path):
            img_path = item["file"]
            
        img = Image.open(img_path)
        
        # Create a page in standard US Letter / A4 aspect
        fig, ax = plt.subplots(figsize=(8.5, 11), dpi=200)
        ax.set_axis_off()
        
        # Display image centered
        # Adjust extent to keep aspect ratio
        img_w, img_h = img.size
        aspect = img_h / img_w
        
        # Compute display dimensions
        display_w = 0.88
        display_h = display_w * aspect * (8.5 / 11)
        if display_h > 0.70:
            display_h = 0.70
            display_w = display_h / aspect * (11 / 8.5)
            
        x_left = (1.0 - display_w) / 2.0
        y_bottom = 0.45 - (display_h / 2.0)
        
        # Page header
        fig.text(0.5, 0.94, "HPCS: High-Performance Parallelization of Pigeonhole Sort", 
                 ha='center', fontsize=12, fontweight='bold', color='#111111')
        fig.text(0.5, 0.915, item["title"], 
                 ha='center', fontsize=11, fontweight='bold', color='#333333')
        
        # Inset axes for the image
        img_ax = fig.add_axes([x_left, y_bottom, display_w, display_h])
        img_ax.imshow(img)
        img_ax.set_axis_off()
        
        # Description at the bottom
        fig.text(0.5, y_bottom - 0.04, item["desc"], 
                 ha='center', fontsize=9.5, style='italic', color='#555555')
        
        # Page footer
        fig.text(0.5, 0.04, f"Page {idx+1} of {len(figures_list)}  |  HPCS Academic Report Figures", 
                 ha='center', fontsize=8.5, color='#888888')
        
        pdf.savefig(fig, facecolor='white')
        plt.close(fig)

print("HPCS_All_Figures.pdf created successfully.")

# =============================================================================
# 2. GENERATE SINGLE COMPOSITE IMAGE (all_hpcs_figures_combined.png)
# =============================================================================
png_path = "all_hpcs_figures_combined.png"
print(f"Creating combined single image: {png_path}...")

# Target width for all panels
TARGET_WIDTH = 2400

processed_images = []
for item in figures_list:
    img_path = os.path.join(figures_dir, item["file"])
    if not os.path.exists(img_path):
        img_path = item["file"]
    
    img = Image.open(img_path).convert("RGB")
    
    # Calculate new height maintaining aspect ratio
    w, h = img.size
    scale = (TARGET_WIDTH - 80) / w
    new_w = int(w * scale)
    new_h = int(h * scale)
    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Add a border / canvas around image
    panel = Image.new("RGB", (TARGET_WIDTH, new_h + 80), "white")
    x_offset = (TARGET_WIDTH - new_w) // 2
    panel.paste(img_resized, (x_offset, 40))
    processed_images.append(panel)

# Compute total height including top title and dividers
total_height = sum(p.size[1] for p in processed_images) + 180

combined_img = Image.new("RGB", (TARGET_WIDTH, total_height), "white")

# Paste panels
current_y = 120
for p in processed_images:
    combined_img.paste(p, (0, current_y))
    current_y += p.size[1]

# Save optimized single image
combined_img.save(png_path, "PNG", optimize=True)
print(f"all_hpcs_figures_combined.png created successfully ({TARGET_WIDTH}x{total_height} px).")
