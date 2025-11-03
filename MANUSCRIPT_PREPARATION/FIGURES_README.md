# Figures Generation Guide

**Status:** ✅ **READY FOR FIGURE GENERATION**

---

## QUICK START

```bash
cd FIGURES_GENERATION
python generate_all_figures.py
```

All 20 figures will be generated and saved to `GENERATED_FIGURES/`

---

## FOLDER STRUCTURE

```
MANUSCRIPT_PREPARATION/
├── FIGURES_README.md (this file)
├── FIGURES_GENERATION/
│   ├── generate_all_figures.py          # Master script - generates all 20 figures
│   ├── generate_figure_1.py             # Individual figure scripts
│   ├── generate_figure_2.py
│   ├── ... (all 20 figures)
│   └── generate_figure_20.py
├── FIGURE_DATA/
│   ├── figure_1_data.csv
│   ├── figure_2_data.csv
│   ├── ... (all 20 data files)
│   └── figure_20_data.csv
└── GENERATED_FIGURES/
    ├── figure_1_asr_comparison.png
    ├── figure_2_evasion_heatmap.png
    ├── ... (all generated figures)
    └── figure_20_execution_timeline.png
```

---

## FIGURE SPECIFICATIONS

| # | Title | Type | Data File |
|---|-------|------|-----------|
| 1 | Attack Success Rate Comparison | Bar | figure_1_data.csv |
| 2 | Evasion Technique Heatmap | Heatmap | figure_2_data.csv |
| 3 | Schema Smuggling by Tool | Bar | figure_3_data.csv |
| 4 | Detector Performance | Bar | figure_4_data.csv |
| 5 | Fusion Strategy Comparison | Scatter | figure_5_data.csv |
| 6 | Detector Complementarity | Venn | figure_6_data.csv |
| 7 | Threshold Robustness | Line | figure_7_data.csv |
| 8 | Learned Fusion (Nested CV) | Box | figure_8_data.csv |
| 9 | Lift Over Baseline | Bar | figure_9_data.csv |
| 10 | FAR by Config & Obfuscation | Heatmap | figure_10_data.csv |
| 11 | TPR by Attack Type | Bar | figure_11_data.csv |
| 12 | Coverage Gaps | Radar | figure_12_data.csv |
| 13 | Adversarial Techniques | Bar | figure_13_data.csv |
| 14 | Performance Progression | Line | figure_14_data.csv |
| 15 | Generalization Gap | Bar | figure_15_data.csv |
| 16 | System Architecture | Flow | (manual) |
| 17 | Confusion Matrices | Matrix | figure_17_data.csv |
| 18 | Feature Importance | Bar | figure_18_data.csv |
| 19 | Deployment Comparison | Table | figure_19_data.csv |
| 20 | Execution Timeline | Gantt | figure_20_data.csv |

---

## HOW TO USE

### Generate All Figures at Once:
```bash
python FIGURES_GENERATION/generate_all_figures.py
```

### Generate Individual Figure:
```bash
python FIGURES_GENERATION/generate_figure_1.py
```

### Output Location:
All figures saved to: `GENERATED_FIGURES/`

---

## REQUIREMENTS

```
matplotlib>=3.5.0
seaborn>=0.12.0
pandas>=1.5.0
numpy>=1.23.0
scipy>=1.9.0
```

Install with:
```bash
pip install -r FIGURES_GENERATION/requirements.txt
```

---

## FIGURE DESCRIPTIONS

### Figure 1: Attack Success Rate Comparison
- **Type:** Grouped bar chart
- **Shows:** ASR for LLaMA-2 (65%, 31.58%) vs Falcon-7b (5%, 26.32%)
- **Key Insight:** LLaMA-2 is 13x more vulnerable to RAG-borne attacks

### Figure 2: Evasion Technique Heatmap
- **Type:** 2D heatmap
- **Shows:** Effectiveness of 8 evasion techniques across 2 models
- **Key Insight:** Plain, delimiter, role confusion = 100% on LLaMA-2; Homoglyph = 0%

### Figure 3: Schema Smuggling by Tool
- **Type:** Grouped bar chart
- **Shows:** Vulnerability of 3 tools (HTTP GET, DB Query, Email)
- **Key Insight:** HTTP GET universally vulnerable (100%)

### Figure 4: Detector Performance
- **Type:** Grouped bar chart with error bars
- **Shows:** TPR and FAR for v1, v2, v3 with 95% CI
- **Key Insight:** v1 is most effective (80% TPR, 0% FAR)

### Figure 5: Fusion Strategy Comparison
- **Type:** Scatter plot
- **Shows:** TPR vs FAR for 10 fusion configurations
- **Key Insight:** v1+v3 (OR) optimal at 87% TPR, 0% FAR

### Figure 6: Detector Complementarity
- **Type:** Venn diagram or stacked bar
- **Shows:** Attack coverage by detector
- **Key Insight:** v1+v3 catches 174/200 (87%) through complementarity

