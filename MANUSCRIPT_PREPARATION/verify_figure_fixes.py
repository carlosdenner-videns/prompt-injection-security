#!/usr/bin/env python3
"""
Verification Script: Check if figures have been regenerated without embedded numbers.
This script helps track your progress in fixing the figure numbering issue.
"""

import os
from pathlib import Path
from datetime import datetime

# Configuration
MANUSCRIPT_DIR = Path(__file__).parent
CHECKLIST_FILE = MANUSCRIPT_DIR / "figure_fix_checklist.txt"


def create_checklist():
    """Create an interactive checklist file."""
    figures_to_fix = [
        ("fig4_detector_performance.pdf", 4, 2, "Remove 'Figure 4:', keep 'Detector Performance Comparison'"),
        ("fig6_complementarity.pdf", 6, 3, "Remove 'Figure 6:', keep 'Detector Complementarity Analysis'"),
        ("fig7_threshold_invariance.pdf", 7, 4, "Remove 'Figure 7:', keep 'Threshold-Invariant Performance'"),
        ("fig9_learning_gain.pdf", 9, 5, "Remove 'Figure 9:', keep title only"),
        ("fig10_obfuscation_fpr.pdf", 10, 6, "Remove 'Figure 10:', keep title only"),
        ("fig11_novel_attack_tpr.pdf", 11, 7, "Remove 'Figure 11:', keep title only"),
        ("fig13_adversarial_evasion.pdf", 13, 9, "Remove 'Figure 13:', keep title only"),
        ("fig15_generalization_gap.pdf", 15, 8, "Remove 'Figure 15:', keep title only"),
        ("fig16_architecture.pdf", 16, 10, "Remove 'Figure 16:', keep title only"),
    ]
    
    with open(CHECKLIST_FILE, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("FIGURE REGENERATION CHECKLIST\n")
        f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("Instructions:\n")
        f.write("1. Regenerate each figure without the 'Figure X:' prefix\n")
        f.write("2. Mark each item with [X] when complete\n")
        f.write("3. Run verify_figure_fixes.py to check your progress\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("CHECKLIST (Mark [X] when done):\n")
        f.write("-" * 80 + "\n\n")
        
        for filename, old_num, correct_num, action in figures_to_fix:
            f.write(f"[ ] Figure {correct_num} (LaTeX): {filename}\n")
            f.write(f"    Currently embedded: Figure {old_num}\n")
            f.write(f"    Action: {action}\n")
            f.write(f"    File modified: ___________\n")
            f.write("\n")
        
        f.write("-" * 80 + "\n")
        f.write("VERIFICATION:\n")
        f.write("-" * 80 + "\n")
        f.write("[ ] All figures regenerated\n")
        f.write("[ ] Verified in LaTeX compilation\n")
        f.write("[ ] No 'Figure X:' visible in any embedded images\n")
        f.write("[ ] Captions show correct sequential numbering\n")
        f.write("[ ] Ready for CACM submission\n")
    
    print(f"✓ Created checklist: {CHECKLIST_FILE}")
    print(f"  Edit this file to track your progress")


def read_checklist_status():
    """Read the checklist and count completed items."""
    if not CHECKLIST_FILE.exists():
        print(f"Checklist not found. Creating new checklist...")
        create_checklist()
        return
    
    with open(CHECKLIST_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count checkboxes
    total_items = content.count('[ ]') + content.count('[X]') + content.count('[x]')
    completed_items = content.count('[X]') + content.count('[x]')
    
    print()
    print("=" * 80)
    print("FIGURE FIX PROGRESS")
    print("=" * 80)
    print()
    print(f"Completed: {completed_items} / {total_items}")
    print(f"Progress: {'█' * int(completed_items / total_items * 40)}{' ' * (40 - int(completed_items / total_items * 40))} {completed_items / total_items * 100:.1f}%")
    print()
    
    if completed_items == total_items:
        print("🎉 ALL ITEMS COMPLETED! 🎉")
        print("Your manuscript is ready for CACM submission.")
    elif completed_items > 0:
        print(f"Keep going! {total_items - completed_items} items remaining.")
    else:
        print("Get started by regenerating the first figure!")
    
    print()
    print("=" * 80)


def generate_final_report():
    """Generate a final report for submission."""
    print()
    print("=" * 80)
    print("FINAL SUBMISSION CHECKLIST")
    print("=" * 80)
    print()
    
    checklist_items = [
        ("All figures regenerated without 'Figure X:' prefixes", False),
        ("LaTeX compiles without errors", False),
        ("All \\ref{fig:...} commands working correctly", False),
        ("Figure captions are descriptive and complete", False),
        ("Figure numbering is sequential (1, 2, 3, ...)", False),
        ("All figures have \\Description{} for accessibility", False),
        ("PDF output reviewed and figures look professional", False),
        ("No numbering mismatches between caption and image", False),
    ]
    
    for item, status in checklist_items:
        checkbox = "[X]" if status else "[ ]"
        print(f"{checkbox} {item}")
    
    print()
    print("=" * 80)
    print()
    print("FINAL STEPS BEFORE SUBMISSION:")
    print("1. Compile LaTeX: pdflatex prompt_injection_cacm.tex")
    print("2. Run BibTeX: bibtex prompt_injection_cacm")
    print("3. Compile again: pdflatex prompt_injection_cacm.tex (2x)")
    print("4. Review PDF: Check all figures appear correctly")
    print("5. Verify numbering: Figures should be 1-10 in order")
    print()
    print("=" * 80)


def check_file_timestamps():
    """Check when figure files were last modified."""
    print()
    print("=" * 80)
    print("FIGURE FILE MODIFICATION TIMES")
    print("=" * 80)
    print()
    
    figure_files = [
        "fig1_baseline_vulnerability.pdf",
        "fig4_detector_performance.pdf",
        "fig6_complementarity.pdf",
        "fig7_threshold_invariance.pdf",
        "fig9_learning_gain.pdf",
        "fig10_obfuscation_fpr.pdf",
        "fig11_novel_attack_tpr.pdf",
        "fig13_adversarial_evasion.pdf",
        "fig15_generalization_gap.pdf",
        "fig16_architecture.pdf",
    ]
    
    print(f"{'Filename':<40} {'Last Modified':<25} {'Status':<10}")
    print("-" * 80)
    
    for filename in figure_files:
        filepath = MANUSCRIPT_DIR / filename
        if filepath.exists():
            mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
            age_hours = (datetime.now() - mtime).total_seconds() / 3600
            
            if age_hours < 1:
                status = "Just now"
            elif age_hours < 24:
                status = f"{age_hours:.1f}h ago"
            else:
                status = f"{age_hours/24:.1f}d ago"
            
            print(f"{filename:<40} {mtime.strftime('%Y-%m-%d %H:%M:%S'):<25} {status:<10}")
        else:
            print(f"{filename:<40} {'NOT FOUND':<25} {'MISSING':<10}")
    
    print()


def main():
    """Main verification function."""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 23 + "FIGURE FIX VERIFICATION" + " " * 33 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Check if checklist exists
    if not CHECKLIST_FILE.exists():
        print()
        print("No checklist found. Creating one now...")
        create_checklist()
        print()
        print(f"Edit {CHECKLIST_FILE.name} to track your progress.")
        print("Mark items with [X] as you complete them.")
    else:
        read_checklist_status()
    
    check_file_timestamps()
    generate_final_report()
    
    print()
    print("TIP: After regenerating figures, run this script again to see your progress!")
    print()


if __name__ == "__main__":
    main()
