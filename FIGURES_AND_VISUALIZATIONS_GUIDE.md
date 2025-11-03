# Figures and Visualizations Guide

**Project:** Prompt Injection Security: Multi-Phase Evaluation Framework  
**Date:** November 3, 2025  
**Status:** ✅ **FIGURE SPECIFICATIONS FOR PUBLICATION**

---

## OVERVIEW

This document specifies 20 figures needed for publication. Each includes:
- Description and purpose
- Data source (CSV file)
- Visualization type
- Key metrics
- Recommended dimensions

---

## FIGURE SPECIFICATIONS

### FIGURE 1: Attack Success Rate Comparison
**Type:** Grouped Bar Chart  
**Purpose:** Compare vulnerability between LLaMA-2 and Falcon-7b  
**Data:** RAG-Borne (65%, 5%), Schema Smuggling (31.58%, 26.32%)  
**Insight:** LLaMA-2 is 13x more vulnerable to RAG-borne attacks  
**Dimensions:** 800x500px

### FIGURE 2: Evasion Technique Effectiveness Heatmap
**Type:** Heatmap (2D grid)  
**Purpose:** Show effectiveness of 8 evasion techniques across 2 models  
**Data:** 8 techniques × 2 models with ASR percentages  
**Insight:** Plain, delimiter, role confusion = 100% on LLaMA-2; Homoglyph = 0% on both  
**Dimensions:** 600x400px

### FIGURE 3: Schema Smuggling by Tool
**Type:** Grouped Bar Chart  
**Purpose:** Show vulnerability of 3 tools  
**Data:** HTTP GET (100%), DB Query (50%), Email (13-21%)  
**Insight:** HTTP GET universally vulnerable  
**Dimensions:** 700x450px

### FIGURE 4: Detector Performance Comparison
**Type:** Grouped Bar Chart with Error Bars  
**Purpose:** Compare TPR and FAR across v1, v2, v3  
**Data:** v1 (80% TPR, 0% FAR), v2 (44%, 0%), v3 (57%, 0%)  
**Insight:** v1 is most effective  
**Dimensions:** 800x500px

### FIGURE 5: Fusion Strategy Comparison
**Type:** Scatter Plot  
**Purpose:** Show TPR vs FAR for 10 configurations  
**Data:** 10 fusion strategies plotted  
**Insight:** v1+v3 (OR) optimal at 87% TPR, 0% FAR  
**Dimensions:** 800x600px

### FIGURE 6: Detector Complementarity
**Type:** Venn Diagram or Stacked Bar  
**Purpose:** Show how v1 and v3 catch different attacks  
**Data:** v1 only (6), v3 only (0), both (168), neither (26)  
**Insight:** v1+v3 catches 174/200 (87%)  
**Dimensions:** 700x500px

### FIGURE 7: Threshold Robustness
**Type:** Line Chart  
**Purpose:** Show TPR/FAR across 15 thresholds (0.05-0.75)  
**Data:** All thresholds yield 87% TPR, 0% FAR  
**Insight:** Threshold-invariant performance  
**Dimensions:** 900x500px

### FIGURE 8: Learned Fusion (Nested CV)
**Type:** Box Plot with CI  
**Purpose:** Show nested CV results  
**Data:** Mean TPR 99%, 95% CI [95%, 100%]  
**Insight:** Consistent across folds  
**Dimensions:** 700x500px

### FIGURE 9: Lift Over Baseline
**Type:** Bar Chart  
**Purpose:** Show improvement Phase 3 → Phase 5  
**Data:** 87% → 99% TPR (+12pp, +24 attacks)  
**Insight:** Learned fusion catches 24 additional attacks  
**Dimensions:** 600x400px

### FIGURE 10: FAR by Configuration & Obfuscation Type
**Type:** Heatmap  
**Purpose:** Show FAR across 6 configs × 8 obfuscation types  
**Data:** Normalizer+v3 = 0.77% FAR (best)  
**Insight:** Normalizer fixes homoglyphs (100% → 0% FAR)  
**Dimensions:** 1000x500px

### FIGURE 11: TPR by Attack Type (Novel)
**Type:** Grouped Bar Chart  
**Purpose:** Show detection rate for 6 novel attack types  
**Data:** Instruction Embedding (95%), Context Confusion (25%)  
**Insight:** Significant coverage gaps identified  
**Dimensions:** 900x500px

### FIGURE 12: Coverage Gaps (Novel Attacks)
**Type:** Radar Chart or Stacked Bar  
**Purpose:** Visualize coverage gaps  
**Data:** Multi-turn (40%), Context confusion (25%)  
**Insight:** Critical gaps in multi-turn and context confusion  
**Dimensions:** 700x700px (radar) or 800x500px (stacked)

### FIGURE 13: Adversarial Technique Effectiveness
**Type:** Horizontal Bar Chart  
**Purpose:** Show evasion rates for 5 adversarial techniques  
**Data:** Multi-step (75%), Paraphrasing (60%)  
**Insight:** Multi-step instructions most effective  
**Dimensions:** 700x400px

### FIGURE 14: Cross-Phase Performance Progression
**Type:** Line Chart with Markers  
**Purpose:** Show TPR improvement across all 8 phases  
**Data:** Phase 1 (65%), Phase 2 (80%), Phase 3 (87%), Phase 5 (99%), Phase 6b (49.2%)  
**Insight:** Generalization gap revealed in Phase 6b  
**Dimensions:** 1000x600px

