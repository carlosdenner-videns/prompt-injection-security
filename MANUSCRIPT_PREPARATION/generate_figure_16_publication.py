#!/usr/bin/env python3
"""
Figure 16: System Architecture - Publication-Ready Design
Comprehensive diagram with proper spacing and visual hierarchy
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import matplotlib.lines as mlines
import numpy as np
from pathlib import Path

fig = plt.figure(figsize=(16, 11))
ax = fig.add_subplot(111)
ax.set_xlim(0, 16)
ax.set_ylim(0, 11)
ax.axis('off')

# ============================================================================
# TITLE
# ============================================================================
ax.text(8, 10.6, 'Prompt Injection Detection Pipeline Architecture', 
        ha='center', fontsize=16, fontweight='bold')
ax.text(8, 10.15, 'Input-Side Detection Before LLM Processing', 
        ha='center', fontsize=11, style='italic', color='#555')

# ============================================================================
# COLOR SCHEME
# ============================================================================
color_input = '#E3F2FD'
color_normalizer = '#C8E6C9'
color_detector = '#64B5F6'
color_fusion = '#2196F3'
color_decision = '#D32F2F'
color_llm = '#FFF9C4'
color_example = '#FFE0B2'
color_metrics = '#F5F5F5'
color_border = '#333'

# ============================================================================
# SECTION 1: MAIN PIPELINE (Top)
# ============================================================================
y_pipeline = 8.5

# INPUT
input_box = FancyBboxPatch((0.5, y_pipeline - 0.5), 1.2, 0.8, boxstyle="round,pad=0.08",
                           edgecolor=color_border, facecolor=color_input, linewidth=2)
ax.add_patch(input_box)
ax.text(1.1, y_pipeline - 0.1, 'INPUT\nQuery', ha='center', va='center', 
        fontsize=9, fontweight='bold')

# Arrow to Normalizer
arrow1 = FancyArrowPatch((1.7, y_pipeline - 0.1), (2.5, y_pipeline - 0.1), 
                         arrowstyle='->', mutation_scale=25, linewidth=2.5, color=color_border)
ax.add_patch(arrow1)

# NORMALIZER (Recommended)
norm_box = FancyBboxPatch((2.5, y_pipeline - 0.5), 1.4, 0.8, boxstyle="round,pad=0.08",
                          edgecolor='#2E7D32', facecolor=color_normalizer, linewidth=2.5)
ax.add_patch(norm_box)
ax.text(3.2, y_pipeline - 0.1, 'Normalizer\nUnicode Fix', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='#1B5E20')

# Arrow to Detectors
arrow2 = FancyArrowPatch((3.9, y_pipeline - 0.1), (4.7, y_pipeline - 0.1), 
                         arrowstyle='->', mutation_scale=25, linewidth=2.5, color=color_border)
ax.add_patch(arrow2)

# DETECTOR v1 (Signature)
det1_box = FancyBboxPatch((4.7, y_pipeline + 0.4), 1.3, 0.7, boxstyle="round,pad=0.06",
                          edgecolor='#1565C0', facecolor=color_detector, linewidth=2)
ax.add_patch(det1_box)
ax.text(5.35, y_pipeline + 0.75, 'Signature\nDetector (v1)', ha='center', va='center', 
        fontsize=8, fontweight='bold', color='white')

# DETECTOR v2 (Heuristic)
det2_box = FancyBboxPatch((4.7, y_pipeline - 0.1), 1.3, 0.7, boxstyle="round,pad=0.06",
                          edgecolor='#1565C0', facecolor=color_detector, linewidth=2)
ax.add_patch(det2_box)
ax.text(5.35, y_pipeline + 0.25, 'Heuristic\nDetector (v2)', ha='center', va='center', 
        fontsize=8, fontweight='bold', color='white')

# DETECTOR v3 (Semantic)
det3_box = FancyBboxPatch((4.7, y_pipeline - 0.6), 1.3, 0.7, boxstyle="round,pad=0.06",
                          edgecolor='#1565C0', facecolor=color_detector, linewidth=2)
ax.add_patch(det3_box)
ax.text(5.35, y_pipeline - 0.25, 'Semantic\nDetector (v3)', ha='center', va='center', 
        fontsize=8, fontweight='bold', color='white')

# Arrows from detectors to fusion
arrow_d1 = FancyArrowPatch((6.0, y_pipeline + 0.75), (6.5, y_pipeline + 0.15), 
                           arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#666')
ax.add_patch(arrow_d1)
arrow_d2 = FancyArrowPatch((6.0, y_pipeline + 0.25), (6.5, y_pipeline + 0.15), 
                           arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#666')
ax.add_patch(arrow_d2)
arrow_d3 = FancyArrowPatch((6.0, y_pipeline - 0.25), (6.5, y_pipeline + 0.15), 
                           arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#666')
ax.add_patch(arrow_d3)

# FUSION (OR Logic)
fusion_box = FancyBboxPatch((6.5, y_pipeline - 0.35), 1.5, 1.0, boxstyle="round,pad=0.08",
                            edgecolor='#0D47A1', facecolor=color_fusion, linewidth=2.5)
ax.add_patch(fusion_box)
ax.text(7.25, y_pipeline + 0.15, 'Fusion\nOR Logic\n(v1+v3)', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='white')

# Arrow to Decision
arrow3 = FancyArrowPatch((8.0, y_pipeline + 0.15), (9.0, y_pipeline + 0.15), 
                         arrowstyle='->', mutation_scale=25, linewidth=2.5, color=color_border)
ax.add_patch(arrow3)

# DECISION
decision_box = FancyBboxPatch((9.0, y_pipeline - 0.35), 1.3, 1.0, boxstyle="round,pad=0.08",
                              edgecolor='#B71C1C', facecolor=color_decision, linewidth=2.5)
ax.add_patch(decision_box)
ax.text(9.65, y_pipeline + 0.15, 'DECISION\nAttack/Benign', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='white')

# Arrow BLOCKED (downward)
arrow_blocked = FancyArrowPatch((9.65, y_pipeline - 0.35), (9.65, y_pipeline - 1.0), 
                                arrowstyle='->', mutation_scale=25, linewidth=2.5, 
                                color='#B71C1C', linestyle='--')
ax.add_patch(arrow_blocked)
ax.text(10.1, y_pipeline - 0.65, 'BLOCKED', ha='left', fontsize=8, fontweight='bold', 
        color='#B71C1C')

# Arrow ALLOWED (rightward)
arrow_allowed = FancyArrowPatch((10.3, y_pipeline + 0.15), (11.3, y_pipeline + 0.15), 
                                arrowstyle='->', mutation_scale=25, linewidth=2.5, 
                                color='#2E7D32')
ax.add_patch(arrow_allowed)
ax.text(10.8, y_pipeline + 0.45, 'ALLOWED', ha='center', fontsize=8, fontweight='bold', 
        color='#2E7D32')

# LLM PROCESSING
llm_box = FancyBboxPatch((11.3, y_pipeline - 0.35), 1.3, 1.0, boxstyle="round,pad=0.08",
                         edgecolor='#F57F17', facecolor=color_llm, linewidth=2.5)
ax.add_patch(llm_box)
ax.text(11.95, y_pipeline + 0.15, 'LLM\nProcessing', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='#F57F17')

# ============================================================================
# SECTION 2: EXAMPLE ATTACK FLOW
# ============================================================================
y_example = 6.5

example_box = FancyBboxPatch((0.3, y_example - 1.8), 15.4, 1.8, boxstyle="round,pad=0.1",
                             edgecolor='#E65100', facecolor=color_example, linewidth=2, linestyle='--')
ax.add_patch(example_box)
ax.text(0.6, y_example + 0.5, 'Example: Attack Processing Flow', fontsize=10, fontweight='bold', 
        color='#E65100')

# Example input
ex_input = FancyBboxPatch((0.5, y_example - 1.3), 2.5, 0.7, boxstyle="round,pad=0.06",
                          edgecolor='#1565C0', facecolor=color_input, linewidth=1.5)
ax.add_patch(ex_input)
ax.text(1.75, y_example - 0.95, 'Input:\n"Ignore previous\ninstructions..."', ha='center', va='center', 
        fontsize=7.5, family='monospace')

# Arrow
arrow_ex1 = FancyArrowPatch((3.0, y_example - 0.95), (3.6, y_example - 0.95), 
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#E65100')
ax.add_patch(arrow_ex1)

# Normalizer step
ex_norm = FancyBboxPatch((3.6, y_example - 1.3), 2.0, 0.7, boxstyle="round,pad=0.06",
                         edgecolor='#2E7D32', facecolor=color_normalizer, linewidth=1.5)
ax.add_patch(ex_norm)
ax.text(4.6, y_example - 0.95, 'Normalizer:\nCleans unicode', ha='center', va='center', 
        fontsize=7.5, family='monospace')

# Arrow
arrow_ex2 = FancyArrowPatch((5.6, y_example - 0.95), (6.2, y_example - 0.95), 
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#E65100')
ax.add_patch(arrow_ex2)

# v1 Detection
ex_v1 = FancyBboxPatch((6.2, y_example - 1.3), 2.0, 0.7, boxstyle="round,pad=0.06",
                       edgecolor='#1565C0', facecolor=color_detector, linewidth=1.5)
ax.add_patch(ex_v1)
ax.text(7.2, y_example - 0.95, 'v1 Signature:\nMatches keyword', ha='center', va='center', 
        fontsize=7.5, family='monospace', color='white', fontweight='bold')

# Arrow
arrow_ex3 = FancyArrowPatch((8.2, y_example - 0.95), (8.8, y_example - 0.95), 
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#E65100')
ax.add_patch(arrow_ex3)

# Decision
ex_decision = FancyBboxPatch((8.8, y_example - 1.3), 2.0, 0.7, boxstyle="round,pad=0.06",
                             edgecolor='#B71C1C', facecolor=color_decision, linewidth=1.5)
ax.add_patch(ex_decision)
ax.text(9.8, y_example - 0.95, 'Decision:\nBLOCKED', ha='center', va='center', 
        fontsize=7.5, family='monospace', color='white', fontweight='bold')

# Performance metrics
ax.text(0.5, y_example - 1.65, 'Performance: 87% TPR on known attacks  |  0.77% FAR on benign  |  <0.1ms latency', 
        fontsize=8, style='italic', color='#E65100', fontweight='bold')

# ============================================================================
# SECTION 3: METRICS & SPECIFICATIONS (Two columns)
# ============================================================================
y_metrics = 4.2

# Left column: Production Configuration
metrics_box_left = FancyBboxPatch((0.3, y_metrics - 1.8), 7.3, 1.8, boxstyle="round,pad=0.1",
                                  edgecolor=color_border, facecolor=color_metrics, linewidth=2)
ax.add_patch(metrics_box_left)
ax.text(3.95, y_metrics + 0.5, 'Production Configuration: Normalizer + v3', 
        fontsize=9, fontweight='bold', color='#0D47A1')

metrics_text_left = """True Positive Rate (TPR): 87% on known attacks
False Alarm Rate (FAR): 0.77% on obfuscated benign
Latency: <0.1ms per sample (CPU-only)
Complexity: ~1,200 lines of code
Deployment: Stateless, parallelizable
Dependencies: None (pure Python)"""

ax.text(0.6, y_metrics + 0.15, metrics_text_left, fontsize=7.5, family='monospace', 
        verticalalignment='top')

# Right column: Component Specifications
metrics_box_right = FancyBboxPatch((8.4, y_metrics - 1.8), 7.3, 1.8, boxstyle="round,pad=0.1",
                                   edgecolor=color_border, facecolor=color_metrics, linewidth=2)
ax.add_patch(metrics_box_right)
ax.text(12.05, y_metrics + 0.5, 'Component Specifications', fontsize=9, fontweight='bold', 
        color='#0D47A1')

details_text = """Signature Detector (v1): Keyword matching
  • 80% TPR, 0% FAR on Phase 1 attacks
  • Catches: plain, delimiter, role confusion

