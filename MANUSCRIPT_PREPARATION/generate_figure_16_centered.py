#!/usr/bin/env python3
"""
Figure 16: System Architecture - Centered Layout
Upper pipeline and example box centered on page
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import matplotlib.lines as mlines
import numpy as np
from pathlib import Path

fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# ============================================================================
# TITLE
# ============================================================================
ax.text(8, 11.5, 'Prompt Injection Detection Pipeline Architecture', 
        ha='center', fontsize=16, fontweight='bold')
ax.text(8, 11.0, 'Input-Side Detection Before LLM Processing', 
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
# SECTION 1: MAIN PIPELINE (Top) - CENTERED
# ============================================================================
y_pipeline = 9.8

# Calculate center position for the pipeline
# Total width needed: input(1.4) + arrow(0.8) + normalizer(1.6) + arrow(0.8) + detectors(1.3) + 
#                    arrows(1.0) + fusion(1.6) + arrow(0.8) + decision(1.5) + arrow(0.8) + llm(1.5)
# Total ≈ 14.1, so we start at (16-14.1)/2 = 0.95, but let's center better

# Center the entire pipeline horizontally
pipeline_start_x = 1.0  # Left margin for centering

# INPUT
input_box = FancyBboxPatch((pipeline_start_x, y_pipeline - 0.6), 1.4, 0.9, boxstyle="round,pad=0.08",
                           edgecolor=color_border, facecolor=color_input, linewidth=2)
ax.add_patch(input_box)
ax.text(pipeline_start_x + 0.7, y_pipeline - 0.05, 'INPUT', ha='center', va='center', 
        fontsize=9, fontweight='bold')
ax.text(pipeline_start_x + 0.7, y_pipeline - 0.35, 'Query', ha='center', va='center', 
        fontsize=8)

# Arrow to Normalizer
arrow1 = FancyArrowPatch((pipeline_start_x + 1.4, y_pipeline - 0.05), (pipeline_start_x + 2.2, y_pipeline - 0.05), 
                         arrowstyle='->', mutation_scale=25, linewidth=2.5, color=color_border)
ax.add_patch(arrow1)

# NORMALIZER
norm_box = FancyBboxPatch((pipeline_start_x + 2.2, y_pipeline - 0.6), 1.6, 0.9, boxstyle="round,pad=0.08",
                          edgecolor='#2E7D32', facecolor=color_normalizer, linewidth=2.5)
ax.add_patch(norm_box)
ax.text(pipeline_start_x + 3.0, y_pipeline - 0.05, 'Normalizer', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='#1B5E20')
ax.text(pipeline_start_x + 3.0, y_pipeline - 0.35, 'Unicode Fix', ha='center', va='center', 
        fontsize=8, color='#1B5E20')

# Arrow to Detectors
arrow2 = FancyArrowPatch((pipeline_start_x + 3.8, y_pipeline - 0.05), (pipeline_start_x + 4.5, y_pipeline - 0.05), 
                         arrowstyle='->', mutation_scale=25, linewidth=2.5, color=color_border)
ax.add_patch(arrow2)

# ============================================================================
# THREE SEPARATE DETECTOR BOXES (Properly Aligned)
# ============================================================================
detector_width = 1.3
detector_height = 0.65
detector_x_start = pipeline_start_x + 4.5

# DETECTOR v1 (Signature) - TOP
det1_y = y_pipeline + 0.5
det1_box = FancyBboxPatch((detector_x_start, det1_y - detector_height), detector_width, detector_height, 
                          boxstyle="round,pad=0.06", edgecolor='#1565C0', facecolor=color_detector, linewidth=2)
ax.add_patch(det1_box)
ax.text(detector_x_start + detector_width/2, det1_y - detector_height/2, 'Signature\nDetector (v1)', 
        ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# DETECTOR v2 (Heuristic) - MIDDLE
det2_y = y_pipeline - 0.05
det2_box = FancyBboxPatch((detector_x_start, det2_y - detector_height), detector_width, detector_height, 
                          boxstyle="round,pad=0.06", edgecolor='#1565C0', facecolor=color_detector, linewidth=2)
ax.add_patch(det2_box)
ax.text(detector_x_start + detector_width/2, det2_y - detector_height/2, 'Heuristic\nDetector (v2)', 
        ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# DETECTOR v3 (Semantic) - BOTTOM
det3_y = y_pipeline - 0.6
det3_box = FancyBboxPatch((detector_x_start, det3_y - detector_height), detector_width, detector_height, 
                          boxstyle="round,pad=0.06", edgecolor='#1565C0', facecolor=color_detector, linewidth=2)
ax.add_patch(det3_box)
ax.text(detector_x_start + detector_width/2, det3_y - detector_height/2, 'Semantic\nDetector (v3)', 
        ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# ============================================================================
# ARROWS FROM DETECTORS TO FUSION
# ============================================================================
fusion_x = pipeline_start_x + 6.3
fusion_y = y_pipeline - 0.05

# Arrow from v1 to fusion
arrow_d1 = FancyArrowPatch((detector_x_start + detector_width, det1_y - detector_height/2), 
                           (fusion_x, fusion_y), 
                           arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#666')
ax.add_patch(arrow_d1)

# Arrow from v2 to fusion
arrow_d2 = FancyArrowPatch((detector_x_start + detector_width, det2_y - detector_height/2), 
                           (fusion_x, fusion_y), 
                           arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#666')
ax.add_patch(arrow_d2)

# Arrow from v3 to fusion
arrow_d3 = FancyArrowPatch((detector_x_start + detector_width, det3_y - detector_height/2), 
                           (fusion_x, fusion_y), 
                           arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#666')
ax.add_patch(arrow_d3)

# ============================================================================
# FUSION (OR Logic)
# ============================================================================
fusion_box = FancyBboxPatch((fusion_x, fusion_y - 0.45), 1.6, 1.0, boxstyle="round,pad=0.08",
                            edgecolor='#0D47A1', facecolor=color_fusion, linewidth=2.5)
ax.add_patch(fusion_box)
ax.text(fusion_x + 0.8, fusion_y + 0.15, 'Fusion', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='white')
ax.text(fusion_x + 0.8, fusion_y - 0.15, 'OR Logic', ha='center', va='center', 
        fontsize=8, color='white')
ax.text(fusion_x + 0.8, fusion_y - 0.35, '(v1+v3)', ha='center', va='center', 
        fontsize=7.5, color='white')

# Arrow to Decision
arrow3 = FancyArrowPatch((fusion_x + 1.6, fusion_y), (fusion_x + 2.4, fusion_y), 
                         arrowstyle='->', mutation_scale=25, linewidth=2.5, color=color_border)
ax.add_patch(arrow3)

# ============================================================================
# DECISION
# ============================================================================
decision_x = fusion_x + 2.4
decision_box = FancyBboxPatch((decision_x, fusion_y - 0.45), 1.5, 1.0, boxstyle="round,pad=0.08",
                              edgecolor='#B71C1C', facecolor=color_decision, linewidth=2.5)
ax.add_patch(decision_box)
ax.text(decision_x + 0.75, fusion_y + 0.15, 'DECISION', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='white')
ax.text(decision_x + 0.75, fusion_y - 0.15, 'Attack/Benign', ha='center', va='center', 
        fontsize=8, color='white')

# Arrow BLOCKED (downward)
arrow_blocked = FancyArrowPatch((decision_x + 0.75, fusion_y - 0.45), (decision_x + 0.75, fusion_y - 1.1), 
                                arrowstyle='->', mutation_scale=25, linewidth=2.5, 
                                color='#B71C1C', linestyle='--')
ax.add_patch(arrow_blocked)
ax.text(decision_x + 1.2, fusion_y - 0.75, 'BLOCKED', ha='left', fontsize=8, fontweight='bold', 
        color='#B71C1C')

# Arrow ALLOWED (rightward)
arrow_allowed = FancyArrowPatch((decision_x + 1.5, fusion_y), (decision_x + 2.5, fusion_y), 
                                arrowstyle='->', mutation_scale=25, linewidth=2.5, 
                                color='#2E7D32')
ax.add_patch(arrow_allowed)
ax.text(decision_x + 2.0, fusion_y + 0.35, 'ALLOWED', ha='center', fontsize=8, fontweight='bold', 
        color='#2E7D32')

# ============================================================================
# LLM PROCESSING
# ============================================================================
llm_x = decision_x + 2.5
llm_box = FancyBboxPatch((llm_x, fusion_y - 0.45), 1.5, 1.0, boxstyle="round,pad=0.08",
                         edgecolor='#F57F17', facecolor=color_llm, linewidth=2.5)
ax.add_patch(llm_box)
ax.text(llm_x + 0.75, fusion_y + 0.15, 'LLM', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='#F57F17')
ax.text(llm_x + 0.75, fusion_y - 0.15, 'Processing', ha='center', va='center', 
        fontsize=8, color='#F57F17')

# ============================================================================
# SECTION 2: EXAMPLE ATTACK FLOW - CENTERED AND CLOSER TO TITLE
# ============================================================================
y_example_title = 7.5
y_example = 7.1

# Title for example
ax.text(0.6, y_example_title, 'Example: Attack Processing Flow', fontsize=10, fontweight='bold', 
        color='#E65100')

# Example box - centered and closer to title
example_box = FancyBboxPatch((0.5, y_example - 1.7), 15.0, 1.7, boxstyle="round,pad=0.1",
                             edgecolor='#E65100', facecolor=color_example, linewidth=2, linestyle='--')
ax.add_patch(example_box)

# Example input
ex_input = FancyBboxPatch((1.0, y_example - 1.3), 2.0, 0.7, boxstyle="round,pad=0.06",
                          edgecolor='#1565C0', facecolor=color_input, linewidth=1.5)
ax.add_patch(ex_input)
ax.text(2.0, y_example - 0.8, 'Input:', ha='center', va='center', 
        fontsize=7.5, fontweight='bold')
ax.text(2.0, y_example - 1.05, '"Ignore previous', ha='center', va='center', 
        fontsize=6.5, family='monospace')
ax.text(2.0, y_example - 1.25, 'instructions..."', ha='center', va='center', 
        fontsize=6.5, family='monospace')

# Arrow
arrow_ex1 = FancyArrowPatch((3.0, y_example - 0.95), (3.6, y_example - 0.95), 
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#E65100')
ax.add_patch(arrow_ex1)

# Normalizer step
ex_norm = FancyBboxPatch((3.6, y_example - 1.3), 1.8, 0.7, boxstyle="round,pad=0.06",
                         edgecolor='#2E7D32', facecolor=color_normalizer, linewidth=1.5)
ax.add_patch(ex_norm)
ax.text(4.5, y_example - 0.8, 'Normalizer:', ha='center', va='center', 
        fontsize=7.5, fontweight='bold', color='#1B5E20')
ax.text(4.5, y_example - 1.05, 'Cleans unicode', ha='center', va='center', 
        fontsize=7, family='monospace', color='#1B5E20')

# Arrow
arrow_ex2 = FancyArrowPatch((5.4, y_example - 0.95), (6.0, y_example - 0.95), 
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#E65100')
ax.add_patch(arrow_ex2)

# v1 Detection
ex_v1 = FancyBboxPatch((6.0, y_example - 1.3), 1.8, 0.7, boxstyle="round,pad=0.06",
                       edgecolor='#1565C0', facecolor=color_detector, linewidth=1.5)
ax.add_patch(ex_v1)
ax.text(6.9, y_example - 0.8, 'v1 Signature:', ha='center', va='center', 
        fontsize=7.5, fontweight='bold', color='white')
ax.text(6.9, y_example - 1.05, 'Matches keyword', ha='center', va='center', 
        fontsize=7, family='monospace', color='white')

# Arrow
arrow_ex3 = FancyArrowPatch((7.8, y_example - 0.95), (8.4, y_example - 0.95), 
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#E65100')
ax.add_patch(arrow_ex3)

# Decision
ex_decision = FancyBboxPatch((8.4, y_example - 1.3), 1.8, 0.7, boxstyle="round,pad=0.06",
                             edgecolor='#B71C1C', facecolor=color_decision, linewidth=1.5)
ax.add_patch(ex_decision)
ax.text(9.3, y_example - 0.8, 'Decision:', ha='center', va='center', 
        fontsize=7.5, fontweight='bold', color='white')
ax.text(9.3, y_example - 1.05, 'BLOCKED', ha='center', va='center', 
        fontsize=7, family='monospace', color='white')

# Performance metrics
perf_text = 'Performance: 87% TPR on known attacks  |  0.77% FAR on benign  |  <0.1ms latency'
ax.text(0.7, y_example - 1.55, perf_text, fontsize=8, style='italic', 
        color='#E65100', fontweight='bold')

# ============================================================================
# SECTION 3: METRICS & SPECIFICATIONS (Two columns)
# ============================================================================
y_metrics = 4.5

# Left column: Production Configuration
metrics_box_left = FancyBboxPatch((0.5, y_metrics - 1.8), 7.3, 1.8, boxstyle="round,pad=0.1",
                                  edgecolor=color_border, facecolor=color_metrics, linewidth=2)
ax.add_patch(metrics_box_left)
ax.text(4.15, y_metrics + 0.5, 'Production Configuration: Normalizer + v3', 
        fontsize=9, fontweight='bold', color='#0D47A1')

metrics_lines_left = [
    'True Positive Rate (TPR): 87%',
    'False Alarm Rate (FAR): 0.77%',
    'Latency: <0.1ms per sample',
    'Complexity: ~1,200 lines',
    'Deployment: Stateless',
    'Dependencies: None (pure Python)'
]

y_pos = y_metrics + 0.15
for line in metrics_lines_left:
    ax.text(0.8, y_pos, line, fontsize=7.5, family='monospace', verticalalignment='top')
    y_pos -= 0.25

# Right column: Component Specifications
metrics_box_right = FancyBboxPatch((8.2, y_metrics - 1.8), 7.3, 1.8, boxstyle="round,pad=0.1",
                                   edgecolor=color_border, facecolor=color_metrics, linewidth=2)
ax.add_patch(metrics_box_right)
ax.text(11.85, y_metrics + 0.5, 'Component Specifications', fontsize=9, fontweight='bold', 
        color='#0D47A1')

details_lines = [
    'Signature Detector (v1):',
    '  • 80% TPR, 0% FAR',
    '  • Keyword matching',
    '',
    'Semantic Detector (v3):',
    '  • 57% TPR, 0% FAR',
    '  • Pattern analysis',
    '',
    'Fusion: OR Logic (v1+v3)',
    '  • Combined: 87% TPR, 0% FAR'
]

y_pos = y_metrics + 0.15
for line in details_lines:
    ax.text(8.5, y_pos, line, fontsize=7.5, family='monospace', verticalalignment='top')
    y_pos -= 0.18

# ============================================================================
# SECTION 4: KEY DESIGN PRINCIPLES (Bottom)
# ============================================================================
y_principles = 2.0

principles_box = FancyBboxPatch((0.5, y_principles - 1.5), 15.0, 1.5, boxstyle="round,pad=0.1",
                                edgecolor='#0D47A1', facecolor='#E3F2FD', linewidth=2.5)
ax.add_patch(principles_box)
ax.text(8, y_principles + 0.7, 'Key Design Principles', fontsize=10, fontweight='bold', 
        color='#0D47A1', ha='center')

principles_lines = [
    '1. INPUT-SIDE DETECTION: Attacks blocked BEFORE reaching the LLM',
    '2. NORMALIZER FIRST: Unicode/homoglyph normalization ensures consistent detection',
    '3. COMPLEMENTARY DETECTORS: v1 (signature) + v3 (semantic) catch different patterns',
    '4. THRESHOLD-INVARIANT: Binary OR logic eliminates threshold tuning complexity',
    '5. PRODUCTION-READY: <0.1ms latency, CPU-only, no external dependencies'
]

y_pos = y_principles + 0.3
for line in principles_lines:
    ax.text(0.8, y_pos, line, fontsize=7.5, verticalalignment='top')
    y_pos -= 0.25

# ============================================================================
# LEGEND
# ============================================================================
legend_y = 0.15
ax.text(0.5, legend_y, 'Legend:', fontsize=8, fontweight='bold')

colors_legend = [
    (color_input, 'Input'),
    (color_normalizer, 'Normalizer'),
    (color_detector, 'Detector'),
    (color_fusion, 'Fusion'),
    (color_decision, 'Decision'),
    (color_llm, 'LLM'),
]

legend_x = 1.4
for i, (color, label) in enumerate(colors_legend):
    rect = Rectangle((legend_x + i*1.95, legend_y - 0.08), 0.12, 0.08, 
                     facecolor=color, edgecolor=color_border, linewidth=1)
    ax.add_patch(rect)
    ax.text(legend_x + i*1.95 + 0.2, legend_y - 0.04, label, fontsize=7, va='center')

plt.tight_layout()
output_path = Path(__file__).parent / 'GENERATED_FIGURES' / 'figure_16_system_architecture.png'
plt.savefig(str(output_path), dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print("✓ Figure 16 (Centered Layout) generated successfully!")
print(f"  Saved to: {output_path}")
print("\nCentering Improvements:")
print("  ✓ Upper pipeline diagram centered on page")
print("  ✓ Example box (red dashed) centered on page")
print("  ✓ Example box moved closer to its title")
print("  ✓ Better visual balance")
print("  ✓ Professional layout")