### FIGURE 15: Generalization Gap Analysis
**Type:** Grouped Bar Chart  
**Purpose:** Highlight performance drop from Phase 1 to novel/adversarial  
**Data:** Phase 1 (87%), Novel (49.2%), Adversarial (53.1%)  
**Insight:** 50 percentage point gap  
**Dimensions:** 700x500px

### FIGURE 16: System Architecture Diagram
**Type:** Flow Diagram  
**Purpose:** Show data flow through components  
**Data:** Input → Normalizer → Detectors → Fusion → Decision  
**Insight:** Clear component hierarchy  
**Dimensions:** 1000x600px

### FIGURE 17: Confusion Matrices (Phase 2)
**Type:** 3x Confusion Matrices  
**Purpose:** Show TP, FP, TN, FN for v1, v2, v3  
**Data:** v1 (160 TP, 0 FP), v2 (88 TP, 0 FP), v3 (114 TP, 0 FP)  
**Insight:** v1 has best accuracy  
**Dimensions:** 900x300px

### FIGURE 18: Feature Importance (Learned Fusion)
**Type:** Horizontal Bar Chart  
**Purpose:** Show which features contribute most  
**Data:** v1.is_attack (0.45), v3.is_attack (0.35), others (0.20)  
**Insight:** Detector outputs dominate  
**Dimensions:** 800x600px

### FIGURE 19: Deployment Recommendation Summary
**Type:** Comparison Table  
**Purpose:** Compare Normalizer+v3 vs Normalizer+v1+v3  
**Data:** TPR (87% both), FAR (0.77% vs 12.3%), TPR Novel (44.2% vs 49.2%)  
**Insight:** Production vs Monitoring tradeoff  
**Dimensions:** 900x400px

### FIGURE 20: Execution Timeline
**Type:** Gantt Chart  
**Purpose:** Show execution time for each phase  
**Data:** Phase 1 (4.0 hrs), Phase 2 (0.5 hrs), ... Phase 6c (0.5 hrs)  
**Insight:** Total ~7.33 hours  
**Dimensions:** 800x400px

---

## SUMMARY TABLE

| # | Title | Type | Data Source | Dimensions |
|---|-------|------|-------------|-----------|
| 1 | ASR Comparison | Bar | partA/B_results.json | 800x500 |
| 2 | Evasion Heatmap | Heatmap | partA_results.json | 600x400 |
| 3 | Schema Smuggling | Bar | partB_results.json | 700x450 |
| 4 | Detector Performance | Bar | input_detection_metrics.csv | 800x500 |
| 5 | Fusion Comparison | Scatter | evaluate_fusion.py | 800x600 |
| 6 | Complementarity | Venn | evaluate_fusion.py | 700x500 |
| 7 | Threshold Robustness | Line | threshold_sweep.csv | 900x500 |
| 8 | Learned Fusion CV | Box | fusion_threshold_sweep_cv.csv | 700x500 |
| 9 | Lift Over Baseline | Bar | Phase 3 + 5 | 600x400 |
| 10 | FAR Heatmap | Heatmap | obfuscated_benign_metrics.csv | 1000x500 |
| 11 | Novel Attack TPR | Bar | attack_type_analysis.csv | 900x500 |
| 12 | Coverage Gaps | Radar | attack_type_analysis.csv | 700x700 |
| 13 | Adversarial Tech | Bar | technique_effectiveness.csv | 700x400 |
| 14 | Performance Progression | Line | All phases | 1000x600 |
| 15 | Generalization Gap | Bar | Phases 5,6b,6c | 700x500 |
| 16 | Architecture | Flow | ARCHITECTURE_VISUALIZATION.md | 1000x600 |
| 17 | Confusion Matrices | Matrix | input_detection_metrics.csv | 900x300 |
| 18 | Feature Importance | Bar | feature_importance.csv | 800x600 |
| 19 | Deployment Comparison | Table | Phase 6a + 6b | 900x400 |
| 20 | Execution Timeline | Gantt | Execution logs | 800x400 |

---

## PYTHON GENERATION TEMPLATE

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Figure 1: Attack Success Rate Comparison
data = {
    'Attack Vector': ['RAG-Borne', 'Schema Smuggling'],
    'LLaMA-2': [65, 31.58],
    'Falcon-7b': [5, 26.32]
}
df = pd.DataFrame(data)
df.set_index('Attack Vector').plot(kind='bar', figsize=(8, 5))
plt.ylabel('Attack Success Rate (%)')
plt.title('Figure 1: Attack Success Rate Comparison')
plt.tight_layout()
plt.savefig('figure1_asr_comparison.png', dpi=300)
```

---

## PUBLICATION CHECKLIST

- [ ] Generate all 20 figures
- [ ] Verify data accuracy
- [ ] Use consistent color scheme
- [ ] Add figure captions
- [ ] Include figure references in text
- [ ] Ensure 300 DPI for print
- [ ] Test readability at publication size
- [ ] Create figure legend
- [ ] Verify all labels and units

---

**Status:** ✅ **FIGURE SPECIFICATIONS COMPLETE**  
**Ready for:** Visualization generation
