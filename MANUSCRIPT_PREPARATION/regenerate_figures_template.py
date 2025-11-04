#!/usr/bin/env python3
"""
Template for Regenerating Figures WITHOUT Embedded Numbers
This shows how to modify your figure generation code to remove 'Figure X:' prefixes.

BEFORE (incorrect):
    plt.title('Figure 4: Detector Performance Comparison', fontsize=14, fontweight='bold')

AFTER (correct):
    plt.title('Detector Performance Comparison', fontsize=14, fontweight='bold')

LaTeX will handle the figure numbering via \caption{}.
"""

import matplotlib.pyplot as plt
import numpy as np

# Set publication-quality defaults
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['figure.dpi'] = 300


def example_figure_correct():
    """Example of CORRECT figure generation (no embedded number)."""
    fig, ax = plt.subplots()
    
    # Sample data
    categories = ['v1\n(signature)', 'v2\n(heuristics)', 'v3\n(semantic)']
    tpr = [89, 45, 82]
    far = [0.5, 3.2, 0.8]
    
    x = np.arange(len(categories))
    width = 0.35
    
    # Plot bars
    ax.bar(x - width/2, tpr, width, label='TPR (%)', color='#2E86AB')
    ax.bar(x + width/2, far, width, label='FAR (%)', color='#E63946')
    
    # CORRECT: No "Figure X:" prefix
    ax.set_title('Detector Performance Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel('Rate (%)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11)
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, 100)
    
    plt.tight_layout()
    return fig


def example_figure_incorrect():
    """Example of INCORRECT figure generation (has embedded number)."""
    fig, ax = plt.subplots()
    
    # Sample data
    categories = ['v1\n(signature)', 'v2\n(heuristics)', 'v3\n(semantic)']
    tpr = [89, 45, 82]
    
    x = np.arange(len(categories))
    
    ax.bar(x, tpr, color='#2E86AB')
    
    # INCORRECT: Has "Figure 4:" embedded
    ax.set_title('Figure 4: Detector Performance Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel('TPR (%)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    
    plt.tight_layout()
    return fig


def batch_regenerate_figures():
    """
    Template for batch regenerating all figures.
    Adapt this to your actual figure generation code.
    """
    
    # List of figures to regenerate
    figures_to_fix = [
        {
            'old_file': 'fig4_detector_performance.pdf',
            'new_file': 'fig4_detector_performance_fixed.pdf',
            'old_title': 'Figure 4: Detector Performance Comparison',
            'new_title': 'Detector Performance Comparison',
            'function': None  # Your figure generation function
        },
        {
            'old_file': 'fig6_complementarity.pdf',
            'new_file': 'fig6_complementarity_fixed.pdf',
            'old_title': 'Figure 6: Detector Complementarity Analysis',
            'new_title': 'Detector Complementarity Analysis',
            'function': None
        },
        {
            'old_file': 'fig7_threshold_invariance.pdf',
            'new_file': 'fig7_threshold_invariance_fixed.pdf',
            'old_title': 'Figure 7: Threshold-Invariant Performance',
            'new_title': 'Threshold-Invariant Performance',
            'function': None
        },
        # Add more figures as needed
    ]
    
    print("Figures to regenerate:")
    print("-" * 80)
    for i, fig_info in enumerate(figures_to_fix, 1):
        print(f"{i}. {fig_info['old_file']}")
        print(f"   Old title: {fig_info['old_title']}")
        print(f"   New title: {fig_info['new_title']}")
        print(f"   Output: {fig_info['new_file']}")
        print()
    
    return figures_to_fix


def quick_fix_guide():
    """Print a quick reference guide."""
    print()
    print("=" * 80)
    print("QUICK FIX GUIDE FOR MATPLOTLIB FIGURES")
    print("=" * 80)
    print()
    print("Step 1: Find the title line in your figure generation code")
    print("   Look for: plt.title(...) or ax.set_title(...)")
    print()
    print("Step 2: Remove the 'Figure X:' prefix")
    print("   BEFORE: plt.title('Figure 4: Detector Performance')")
    print("   AFTER:  plt.title('Detector Performance')")
    print()
    print("Step 3: Regenerate the PDF")
    print("   plt.savefig('figX_name.pdf', dpi=300, bbox_inches='tight')")
    print()
    print("Step 4: Verify the change")
    print("   Open the PDF and confirm no 'Figure X:' appears in the title")
    print()
    print("=" * 80)
    print()
    print("FOR OTHER TOOLS:")
    print()
    print("R/ggplot2:")
    print("   ggtitle('Detector Performance')  # Remove 'Figure 4:' prefix")
    print()
    print("Seaborn:")
    print("   plt.title('Detector Performance')  # Remove 'Figure 4:' prefix")
    print()
    print("Manual editing (if source code unavailable):")
    print("   1. Open PDF in Illustrator/Inkscape")
    print("   2. Delete 'Figure X:' text")
    print("   3. Save as new PDF")
    print()
    print("=" * 80)


if __name__ == "__main__":
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "FIGURE REGENERATION TEMPLATE" + " " * 30 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # Show examples
    print("Example 1: CORRECT figure (no embedded number)")
    print("-" * 80)
    fig_correct = example_figure_correct()
    # Uncomment to save: fig_correct.savefig('example_correct.pdf', dpi=300, bbox_inches='tight')
    print("✓ Title: 'Detector Performance Comparison'")
    print("✓ No 'Figure X:' prefix")
    print()
    
    print("Example 2: INCORRECT figure (has embedded number)")
    print("-" * 80)
    # Uncomment to see: fig_incorrect = example_figure_incorrect()
    print("✗ Title: 'Figure 4: Detector Performance Comparison'")
    print("✗ Should remove 'Figure 4:' prefix")
    print()
    
    # Show batch regeneration template
    figures_list = batch_regenerate_figures()
    
    # Show quick fix guide
    quick_fix_guide()
    
    print()
    print("NEXT STEPS:")
    print("1. Locate your original figure generation scripts")
    print("2. Modify titles to remove 'Figure X:' prefixes")
    print("3. Regenerate all PDFs with corrected titles")
    print("4. Run fix_figure_numbering.py to verify corrections")
    print()