Semantic Detector (v3): Pattern analysis
  • 57% TPR, 0% FAR on Phase 1 attacks
  • Catches: formatting, semantic anomalies

Fusion (OR Logic): v1 OR v3
  • Combined: 87% TPR, 0% FAR"""

ax.text(8.7, y_metrics + 0.15, details_text, fontsize=7.5, family='monospace', 
        verticalalignment='top')

# ============================================================================
# SECTION 4: KEY DESIGN PRINCIPLES (Bottom)
# ============================================================================
y_principles = 1.8

principles_box = FancyBboxPatch((0.3, y_principles - 1.5), 15.4, 1.5, boxstyle="round,pad=0.1",
                                edgecolor='#0D47A1', facecolor='#E3F2FD', linewidth=2.5)
ax.add_patch(principles_box)
ax.text(8, y_principles + 0.7, 'Key Design Principles', fontsize=10, fontweight='bold', 
        color='#0D47A1', ha='center')

principles_text = """1. INPUT-SIDE DETECTION: Attacks blocked BEFORE reaching the LLM, preventing prompt injection at the source
2. NORMALIZER FIRST: Unicode/homoglyph normalization ensures consistent detection across obfuscation techniques
3. COMPLEMENTARY DETECTORS: v1 (signature) + v3 (semantic) catch different attack patterns through OR fusion
4. THRESHOLD-INVARIANT: Binary OR logic eliminates threshold tuning complexity in deployment
5. PRODUCTION-READY: <0.1ms latency, CPU-only, no external dependencies, stateless architecture"""

ax.text(0.6, y_principles + 0.3, principles_text, fontsize=7.5, verticalalignment='top')

# ============================================================================
# LEGEND
# ============================================================================
legend_y = 0.15
ax.text(0.3, legend_y, 'Legend:', fontsize=8, fontweight='bold')

colors_legend = [
    (color_input, 'Input'),
    (color_normalizer, 'Normalizer'),
    (color_detector, 'Detector'),
    (color_fusion, 'Fusion'),
    (color_decision, 'Decision'),
    (color_llm, 'LLM'),
]

legend_x = 1.2
for i, (color, label) in enumerate(colors_legend):
    rect = Rectangle((legend_x + i*2.0, legend_y - 0.08), 0.12, 0.08, 
                     facecolor=color, edgecolor=color_border, linewidth=1)
    ax.add_patch(rect)
    ax.text(legend_x + i*2.0 + 0.2, legend_y - 0.04, label, fontsize=7, va='center')

plt.tight_layout()
# Save both PNG and PDF
output_path_png = Path(__file__).parent / 'GENERATED_FIGURES' / 'figure_16_system_architecture.png'
output_path_pdf = Path(__file__).parent / 'fig16_architecture.pdf'
plt.savefig(str(output_path_png), dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.savefig(str(output_path_pdf), dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print("✓ Figure 16 (Publication-Ready) generated successfully!")
print(f"  PNG: {output_path_png}")
print(f"  PDF: {output_path_pdf}")
print("\nImprovements:")
print("  ✓ Proper spacing and visual hierarchy")
print("  ✓ Clear separation of sections")
print("  ✓ No overlapping text")
print("  ✓ Larger figure size (16x11 inches)")
print("  ✓ Better readability")
print("  ✓ Professional layout")
