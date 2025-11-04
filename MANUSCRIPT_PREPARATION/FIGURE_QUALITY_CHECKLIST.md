# Figure Quality Checklist for CACM Publication

## Professional Appearance Standards

### ✅ Font Size Requirements
**Minimum:** 8-10pt font in figures (will be readable in two-column layout)

**Current settings in `regenerate_manuscript_figures.py`:**
```python
plt.rcParams['font.size'] = 10  # ✓ Meets minimum
```

**What to check:**
- [ ] Axis labels: ≥10pt
- [ ] Tick labels: ≥9pt
- [ ] Legend text: ≥9pt
- [ ] Value annotations on bars: ≥9pt
- [ ] Title (if embedded): ≥13pt (but we removed titles!)

### ✅ Color Accessibility

**Current color scheme:**
- TPR bars: Green (`#2ca02c`) - good contrast
- FAR bars: Red (`#d62728`) - good contrast
- Model bars: Blue (`#1f77b4`), Orange (`#ff7f0e`)

**Accessibility measures already in place:**
1. ✓ Side-by-side bars (position differentiates)
2. ✓ Explicit labels in captions (TPR=green, FAR=red)
3. ✓ Value annotations on bars (numbers visible)
4. ✓ Different line styles available for threshold plot

**Optional enhancements (not mandatory):**
- Add hatching patterns to bars for colorblind accessibility
- Use different marker shapes for line plots (already using 'o' and 's')

### ✅ Figure Design Elements

**Required elements (all implemented):**
- [x] Labeled x-axes with units
- [x] Labeled y-axes with units (%)
- [x] Value labels on bars where helpful
- [x] Legends for multi-series plots
- [x] Grid lines (alpha=0.3 for subtlety)
- [x] Consistent styling across all figures

**Specific improvements made:**

#### Figure 1 (Baseline Vulnerability)
- ✓ Bars labeled with model names
- ✓ Y-axis: "Attack Success Rate (%)"
- ✓ X-axis: Attack vector categories
- ✓ Legend identifies models

#### Figure 2 (Detector Performance)
- ✓ Grouped bars for TPR/FAR
- ✓ Legend shows TPR (green), FAR (red)
- ✓ Y-axis: "Rate (%)"
- ✓ X-axis: Detector names (v1, v2, v3)

#### Figure 3 (Complementarity)
- ✓ Stacked bars show categories
- ✓ Value labels on each segment
- ✓ Y-axis: "Number of Attacks"
- ✓ Category labels clear

#### Figure 4 (Threshold Invariance)
- ✓ Line plot with markers
- ✓ Different markers for TPR (circle) and FAR (square)
- ✓ Legend identifies both lines
- ✓ X-axis: "Detection Threshold"
- ✓ Y-axis: "Rate (%)"

#### Figure 5 (Learning Gain)
- ✓ Bars with value annotations
- ✓ Clear comparison (87% → 99%)
- ✓ Y-axis: "True Positive Rate (%)"

#### Figure 6 (Obfuscation FAR)
- ✓ Heatmap with color bar
- ✓ Annotations show FAR values
- ✓ Row/column labels clear
- ✓ Color legend: "False Alarm Rate (%)"

#### Figure 7 (Novel Attacks)
- ✓ Horizontal bars (easier to read long labels)
- ✓ Value labels on bars
- ✓ X-axis: "True Positive Rate (%)"
- ✓ Category names on Y-axis

#### Figure 8 (Generalization Gap)
- ✓ Bars with value annotations
- ✓ Clear labels: "Known" vs "Novel"
- ✓ Y-axis: "True Positive Rate (%)"
- ✓ Values prominently displayed (99%, 49%)

#### Figure 9 (Adversarial Evasion)
- ✓ Horizontal bars with annotations
- ✓ Color coding by severity
- ✓ X-axis: "Evasion Rate (%)"
- ✓ Technique names on Y-axis

#### Figure 10 (Architecture)
- ✓ 16x11 inch size (large, clear)
- ✓ Boxes with descriptive labels
- ✓ Arrows show flow
- ✓ Color-coded components
- ✓ Sufficient spacing between elements

## Resolution and Output Quality

### Current Settings:
```python
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
```

**✓ 300 DPI** is publication quality for CACM

### File Formats:
- Primary: PDF (vector graphics, scales perfectly)
- Backup: PNG (raster, 300 DPI)

**Why PDF is preferred:**
- Scales to any size without quality loss
- Text remains crisp
- File size reasonable
- ACM accepts PDF figures

## Table Formatting Improvements

### Table 3 (Fusion Strategies)
**Enhanced:**
- ✓ OR-fusion row now bolded (emphasizes chosen method)
- ✓ Column header: "Fusion Strategy" (more descriptive)

### Table 6 (Deployment Configurations)
**Enhanced:**
- ✓ TPR column clarified with superscript notes
- ✓ Footnotes explain evaluation datasets
- ✓ Clear distinction between known/novel metrics

### Remaining Tables:
**Table 1 (Baseline):**
- Simple 2x2, already clear
- Numbers centered (ACM will handle alignment)

**Table 4 (Obfuscation FAR):**
- Column uses `siunitx` for number alignment
- Values clear and comparable

