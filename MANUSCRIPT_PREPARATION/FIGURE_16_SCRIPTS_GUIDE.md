# Figure 16 Generation Scripts - Guide

## ✅ **ALL SCRIPTS NOW FIXED**

All 8 Figure 16 generation scripts have been updated to remove the "Figure 16:" prefix from titles.

## 📋 **Available Scripts**

| Script | Purpose | Status | Recommended |
|--------|---------|--------|-------------|
| `generate_figure_16_publication.py` | **PUBLICATION VERSION** - 16x11", best spacing | ✅ Fixed | ⭐ **USE THIS ONE** |
| `generate_figure_16_final_optimized.py` | Optimized version with improved layout | ✅ Fixed | Alternative |
| `generate_figure_16_optimized.py` | Earlier optimized version | ✅ Fixed | - |
| `generate_figure_16_final.py` | Final version (before optimization) | ✅ Fixed | - |
| `generate_figure_16_enhanced.py` | Enhanced version with better colors | ✅ Fixed | - |
| `generate_figure_16_corrected.py` | Corrected spacing issues | ✅ Fixed | - |
| `generate_figure_16_centered.py` | Centered layout version | ✅ Fixed | - |
| `generate_figure_16.py` | Original version | ✅ Fixed | - |

## 🎯 **Recommended Usage**

### **For Manuscript (CACM Submission):**
```bash
python generate_figure_16_publication.py
```

**This generates:**
- `fig16_architecture.pdf` (for LaTeX)
- `GENERATED_FIGURES/figure_16_system_architecture.png` (backup)

**Features:**
- 16x11 inch size (publication-ready)
- No "Figure 16:" in title
- Professional spacing
- Clear visual hierarchy
- No overlapping elements

## ✨ **What Was Fixed**

### Before (ALL scripts):
```python
ax.text(8, 10.6, 'Figure 16: Prompt Injection Detection Pipeline Architecture', ...)
```

### After (ALL scripts NOW):
```python
ax.text(8, 10.6, 'Prompt Injection Detection Pipeline Architecture', ...)
```

## 🔍 **How to Verify**

Check the title in the generated PDF:
```bash
# Generate the figure
python generate_figure_16_publication.py

# Open the PDF
start fig16_architecture.pdf
```

**What you should see:**
- ✅ Title: "Prompt Injection Detection Pipeline Architecture"
- ❌ NOT: "Figure 16: Prompt Injection Detection Pipeline Architecture"

## 📝 **Output Files**

When you run `generate_figure_16_publication.py`:

1. **`fig16_architecture.pdf`** 
   - In: `MANUSCRIPT_PREPARATION/` directory
   - Used by: LaTeX `\includegraphics{fig16_architecture.pdf}`
   - Purpose: Main manuscript figure

2. **`figure_16_system_architecture.png`**
   - In: `MANUSCRIPT_PREPARATION/GENERATED_FIGURES/` directory
   - Purpose: Backup/preview version

## 🚫 **Common Mistake**

Don't use multiple scripts randomly. They were created during iterative development to fix various issues:
- Spacing problems
- Overlapping text
- Size issues
- Layout improvements

**Always use:** `generate_figure_16_publication.py` (the final, best version)

## ✅ **Verification Checklist**

After generating Figure 16:

- [ ] PDF file exists: `fig16_architecture.pdf`
- [ ] No "Figure 16:" in the figure title
- [ ] No overlapping text
- [ ] All sections clearly separated
- [ ] Figure is 16x11 inches
- [ ] Professional appearance

## 🔄 **Regeneration**

If you need to regenerate Figure 16 for any reason:

```bash
cd "c:\Users\carlo\OneDrive - VIDENS ANALYTICS\Prompt Injection Security\MANUSCRIPT_PREPARATION"
python generate_figure_16_publication.py
```

This will overwrite:
- `fig16_architecture.pdf` (main file for manuscript)

## 📦 **Cleanup (Optional)**

If you want to clean up the old version scripts (keep only the publication one):

```bash
# Keep these:
# - generate_figure_16_publication.py (REQUIRED)

# Can delete (if desired):
# - generate_figure_16_final_optimized.py
# - generate_figure_16_optimized.py
# - generate_figure_16_final.py
# - generate_figure_16_enhanced.py
# - generate_figure_16_corrected.py
# - generate_figure_16_centered.py
# - generate_figure_16.py
```

**But all are now fixed, so keeping them won't cause issues.**

---

**Last Updated:** 2025-11-04
**Status:** All 8 scripts fixed ✅
**Recommended:** Use `generate_figure_16_publication.py`
