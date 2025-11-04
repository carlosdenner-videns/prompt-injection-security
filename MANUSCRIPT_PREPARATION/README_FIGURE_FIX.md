# Figure Numbering Fix - README

## Problem

The manuscript has a figure numbering mismatch between LaTeX's automatic numbering and the numbers embedded in the figure PDF files:

| LaTeX Auto-Number | Embedded in PDF | Status |
|-------------------|-----------------|--------|
| Figure 1 | fig1 | ✓ Correct |
| Figure 2 | fig4 | ✗ Mismatch |
| Figure 3 | fig6 | ✗ Mismatch |
| Figure 4 | fig7 | ✗ Mismatch |
| Figure 5 | fig9 | ✗ Mismatch |
| Figure 6 | fig10 | ✗ Mismatch |
| Figure 7 | fig11 | ✗ Mismatch |
| Figure 8 | fig15 | ✗ Mismatch |
| Figure 9 | fig13 | ✗ Mismatch |
| Figure 10 | fig16 | ✗ Mismatch |

## Solution

Remove the "Figure X:" prefix from all embedded figure titles. Let LaTeX handle numbering via `\caption{}`.

## Scripts Provided

### 1. `fix_figure_numbering.py`
**Purpose:** Diagnostic tool to identify all figure numbering issues.

**Usage:**
```bash
python fix_figure_numbering.py
```

**Output:**
- Complete report of all figures
- Numbering mismatches highlighted
- File existence check
- Checklist for regeneration

### 2. `regenerate_figures_template.py`
**Purpose:** Template and examples for regenerating figures without embedded numbers.

**Usage:**
```bash
python regenerate_figures_template.py
```

**Output:**
- Example of correct vs incorrect figure code
- Quick fix guide for matplotlib, R, and other tools
- Batch regeneration template

**How to use:**
1. Open your original figure generation scripts
2. Find lines like: `plt.title('Figure 4: Detector Performance')`
3. Change to: `plt.title('Detector Performance')`
4. Regenerate the PDF

### 3. `verify_figure_fixes.py`
**Purpose:** Track progress and verify completion.

**Usage:**
```bash
python verify_figure_fixes.py
```

**Output:**
- Progress tracker
- File modification times
- Final submission checklist
- Creates `figure_fix_checklist.txt` for manual tracking

## Quick Start Guide

### Step 1: Assess the Situation
```bash
python fix_figure_numbering.py
```
This will show you exactly which figures need fixing.

### Step 2: Regenerate Figures

**Option A: You have the source code**
1. Open your figure generation scripts (Python/R/etc.)
2. Remove "Figure X:" from all titles
3. Regenerate PDFs with same filenames
4. Example:
   ```python
   # BEFORE
   plt.title('Figure 4: Detector Performance Comparison')
   
   # AFTER
   plt.title('Detector Performance Comparison')
   ```

**Option B: No source code available**
1. Open PDF in Illustrator/Inkscape/PDF editor
2. Delete the "Figure X:" text from the title
3. Save as PDF
4. Repeat for all 9 figures

**Option C: Alternative approach (not recommended)**
- Rename files to match LaTeX numbering
- Update `\includegraphics{}` in .tex file
- Still need to remove embedded numbers eventually

### Step 3: Track Your Progress
```bash
python verify_figure_fixes.py
```
Edit `figure_fix_checklist.txt` and mark [X] as you complete each figure.

### Step 4: Verify Completion
```bash
python verify_figure_fixes.py
```
Should show 100% completion.

### Step 5: Final Compilation
```bash
pdflatex prompt_injection_cacm.tex
bibtex prompt_injection_cacm
pdflatex prompt_injection_cacm.tex
pdflatex prompt_injection_cacm.tex
```
Review the final PDF to ensure all figures show correct sequential numbering.

## Figures That Need Fixing

1. **fig4_detector_performance.pdf** → Remove "Figure 4:", keep "Detector Performance Comparison"
2. **fig6_complementarity.pdf** → Remove "Figure 6:", keep "Detector Complementarity Analysis"
3. **fig7_threshold_invariance.pdf** → Remove "Figure 7:", keep "Threshold-Invariant Performance"
4. **fig9_learning_gain.pdf** → Remove "Figure 9:", keep title only
5. **fig10_obfuscation_fpr.pdf** → Remove "Figure 10:", keep title only
6. **fig11_novel_attack_tpr.pdf** → Remove "Figure 11:", keep title only
7. **fig13_adversarial_evasion.pdf** → Remove "Figure 13:", keep title only
8. **fig15_generalization_gap.pdf** → Remove "Figure 15:", keep title only
9. **fig16_architecture.pdf** → Remove "Figure 16:", keep title only

## Why This Matters

- **Reader confusion:** Readers see "Figure 6" in the image but "Figure 3" in the caption
- **Professional appearance:** Mismatched numbers look unpolished
- **CACM standards:** Professional publications require consistent numbering
- **Maintainability:** If you add/remove figures, LaTeX auto-numbering adjusts—embedded numbers don't

## Common Tools

### Matplotlib (Python)
```python
# Remove from title:
plt.title('Your Descriptive Title', fontsize=14, fontweight='bold')
plt.savefig('figX_name.pdf', dpi=300, bbox_inches='tight')
```

### R (ggplot2)
```r
# Remove from ggtitle:
ggplot() + ... + ggtitle("Your Descriptive Title")
ggsave("figX_name.pdf", width=8, height=6, dpi=300)
```

### Seaborn (Python)
```python
# Remove from title:
plt.title('Your Descriptive Title')
plt.savefig('figX_name.pdf', dpi=300, bbox_inches='tight')
```

## Troubleshooting

**Q: I don't have the original figure generation code.**
A: You can edit PDFs directly in Illustrator, Inkscape, or other PDF editors. Just delete the "Figure X:" text.

**Q: The script says files are missing.**
A: Make sure all PDF files are in the same directory as the .tex file.

**Q: Can I just rename the files instead?**
A: You can, but you'll still need to remove the embedded "Figure X:" text eventually. Better to fix it properly now.

**Q: How do I know if I'm done?**
A: Run `verify_figure_fixes.py` and it should show 100% completion. Then compile LaTeX and check the PDF.

## Final Checklist

- [ ] All 9 figures regenerated without "Figure X:" in titles
- [ ] `verify_figure_fixes.py` shows 100% completion
- [ ] LaTeX compiles without errors
- [ ] PDF reviewed: figures numbered 1-10 sequentially
- [ ] No mismatch between caption and embedded image
- [ ] Ready for CACM submission

## Contact

If you encounter any issues with these scripts, check:
1. Python version (3.6+ required)
2. File paths are correct
3. PDFs are in the MANUSCRIPT_PREPARATION directory

---

**Created:** 2025-11-04  
**For:** CACM Manuscript - Prompt Injection Security  
**Purpose:** Fix figure numbering inconsistencies before publication