### Figure 7: Threshold Robustness
- **Type:** Line chart
- **Shows:** TPR and FAR across 15 thresholds (0.05-0.75)
- **Key Insight:** Threshold-invariant performance (all identical)

### Figure 8: Learned Fusion (Nested CV)
- **Type:** Box plot with CI
- **Shows:** Nested CV results across 5 folds
- **Key Insight:** Mean TPR 99%, 95% CI [95%, 100%]

### Figure 9: Lift Over Baseline
- **Type:** Bar chart
- **Shows:** Improvement Phase 3 → Phase 5
- **Key Insight:** 87% → 99% TPR (+12pp, +24 attacks)

### Figure 10: FAR by Configuration & Obfuscation
- **Type:** 2D heatmap
- **Shows:** FAR across 6 configs × 8 obfuscation types
- **Key Insight:** Normalizer+v3 = 0.77% FAR (goal achieved)

### Figure 11: TPR by Attack Type
- **Type:** Grouped bar chart
- **Shows:** Detection rate for 6 novel attack types
- **Key Insight:** Instruction Embedding (95%), Context Confusion (25%)

### Figure 12: Coverage Gaps
- **Type:** Radar chart or stacked bar
- **Shows:** Coverage vs gaps for each attack type
- **Key Insight:** Multi-turn (40%), Context confusion (25%) are gaps

### Figure 13: Adversarial Techniques
- **Type:** Horizontal bar chart
- **Shows:** Evasion rates for 5 adversarial techniques
- **Key Insight:** Multi-step (75%), Paraphrasing (60%)

### Figure 14: Performance Progression
- **Type:** Line chart with markers
- **Shows:** TPR across all 8 phases
- **Key Insight:** 65% → 87% → 99% → 49.2% (generalization gap)

### Figure 15: Generalization Gap
- **Type:** Grouped bar chart
- **Shows:** Phase 1 (87%) vs Novel (49.2%) vs Adversarial (53.1%)
- **Key Insight:** 50 percentage point gap

### Figure 16: System Architecture
- **Type:** Flow diagram
- **Shows:** Data flow through system components
- **Note:** Manual creation recommended (use ARCHITECTURE_VISUALIZATION.md)

### Figure 17: Confusion Matrices
- **Type:** 3 confusion matrices side-by-side
- **Shows:** TP, FP, TN, FN for v1, v2, v3
- **Key Insight:** v1 has best accuracy (90%)

### Figure 18: Feature Importance
- **Type:** Horizontal bar chart
- **Shows:** Feature weights in learned fusion model
- **Key Insight:** v1.is_attack (0.45), v3.is_attack (0.35) dominate

### Figure 19: Deployment Comparison
- **Type:** Comparison table
- **Shows:** Normalizer+v3 vs Normalizer+v1+v3
- **Key Insight:** Production vs Monitoring tradeoff

### Figure 20: Execution Timeline
- **Type:** Gantt chart
- **Shows:** Execution time for each phase
- **Key Insight:** Total ~7.33 hours

---

## DATA FILES INCLUDED

All CSV files are pre-formatted with exact data from experiments:
- `figure_1_data.csv` - ASR comparison data
- `figure_2_data.csv` - Evasion technique matrix
- ... (all 20 data files)

Ready to use with provided Python scripts.

---

## CUSTOMIZATION

### Change Output Format:
Edit `FIGURES_GENERATION/generate_all_figures.py`:
```python
# Change from PNG to PDF
plt.savefig(f'figure_{i}.pdf', dpi=300, bbox_inches='tight')
```

### Change Output Directory:
```python
OUTPUT_DIR = 'GENERATED_FIGURES'  # Change this path
```

### Change Figure Size:
```python
plt.figure(figsize=(10, 6))  # Adjust width, height
```

---

## TROUBLESHOOTING

### ImportError: No module named 'matplotlib'
```bash
pip install matplotlib seaborn pandas numpy scipy
```

### Figures not generating
- Check that CSV files exist in `FIGURE_DATA/`
- Verify Python version (3.7+)
- Check file permissions

### Low resolution figures
- Increase DPI in script: `dpi=300` (default) → `dpi=600`
- Increase figure size: `figsize=(10, 6)` → `figsize=(12, 8)`

---

## NEXT STEPS

1. **Install requirements:**
   ```bash
   pip install -r FIGURES_GENERATION/requirements.txt
   ```

2. **Generate all figures:**
   ```bash
   python FIGURES_GENERATION/generate_all_figures.py
   ```

3. **Verify output:**
   - Check `GENERATED_FIGURES/` folder
   - All 20 PNG files should be present

4. **Insert into manuscript:**
   - Use figure references from methods documents
   - Place figures at referenced locations
   - Add captions from specifications

---

**Status:** ✅ **READY TO GENERATE FIGURES**

All data and scripts are in place. Run `generate_all_figures.py` to create publication-ready figures.
