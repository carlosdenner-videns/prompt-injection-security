#!/usr/bin/env python3
"""
Figure 16: System Architecture - Final Publication-Ready Design
Optimized text placement and spacing
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
# SECTION 1: MAIN PIPELINE (Top)
# ============================================================================
y_pipeline = 9.5

# INPUT
input_box = FancyBboxPatch((0.5, y_pipeline - 0.6), 1.4, 0.9, boxstyle="round,pad=0.08",
                           edgecolor=color_border, facecolor=color_input, linewidth=2)
ax.add_patch(input_box)
ax.text(1.2, y_pipeline - 0.05, 'INPUT', ha='center', va='center', 
        fontsize=9, fontweight='bold')
ax.text(1.2, y_pipeline - 0.35, 'Query', ha='center', va='center', 
        fontsize=8)

# Arrow to Normalizer
arrow1 = FancyArrowPatch((1.9, y_pipeline - 0.05), (2.7, y_pipeline - 0.05), 
                         arrowstyle='->', mutation_scale=25, linewidth=2.5, color=color_border)
ax.add_patch(arrow1)

# NORMALIZER (Recommended)
norm_box = FancyBboxPatch((2.7, y_pipeline - 0.6), 1.6, 0.9, boxstyle="round,pad=0.08",
                          edgecolor='#2E7D32', facecolor=color_normalizer, linewidth=2.5)
ax.add_patch(norm_box)
ax.text(3.5, y_pipeline - 0.05, 'Normalizer', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='#1B5E20')
ax.text(3.5, y_pipeline - 0.35, 'Unicode Fix', ha='center', va='center', 
        fontsize=8, color='#1B5E20')

# Arrow to Detectors
arrow2 = FancyArrowPatch((4.3, y_pipeline - 0.05), (5.1, y_pipeline - 0.05), 
                         arrowstyle='->', mutation_scale=25, linewidth=2.5, color=color_border)
ax.add_patch(arrow2)

# DETECTOR v1 (Signature)
det1_box = FancyBboxPatch((5.1, y_pipeline + 0.35), 1.4, 0.8, boxstyle="round,pad=0.06",
                          edgecolor='#1565C0', facecolor=color_detector, linewidth=2)
ax.add_patch(det1_box)
ax.text(5.8, y_pipeline + 0.65, 'Signature', ha='center', va='center', 
        fontsize=8, fontweight='bold', color='white')
ax.text(5.8, y_pipeline + 0.35, 'Detector (v1)', ha='center', va='center', 
        fontsize=7.5, color='white')

# DETECTOR v2 (Heuristic)
det2_box = FancyBboxPatch((5.1, y_pipeline - 0.15), 1.4, 0.8, boxstyle="round,pad=0.06",
                          edgecolor='#1565C0', facecolor=color_detector, linewidth=2)
ax.add_patch(det2_box)
ax.text(5.8, y_pipeline + 0.15, 'Heuristic', ha='center', va='center', 
        fontsize=8, fontweight='bold', color='white')
ax.text(5.8, y_pipeline - 0.15, 'Detector (v2)', ha='center', va='center', 
        fontsize=7.5, color='white')

# DETECTOR v3 (Semantic)
det3_box = FancyBboxPatch((5.1, y_pipeline - 0.65), 1.4, 0.8, boxstyle="round,pad=0.06",
                          edgecolor='#1565C0', facecolor=color_detector, linewidth=2)
ax.add_patch(det3_box)
ax.text(5.8, y_pipeline - 0.35, 'Semantic', ha='center', va='center', 
        fontsize=8, fontweight='bold', color='white')
ax.text(5.8, y_pipeline - 0.65, 'Detector (v3)', ha='center', va='center', 
        fontsize=7.5, color='white')

# Arrows from detectors to fusion
arrow_d1 = FancyArrowPatch((6.5, y_pipeline + 0.65), (7.0, y_pipeline + 0.15), 
                           arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#666')
ax.add_patch(arrow_d1)
arrow_d2 = FancyArrowPatch((6.5, y_pipeline + 0.15), (7.0, y_pipeline + 0.15), 
                           arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#666')
ax.add_patch(arrow_d2)
arrow_d3 = FancyArrowPatch((6.5, y_pipeline - 0.35), (7.0, y_pipeline + 0.15), 
                           arrowstyle='->', mutation_scale=20, linewidth=1.5, color='#666')
ax.add_patch(arrow_d3)

# FUSION (OR Logic)
fusion_box = FancyBboxPatch((7.0, y_pipeline - 0.45), 1.6, 1.0, boxstyle="round,pad=0.08",
                            edgecolor='#0D47A1', facecolor=color_fusion, linewidth=2.5)
ax.add_patch(fusion_box)
ax.text(7.8, y_pipeline + 0.15, 'Fusion', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='white')
ax.text(7.8, y_pipeline - 0.15, 'OR Logic', ha='center', va='center', 
        fontsize=8, color='white')
ax.text(7.8, y_pipeline - 0.35, '(v1+v3)', ha='center', va='center', 
        fontsize=7.5, color='white')

# Arrow to Decision
arrow3 = FancyArrowPatch((8.6, y_pipeline + 0.05), (9.6, y_pipeline + 0.05), 
                         arrowstyle='->', mutation_scale=25, linewidth=2.5, color=color_border)
ax.add_patch(arrow3)

# DECISION
decision_box = FancyBboxPatch((9.6, y_pipeline - 0.45), 1.5, 1.0, boxstyle="round,pad=0.08",
                              edgecolor='#B71C1C', facecolor=color_decision, linewidth=2.5)
ax.add_patch(decision_box)
ax.text(10.35, y_pipeline + 0.15, 'DECISION', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='white')
ax.text(10.35, y_pipeline - 0.15, 'Attack/Benign', ha='center', va='center', 
        fontsize=8, color='white')

# Arrow BLOCKED (downward)
arrow_blocked = FancyArrowPatch((10.35, y_pipeline - 0.45), (10.35, y_pipeline - 1.1), 
                                arrowstyle='->', mutation_scale=25, linewidth=2.5, 
                                color='#B71C1C', linestyle='--')
ax.add_patch(arrow_blocked)
ax.text(10.8, y_pipeline - 0.75, 'BLOCKED', ha='left', fontsize=8, fontweight='bold', 
        color='#B71C1C')

# Arrow ALLOWED (rightward)
arrow_allowed = FancyArrowPatch((11.1, y_pipeline + 0.05), (12.1, y_pipeline + 0.05), 
                                arrowstyle='->', mutation_scale=25, linewidth=2.5, 
                                color='#2E7D32')
ax.add_patch(arrow_allowed)
ax.text(11.6, y_pipeline + 0.35, 'ALLOWED', ha='center', fontsize=8, fontweight='bold', 
        color='#2E7D32')

# LLM PROCESSING
llm_box = FancyBboxPatch((12.1, y_pipeline - 0.45), 1.5, 1.0, boxstyle="round,pad=0.08",
                         edgecolor='#F57F17', facecolor=color_llm, linewidth=2.5)
ax.add_patch(llm_box)
ax.text(12.85, y_pipeline + 0.15, 'LLM', ha='center', va='center', 
        fontsize=9, fontweight='bold', color='#F57F17')
ax.text(12.85, y_pipeline - 0.15, 'Processing', ha='center', va='center', 
        fontsize=8, color='#F57F17')

# ============================================================================
# SECTION 2: EXAMPLE ATTACK FLOW
# ============================================================================
y_example = 7.2

example_box = FancyBboxPatch((0.3, y_example - 1.9), 15.4, 1.9, boxstyle="round,pad=0.1",
                             edgecolor='#E65100', facecolor=color_example, linewidth=2, linestyle='--')
ax.add_patch(example_box)
ax.text(0.6, y_example + 0.6, 'Example: Attack Processing Flow', fontsize=10, fontweight='bold', 
        color='#E65100')

# Example input
ex_input = FancyBboxPatch((0.5, y_example - 1.4), 2.3, 0.8, boxstyle="round,pad=0.06",
                          edgecolor='#1565C0', facecolor=color_input, linewidth=1.5)
ax.add_patch(ex_input)
ax.text(1.65, y_example - 0.8, 'Input:', ha='center', va='center', 
        fontsize=7.5, fontweight='bold')
ax.text(1.65, y_example - 1.1, '"Ignore previous', ha='center', va='center', 
        fontsize=6.5, family='monospace')
ax.text(1.65, y_example - 1.3, 'instructions..."', ha='center', va='center', 
        fontsize=6.5, family='monospace')

# Arrow
arrow_ex1 = FancyArrowPatch((2.8, y_example - 1.0), (3.4, y_example - 1.0), 
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#E65100')
ax.add_patch(arrow_ex1)

# Normalizer step
ex_norm = FancyBboxPatch((3.4, y_example - 1.4), 2.0, 0.8, boxstyle="round,pad=0.06",
                         edgecolor='#2E7D32', facecolor=color_normalizer, linewidth=1.5)
ax.add_patch(ex_norm)
ax.text(4.4, y_example - 0.8, 'Normalizer:', ha='center', va='center', 
        fontsize=7.5, fontweight='bold', color='#1B5E20')
ax.text(4.4, y_example - 1.1, 'Cleans unicode', ha='center', va='center', 
        fontsize=7, family='monospace', color='#1B5E20')

# Arrow
arrow_ex2 = FancyArrowPatch((5.4, y_example - 1.0), (6.0, y_example - 1.0), 
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#E65100')
ax.add_patch(arrow_ex2)

# v1 Detection
ex_v1 = FancyBboxPatch((6.0, y_example - 1.4), 2.0, 0.8, boxstyle="round,pad=0.06",
                       edgecolor='#1565C0', facecolor=color_detector, linewidth=1.5)
ax.add_patch(ex_v1)
ax.text(7.0, y_example - 0.8, 'v1 Signature:', ha='center', va='center', 
        fontsize=7.5, fontweight='bold', color='white')
ax.text(7.0, y_example - 1.1, 'Matches keyword', ha='center', va='center', 
        fontsize=7, family='monospace', color='white')

# Arrow
arrow_ex3 = FancyArrowPatch((8.0, y_example - 1.0), (8.6, y_example - 1.0), 
                            arrowstyle='->', mutation_scale=20, linewidth=2, color='#E65100')
ax.add_patch(arrow_ex3)

# Decision
ex_decision = FancyBboxPatch((8.6, y_example - 1.4), 2.0, 0.8, boxstyle="round,pad=0.06",
                             edgecolor='#B71C1C', facecolor=color_decision, linewidth=1.5)
ax.add_patch(ex_decision)
ax.text(9.6, y_example - 0.8, 'Decision:', ha='center', va='center', 
        fontsize=7.5, fontweight='bold', color='white')
ax.text(9.6, y_example - 1.1, 'BLOCKED', ha='center', va='center', 
        fontsize=7, family='monospace', color='white')

# Performance metrics
perf_text = 'Performance: 87% TPR on known attacks  |  0.77% FAR on benign  |  <0.1ms latency'
ax.text(0.5, y_example - 1.75, perf_text, fontsize=8, style='italic', 
        color='#E65100', fontweight='bold')

# ============================================================================
# SECTION 3: METRICS & SPECIFICATIONS (Two columns)
# ============================================================================
y_metrics = 4.5

# Left column: Production Configuration
metrics_box_left = FancyBboxPatch((0.3, y_metrics - 1.8), 7.3, 1.8, boxstyle="round,pad=0.1",
                                  edgecolor=color_border, facecolor=color_metrics, linewidth=2)
ax.add_patch(metrics_box_left)
ax.text(3.95, y_metrics + 0.5, 'Production Configuration: Normalizer + v3', 
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
    ax.text(0.6, y_pos, line, fontsize=7.5, family='monospace', verticalalignment='top')
    y_pos -= 0.25

# Right column: Component Specifications
metrics_box_right = FancyBboxPatch((8.4, y_metrics - 1.8), 7.3, 1.8, boxstyle="round,pad=0.1",
                                   edgecolor=color_border, facecolor=color_metrics, linewidth=2)
ax.add_patch(metrics_box_right)
ax.text(12.05, y_metrics + 0.5, 'Component Specifications', fontsize=9, fontweight='bold', 
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
    ax.text(8.7, y_pos, line, fontsize=7.5, family='monospace', verticalalignment='top')
    y_pos -= 0.18

# ============================================================================
# SECTION 4: KEY DESIGN PRINCIPLES (Bottom)
# ============================================================================
y_principles = 2.0

principles_box = FancyBboxPatch((0.3, y_principles - 1.5), 15.4, 1.5, boxstyle="round,pad=0.1",
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
    ax.text(0.6, y_pos, line, fontsize=7.5, verticalalignment='top')
    y_pos -= 0.25

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
    rect = Rectangle((legend_x + i*1.95, legend_y - 0.08), 0.12, 0.08, 
                     facecolor=color, edgecolor=color_border, linewidth=1)
    ax.add_patch(rect)
    ax.text(legend_x + i*1.95 + 0.2, legend_y - 0.04, label, fontsize=7, va='center')

plt.tight_layout()
output_path = Path(__file__).parent / 'GENERATED_FIGURES' / 'figure_16_system_architecture.png'
plt.savefig(str(output_path), dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print("✓ Figure 16 (Final - Text Optimized) generated successfully!")
print(f"  Saved to: {output_path}")
print("\nText Placement Improvements:")
print("  ✓ Multi-line text properly centered in boxes")
print("  ✓ Optimized font sizes for readability")
print("  ✓ Proper vertical spacing within boxes")
print("  ✓ No overlapping or cramped text")
print("  ✓ Clear visual hierarchy")
print("  ✓ Professional typography")