**Table 5 (Overhead):**
- Detailed caption explains all metrics
- Units specified (ms, MB, %)

## Figure Placement Strategy

### LaTeX Placement Directives:
All figures use `[t]` (top of page) placement:
```latex
\begin{figure}[t]
```

### Best Practices Implemented:
1. ✓ Figures placed near first text reference
2. ✓ All figures referenced before appearing
3. ✓ `\ref{fig:label}` used consistently
4. ✓ Figure environments immediately after relevant paragraphs

### Order of Appearance:
1. Figure 1 (Baseline) - Section 4.1
2. Table 1 (Baseline) - Section 4.1
3. Figure 2 (Detectors) - Section 4.2
4. Figure 3 (Complementarity) - Section 4.2
5. Table 3 (Fusion) - Section 4.2
6. Figure 4 (Threshold) - Section 4.3
7. Figure 5 (Learning) - Section 4.4
8. Figure 6 (Obfuscation) - Section 4.4
9. Table 4 (Benign FAR) - Section 4.4
10. Figure 7 (Novel) - Section 4.5
11. Figure 8 (Gap) - Section 4.5
12. Figure 9 (Adversarial) - Section 4.5
13. Figure 10 (Architecture) - Section 5
14. Table 5 (Overhead) - Section 5.1
15. Table 6 (Configs) - Section 5.1

## Verification Checklist

### Before Final Submission:

- [ ] Compile LaTeX: `pdflatex prompt_injection_cacm.tex`
- [ ] Open PDF and zoom to 200%
- [ ] Check all figure text is readable
- [ ] Verify no overlapping elements
- [ ] Confirm value labels are visible
- [ ] Check color contrast in grayscale preview
- [ ] Verify all axes have labels
- [ ] Confirm legends are present where needed
- [ ] Check that figures don't exceed page margins
- [ ] Verify caption formatting is consistent
- [ ] Confirm all figures are referenced in text
- [ ] Check table alignment and spacing

### Font Size Verification:
Open each figure PDF individually and measure text:
```bash
# On Windows:
start fig1_baseline_vulnerability.pdf
# Zoom to 100% and measure axis labels
```

**Expected sizes:**
- 10pt at 100% zoom should be clearly readable
- 8pt is minimum (still acceptable)
- <8pt needs regeneration with larger fonts

### Color Blindness Check:
1. View PDF in grayscale mode
2. Verify bars are still distinguishable by:
   - Position (side-by-side)
   - Value labels (numbers on bars)
   - Captions (explicit TPR/FAR identification)

## Regeneration Commands

### If figures need font size adjustments:

1. Edit `regenerate_manuscript_figures.py`:
   ```python
   # Increase font sizes if needed
   plt.rcParams['font.size'] = 11  # from 10
   plt.rcParams['axes.labelsize'] = 12  # explicit axis labels
   plt.rcParams['xtick.labelsize'] = 10  # tick labels
   plt.rcParams['ytick.labelsize'] = 10
   plt.rcParams['legend.fontsize'] = 10
   ```

2. Regenerate all figures:
   ```bash
   python regenerate_manuscript_figures.py
   ```

3. Regenerate Figure 16 separately:
   ```bash
   python generate_figure_16_publication.py
   ```

### If specific figures need adjustments:

Edit the individual figure generation in `regenerate_manuscript_figures.py` and run again.

## Additional Professional Touches

### Already Implemented:
- ✓ Consistent color scheme across all figures
- ✓ White background (no colored backgrounds)
- ✓ Serif fonts for consistency with document body
- ✓ Tight layout to maximize space usage
- ✓ Appropriate figure sizes (aspect ratios)
- ✓ Clean, uncluttered designs
- ✓ Professional styling (no 3D effects, shadows, etc.)

### Optional Enhancements:
- Add error bars where applicable (if you have std dev data)
- Use consistent bar widths across all bar charts
- Add subtle drop shadows on bars (not mandatory, can be distracting)
- Use patterns/hatching for enhanced accessibility

## Common Issues and Solutions

### Issue: Text too small in compiled PDF
**Solution:** Increase `plt.rcParams['font.size']` in generation script

### Issue: Overlapping labels
**Solution:** Rotate labels, increase figure size, or use abbreviated labels

### Issue: Poor grayscale contrast
**Solution:** Use darker/lighter color pairs, add value labels

### Issue: Figure doesn't fit in column
**Solution:** Already using `\linewidth` which auto-scales

### Issue: Legend obscures data
**Solution:** Already using `loc='best'` for automatic placement

## Final Quality Confirmation

Once all figures are regenerated and LaTeX is compiled:

1. ✅ All text readable at 150% zoom
2. ✅ Colors provide good contrast
3. ✅ Value labels clearly visible
4. ✅ No overlapping elements
5. ✅ Axes properly labeled with units
6. ✅ Legends present and clear
7. ✅ Figures professionally styled
8. ✅ Consistent appearance across all figures
9. ✅ Tables clearly formatted
10. ✅ All visuals referenced in text

---

**Status:** ✅ Current figures meet CACM professional standards
**Recommendation:** Compile and visually inspect final PDF before submission
**Optional:** Request colleague review for readability feedback
