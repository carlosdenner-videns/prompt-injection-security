#!/usr/bin/env python3
"""
Figure 16: System Architecture Diagram
Generates a flow diagram showing the system architecture
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5, 'Figure 16: System Architecture - Prompt Injection Detection Pipeline', 
        ha='center', fontsize=14, fontweight='bold')

# Color scheme
color_input = '#E8F4F8'
color_process = '#B3E5FC'
color_detector = '#81D4FA'
color_fusion = '#4FC3F7'
color_output = '#29B6F6'

# Input Layer
input_box = FancyBboxPatch((0.5, 7.5), 1.8, 1, boxstyle="round,pad=0.1", 
                           edgecolor='black', facecolor=color_input, linewidth=2)
ax.add_patch(input_box)
ax.text(1.4, 8, 'INPUT\nText/Query', ha='center', va='center', fontsize=10, fontweight='bold')

# Arrow to Normalizer
arrow1 = FancyArrowPatch((2.3, 8), (3.2, 8), arrowstyle='->', mutation_scale=20, linewidth=2)
ax.add_patch(arrow1)

# Normalizer
norm_box = FancyBboxPatch((3.2, 7.5), 1.8, 1, boxstyle="round,pad=0.1",
                          edgecolor='black', facecolor=color_process, linewidth=2)
ax.add_patch(norm_box)
ax.text(4.1, 8, 'NORMALIZER\nUnicode/Homoglyph', ha='center', va='center', fontsize=9, fontweight='bold')

# Arrow to Detectors
arrow2 = FancyArrowPatch((5, 8), (5.8, 8), arrowstyle='->', mutation_scale=20, linewidth=2)
ax.add_patch(arrow2)

# Detector v1
det1_box = FancyBboxPatch((5.8, 8.8), 1.5, 0.8, boxstyle="round,pad=0.05",
                          edgecolor='black', facecolor=color_detector, linewidth=2)
ax.add_patch(det1_box)
ax.text(6.55, 9.2, 'v1: Signature', ha='center', va='center', fontsize=9, fontweight='bold')

# Detector v2
det2_box = FancyBboxPatch((5.8, 7.6), 1.5, 0.8, boxstyle="round,pad=0.05",
                          edgecolor='black', facecolor=color_detector, linewidth=2)
ax.add_patch(det2_box)
ax.text(6.55, 8, 'v2: Heuristic', ha='center', va='center', fontsize=9, fontweight='bold')

# Detector v3
det3_box = FancyBboxPatch((5.8, 6.4), 1.5, 0.8, boxstyle="round,pad=0.05",
                          edgecolor='black', facecolor=color_detector, linewidth=2)
ax.add_patch(det3_box)
ax.text(6.55, 6.8, 'v3: Semantic', ha='center', va='center', fontsize=9, fontweight='bold')

# Arrows from detectors to fusion
arrow_d1 = FancyArrowPatch((7.3, 9.2), (7.8, 7.5), arrowstyle='->', mutation_scale=15, linewidth=1.5)
ax.add_patch(arrow_d1)
arrow_d2 = FancyArrowPatch((7.3, 8), (7.8, 7.5), arrowstyle='->', mutation_scale=15, linewidth=1.5)
ax.add_patch(arrow_d2)
arrow_d3 = FancyArrowPatch((7.3, 6.8), (7.8, 7.5), arrowstyle='->', mutation_scale=15, linewidth=1.5)
ax.add_patch(arrow_d3)

# Fusion Layer
fusion_box = FancyBboxPatch((7.8, 6.8), 1.8, 1.4, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor=color_fusion, linewidth=2)
ax.add_patch(fusion_box)
ax.text(8.7, 7.5, 'FUSION\nOR Logic\n(v1+v3)', ha='center', va='center', fontsize=9, fontweight='bold')

# Arrow to Decision
arrow3 = FancyArrowPatch((9.6, 7.5), (0.5, 7.5), arrowstyle='->', mutation_scale=20, linewidth=2, 
                         connectionstyle="arc3,rad=0.3")
ax.add_patch(arrow3)

# Output/Decision
output_box = FancyBboxPatch((0.5, 6.8), 1.8, 1.4, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor=color_output, linewidth=2)
ax.add_patch(output_box)
ax.text(1.4, 7.5, 'DECISION\nAttack/Benign', ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Performance Metrics Box
perf_box = FancyBboxPatch((0.5, 4.5), 9, 1.8, boxstyle="round,pad=0.1",
                          edgecolor='#333', facecolor='#F5F5F5', linewidth=2, linestyle='--')
ax.add_patch(perf_box)
ax.text(5, 6, 'Performance Metrics', ha='center', fontsize=11, fontweight='bold')
ax.text(2, 5.4, '• TPR: 87% (Phase 1)', ha='left', fontsize=9)
ax.text(2, 5, '• FAR: 0.77% (Obfuscated)', ha='left', fontsize=9)
ax.text(5.5, 5.4, '• Latency: <0.1ms', ha='left', fontsize=9)
ax.text(5.5, 5, '• Complexity: ~1,200 LOC', ha='left', fontsize=9)

# Data Flow Examples
data_box = FancyBboxPatch((0.5, 1.5), 9, 2.5, boxstyle="round,pad=0.1",
                          edgecolor='#333', facecolor='#FFFACD', linewidth=2, linestyle='--')
ax.add_patch(data_box)
ax.text(5, 3.7, 'Data Flow Examples', ha='center', fontsize=11, fontweight='bold')

# Example 1
ax.text(0.8, 3.2, 'Example 1: Plain Text Attack', ha='left', fontsize=9, fontweight='bold')
ax.text(0.8, 2.8, 'Input: "Ignore previous instructions..."', ha='left', fontsize=8, style='italic')
ax.text(0.8, 2.4, '→ v1 detects: "Ignore" keyword ✓', ha='left', fontsize=8, color='green')
ax.text(0.8, 2.0, '→ Decision: ATTACK (block)', ha='left', fontsize=8, fontweight='bold', color='red')

# Example 2
ax.text(5.5, 3.2, 'Example 2: Obfuscated Benign', ha='left', fontsize=9, fontweight='bold')
ax.text(5.5, 2.8, 'Input: "Ign0re this café..." (homoglyph)', ha='left', fontsize=8, style='italic')
ax.text(5.5, 2.4, '→ Normalizer fixes: "Ignore this cafe"', ha='left', fontsize=8)
ax.text(5.5, 2.0, '→ Decision: BENIGN (allow)', ha='left', fontsize=8, fontweight='bold', color='green')

# Legend
ax.text(0.5, 0.8, 'Component Legend:', fontsize=10, fontweight='bold')
ax.add_patch(FancyBboxPatch((0.5, 0.3), 0.3, 0.3, boxstyle="round,pad=0.02", 
                            edgecolor='black', facecolor=color_input, linewidth=1))
ax.text(1, 0.45, 'Input', fontsize=8, va='center')

ax.add_patch(FancyBboxPatch((2, 0.3), 0.3, 0.3, boxstyle="round,pad=0.02",
                            edgecolor='black', facecolor=color_process, linewidth=1))
ax.text(2.5, 0.45, 'Processing', fontsize=8, va='center')

ax.add_patch(FancyBboxPatch((3.5, 0.3), 0.3, 0.3, boxstyle="round,pad=0.02",
                            edgecolor='black', facecolor=color_detector, linewidth=1))
ax.text(4, 0.45, 'Detection', fontsize=8, va='center')

ax.add_patch(FancyBboxPatch((5, 0.3), 0.3, 0.3, boxstyle="round,pad=0.02",
                            edgecolor='black', facecolor=color_fusion, linewidth=1))
ax.text(5.5, 0.45, 'Fusion', fontsize=8, va='center')

ax.add_patch(FancyBboxPatch((6.5, 0.3), 0.3, 0.3, boxstyle="round,pad=0.02",
                            edgecolor='black', facecolor=color_output, linewidth=1))
ax.text(7, 0.45, 'Output', fontsize=8, va='center')

plt.tight_layout()
plt.savefig('MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_16_system_architecture.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Figure 16 (System Architecture) generated successfully!")
print("  Saved to: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_16_system_architecture.png")
