#!/usr/bin/env python3
"""
Figure Numbering Fix Script for CACM Manuscript
Identifies figure numbering mismatches and helps track regeneration progress.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict

# Configuration
MANUSCRIPT_DIR = Path(__file__).parent
TEX_FILE = MANUSCRIPT_DIR / "prompt_injection_cacm.tex"
FIGURES_DIR = MANUSCRIPT_DIR  # Figures are in same directory


def extract_figures_from_tex(tex_path: Path) -> List[Dict[str, str]]:
    """Extract figure information from LaTeX file."""
    figures = []
    
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all figure environments
    figure_pattern = r'\\begin\{figure\}\[t\](.*?)\\end\{figure\}'
    matches = re.finditer(figure_pattern, content, re.DOTALL)
    
    figure_num = 0
    for match in matches:
        figure_num += 1
        fig_content = match.group(1)
        
        # Extract filename
        filename_match = re.search(r'\\includegraphics.*?\{([^}]+)\}', fig_content)
        filename = filename_match.group(1) if filename_match else "Unknown"
        
        # Extract label
        label_match = re.search(r'\\label\{([^}]+)\}', fig_content)
        label = label_match.group(1) if label_match else "Unknown"
        
        # Extract caption (first 80 chars)
        caption_match = re.search(r'\\caption\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', fig_content)
        caption = caption_match.group(1) if caption_match else "Unknown"
        caption_short = caption[:80] + "..." if len(caption) > 80 else caption
        
        # Extract embedded number from filename
        embedded_num_match = re.search(r'fig(\d+)', filename)
        embedded_num = int(embedded_num_match.group(1)) if embedded_num_match else None
        
        figures.append({
            'latex_number': figure_num,
            'filename': filename,
            'embedded_number': embedded_num,
            'label': label,
            'caption': caption_short,
            'mismatch': embedded_num != figure_num if embedded_num else False
        })
    
    return figures


def print_figure_report(figures: List[Dict[str, str]]):
    """Print a detailed report of all figures."""
    print("=" * 100)
    print("FIGURE NUMBERING REPORT - CACM Manuscript")
    print("=" * 100)
    print()
    
    print(f"Total figures found: {len(figures)}")
    mismatches = sum(1 for fig in figures if fig['mismatch'])
    print(f"Figures with numbering mismatches: {mismatches}")
    print()
    
    print("-" * 100)
    print(f"{'LaTeX#':<8} {'File#':<8} {'Status':<10} {'Filename':<40} {'Label':<20}")
    print("-" * 100)
    
    for fig in figures:
        latex_num = f"Fig {fig['latex_number']}"
        file_num = f"fig{fig['embedded_number']}" if fig['embedded_number'] else "N/A"
        status = "✗ MISMATCH" if fig['mismatch'] else "✓ OK"
        filename = fig['filename'][:38] + "..." if len(fig['filename']) > 38 else fig['filename']
        label = fig['label'][:18] + "..." if len(fig['label']) > 18 else fig['label']
        
        print(f"{latex_num:<8} {file_num:<8} {status:<10} {filename:<40} {label:<20}")
    
    print("-" * 100)
    print()


def generate_checklist(figures: List[Dict[str, str]]):
    """Generate a checklist for figure regeneration."""
    print("=" * 100)
    print("FIGURE REGENERATION CHECKLIST")
    print("=" * 100)
    print()
    print("Instructions:")
    print("1. Open each figure file in your figure creation tool (Python/matplotlib, R, etc.)")
    print("2. Remove the 'Figure X:' prefix from the title")
    print("3. Keep only the descriptive title")
    print("4. Regenerate the PDF")
    print("5. Check off the item below")
    print()
    print("-" * 100)
    
    for fig in figures:
        if fig['mismatch']:
            print(f"\n[ ] Figure {fig['latex_number']}: {fig['filename']}")
            print(f"    Current embedded number: Figure {fig['embedded_number']}")
            print(f"    Action: Remove 'Figure {fig['embedded_number']:}' from title, keep descriptive text only")
            print(f"    Caption: {fig['caption']}")
    
    print()
    print("-" * 100)


def generate_rename_script(figures: List[Dict[str, str]]):
    """Generate a script to rename files (optional approach)."""
    print()
    print("=" * 100)
    print("OPTIONAL: FILE RENAME SCRIPT")
    print("=" * 100)
    print()
    print("# If you prefer to rename files instead of regenerating:")
    print("# WARNING: This will rename your existing PDF files!")
    print()
    
    for fig in figures:
        if fig['mismatch'] and fig['embedded_number']:
            old_name = fig['filename']
            # Generate new filename with correct number
            new_name = re.sub(r'fig\d+', f'fig{fig["latex_number"]}', old_name)
            
            if old_name != new_name:
                print(f"# Figure {fig['latex_number']}")
                print(f"mv '{old_name}' '{new_name}'")
                print()


def check_file_existence(figures: List[Dict[str, str]], figures_dir: Path):
    """Check if all figure files exist."""
    print()
    print("=" * 100)
    print("FILE EXISTENCE CHECK")
    print("=" * 100)
    print()
    
    missing_files = []
    for fig in figures:
        # Check for .pdf extension
        pdf_file = figures_dir / fig['filename']
        if not pdf_file.exists():
            # Try adding .pdf if not present
            if not fig['filename'].endswith('.pdf'):
                pdf_file = figures_dir / (fig['filename'] + '.pdf')
        
        if not pdf_file.exists():
            missing_files.append(fig['filename'])
            print(f"✗ MISSING: {fig['filename']}")
        else:
            print(f"✓ Found: {fig['filename']}")
    
    print()
    if missing_files:
        print(f"WARNING: {len(missing_files)} figure file(s) not found!")
    else:
        print("All figure files found.")
    print()


def main():
    """Main function."""
    print("\n")
    print("╔" + "═" * 98 + "╗")
    print("║" + " " * 25 + "CACM MANUSCRIPT FIGURE NUMBERING FIX" + " " * 37 + "║")
    print("╚" + "═" * 98 + "╝")
    print()
    
    # Check if TEX file exists
    if not TEX_FILE.exists():
        print(f"ERROR: LaTeX file not found: {TEX_FILE}")
        return
    
    # Extract figure information
    print(f"Reading LaTeX file: {TEX_FILE.name}")
    figures = extract_figures_from_tex(TEX_FILE)
    print(f"Found {len(figures)} figures")
    print()
    
    # Generate reports
    print_figure_report(figures)
    check_file_existence(figures, FIGURES_DIR)
    generate_checklist(figures)
    generate_rename_script(figures)
    
    # Summary
    print()
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print()
    print("RECOMMENDED APPROACH:")
    print("1. Regenerate each mismatched figure WITHOUT 'Figure X:' in the title")
    print("2. This makes the manuscript maintainable (adding/removing figures won't break numbering)")
    print("3. LaTeX \\caption{} will provide the authoritative figure numbers")
    print()
    print("ALTERNATIVE APPROACH:")
    print("1. Use the rename script above to update filenames")
    print("2. Update \\includegraphics{} commands in the .tex file")
    print("3. Still need to remove 'Figure X:' from the embedded images eventually")
    print()
    print("For CACM publication quality, Option 1 (regenerate without numbers) is strongly recommended.")
    print("=" * 100)
    print()


if __name__ == "__main__":
    main()
