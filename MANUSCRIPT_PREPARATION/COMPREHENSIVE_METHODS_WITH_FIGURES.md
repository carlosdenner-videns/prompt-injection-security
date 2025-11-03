# Comprehensive Methods and Results with Embedded Figures

**Project:** Prompt Injection Security: Multi-Phase Evaluation Framework  
**Date:** October 30 - November 1, 2025  
**Status:** ✅ **COMPLETE - ALL 8 PHASES WITH FIGURES**

---

## FIGURE INSERTION GUIDE

This document provides the locations where each figure should be inserted into the comprehensive methods documents.

### PART 1: PHASES 1-4 (COMPREHENSIVE_METHODS_AND_RESULTS_PART1.md)

---

## PHASE 1: BASELINE VULNERABILITY ASSESSMENT

### After "Key Finding: LLaMA-2 is 13x more vulnerable." (Line ~91)

**INSERT: Figure 1 - Attack Success Rate Comparison**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_1_asr_comparison.png
Caption: Figure 1: Attack Success Rate Comparison. Bar chart showing vulnerability 
comparison between LLaMA-2-7b (65% RAG-borne, 31.58% schema smuggling) and 
Falcon-7b (5% RAG-borne, 26.32% schema smuggling). LLaMA-2 is 13x more vulnerable 
to RAG-borne injection attacks.
```

---

### After "Vulnerability by Evasion Type (LLaMA-2-7b):" table (Line ~108)

**INSERT: Figure 2 - Evasion Technique Effectiveness Heatmap**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_2_evasion_heatmap.png
Caption: Figure 2: Evasion Technique Effectiveness Heatmap. 2D heatmap showing 
effectiveness of 8 evasion techniques across LLaMA-2-7b and Falcon-7b. Plain text, 
delimiter, and role confusion attacks achieve 100% success on LLaMA-2, while 
homoglyph and unicode obfuscation are completely ineffective (0%) on both models.
```

---

### After "Vulnerability by Tool:" table in Part B (Line ~145)

**INSERT: Figure 3 - Schema Smuggling by Tool**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_3_schema_smuggling.png
Caption: Figure 3: Schema Smuggling Vulnerability by Tool. Grouped bar chart showing 
vulnerability of three tools to schema smuggling attacks. HTTP GET endpoints are 
universally vulnerable (100%), database queries show 50% vulnerability, and email 
validation is relatively strong (13-21% vulnerability).
```

---

## PHASE 2: INPUT-SIDE DETECTION DEVELOPMENT

### After "Performance Metrics:" table (Line ~220)

**INSERT: Figure 4 - Detector Performance Comparison**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_4_detector_performance.png
Caption: Figure 4: Detector Performance Comparison. Grouped bar chart with error bars 
showing TPR and FAR for v1, v2, and v3 detectors with 95% Wilson confidence intervals. 
v1 (signature-based) achieves 80% TPR with 0% FAR, outperforming v2 (44% TPR) and 
v3 (57% TPR).
```

---

### After "Complementarity Analysis:" table (Line ~302)

**INSERT: Figure 6 - Detector Complementarity**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_6_complementarity.png
Caption: Figure 6: Detector Complementarity Analysis. Stacked bar chart showing how 
v1 and v3 catch different attacks. v1 alone catches 160/200 (80%), v3 alone catches 
114/200 (57%), but together (v1+v3) catch 174/200 (87%) through complementary strengths.
```

---

### After "Phase 2 Output Files" section (Line ~234)

**INSERT: Figure 17 - Confusion Matrices**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_17_confusion_matrices.png
Caption: Figure 17: Confusion Matrices (Phase 2 Detectors). Three confusion matrices 
showing TP, FP, TN, FN for v1, v2, and v3 detectors. v1 achieves 90% accuracy with 
160 TP and 0 FP. v2 achieves 72% accuracy, and v3 achieves 78.5% accuracy.
```

---

## PHASE 3: MULTILAYER DEFENSE OPTIMIZATION

### After "Performance by Configuration:" table (Line ~287)

**INSERT: Figure 5 - Fusion Strategy Comparison**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_5_fusion_comparison.png
Caption: Figure 5: Fusion Strategy Comparison. Scatter plot showing TPR vs FAR for 
10 fusion configurations. v1+v3 (OR fusion) is optimal at 87% TPR, 0% FAR (highlighted 
in red). AND fusion is too conservative (44% TPR), while WEIGHTED fusion achieves 
85% TPR but is suboptimal compared to v1+v3.
```

---

### After "Complementarity Analysis:" section (Line ~302)

**INSERT: Figure 6 - Detector Complementarity** (Already referenced above)

---

## PHASE 4: THRESHOLD ROBUSTNESS ANALYSIS

### After "Result: All thresholds yield identical metrics" table (Line ~343)

**INSERT: Figure 7 - Threshold Robustness**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_7_threshold_robustness.png
Caption: Figure 7: Threshold Robustness (Threshold-Invariant Performance). Line chart 
showing TPR and FAR across 15 thresholds (0.05-0.75). All thresholds yield identical 
metrics (87% TPR, 0% FAR), demonstrating threshold-invariant performance due to binary 
OR fusion logic.
```

---

### PART 2: PHASES 5-8 (COMPREHENSIVE_METHODS_AND_RESULTS_PART2.md)

---

## PHASE 5: OBFUSCATION HARDENING & LEARNED FUSION

### After "Phase 1 Performance (Nested CV):" table (Line ~66)

**INSERT: Figure 8 - Learned Fusion (Nested CV)**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_8_learned_fusion_cv.png
Caption: Figure 8: Learned Fusion Performance (Nested CV). Box plot with confidence 
intervals showing nested cross-validation results across 5 folds. Mean TPR is 99% 
with 95% CI [95%, 100%], demonstrating consistent performance across folds with no 
overfitting to specific folds.
```

---

### After "Lift vs Phase 3 Baseline:" section (Line ~71)

**INSERT: Figure 9 - Lift Over Baseline**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_9_lift_baseline.png
Caption: Figure 9: Lift Over Baseline (Phase 3 → Phase 5). Bar chart showing 
improvement from Phase 3 (87% TPR) to Phase 5 (99% TPR), representing a +12 
percentage point improvement and +24 additional attacks caught.
```

---

## PHASE 6A: OBFUSCATION-BENIGN VALIDATION

### After "False Alarm Rate by Configuration:" table (Line ~132)

**INSERT: Figure 10 - FAR by Configuration & Obfuscation**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_10_far_heatmap.png
Caption: Figure 10: FAR by Configuration and Obfuscation Type. 2D heatmap showing 
FAR across 6 configurations and 8 obfuscation types. Normalizer+v3 achieves 0.77% 
FAR (goal achieved), with homoglyph handling improved from 100% FAR to 0% FAR 
through normalizer processing.
```

---

## PHASE 6B: NOVEL ATTACK VALIDATION

### After "TPR by Configuration:" table (Line ~214)

**INSERT: Figure 11 - TPR by Attack Type**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_11_tpr_attack_type.png
Caption: Figure 11: TPR by Attack Type (Novel Attacks). Horizontal bar chart showing 
detection rate for 6 novel attack types. Instruction embedding achieves 95% TPR 
(best), while context confusion achieves only 25% TPR (worst), revealing critical 
coverage gaps.
```

---

### After "TPR by Attack Type (Normalizer+v1+v3):" table (Line ~225)

**INSERT: Figure 12 - Coverage Gaps**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_12_coverage_gaps.png
Caption: Figure 12: Coverage Gaps by Attack Type. Stacked bar chart showing coverage 
vs gaps for each novel attack type. Multi-turn manipulation (40% TPR) and context 
confusion (25% TPR) represent critical gaps requiring future work.
```

---

## PHASE 6C: ADVERSARIAL ROBUSTNESS

### After "Adversarial Technique Effectiveness:" table (Line ~304)

**INSERT: Figure 13 - Adversarial Techniques**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_13_adversarial_techniques.png
Caption: Figure 13: Adversarial Technique Effectiveness. Horizontal bar chart showing 
evasion rates for 5 adversarial techniques. Multi-step instructions achieve 75% 
evasion (most effective), while paraphrasing achieves 60% evasion (least effective).
```

---

## CROSS-PHASE ANALYSIS

### After "Performance Progression" table (Line ~347)

**INSERT: Figure 14 - Performance Progression**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_14_performance_progression.png
Caption: Figure 14: Cross-Phase Performance Progression. Line chart showing TPR 
across all 8 phases. Performance improves from 65% (Phase 1) to 87% (Phase 3) to 
99% (Phase 5), then drops to 49.2% (Phase 6b) on novel attacks, revealing the 
generalization gap.
```

---

### After "Generalization Gap Analysis:" section (Line ~360)

**INSERT: Figure 15 - Generalization Gap**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_15_generalization_gap.png
Caption: Figure 15: Generalization Gap Analysis. Grouped bar chart highlighting 
performance drop from Phase 1 (87% TPR) to novel attacks (49.2% TPR) and adversarial 
attacks (53.1% TPR), revealing a 50 percentage point gap between known and novel 
attacks.
```

---

### In ARCHITECTURE_VISUALIZATION.md or Methods Section

**INSERT: Figure 16 - System Architecture**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_16_system_architecture.png
Caption: Figure 16: System Architecture - Prompt Injection Detection Pipeline. Flow 
diagram showing data flow through system components: Input → Normalizer → Detectors 
(v1, v2, v3) → Fusion (OR Logic) → Decision. Includes performance metrics (87% TPR, 
0.77% FAR, <0.1ms latency) and data flow examples.
```

---

## CONCLUSIONS & RECOMMENDATIONS

### After "Key Metrics Summary" table (Line ~~)

**INSERT: Figure 18 - Feature Importance**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_18_feature_importance.png
Caption: Figure 18: Feature Importance (Learned Fusion Model). Horizontal bar chart 
showing feature weights in the learned fusion model. v1.is_attack (0.45) and 
v3.is_attack (0.35) dominate, accounting for 80% of model importance.
```

---

### In Deployment Recommendations Section

**INSERT: Figure 19 - Deployment Comparison**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_19_deployment_comparison.png
Caption: Figure 19: Deployment Configuration Comparison. Comparison table showing 
two recommended configurations: Normalizer+v3 for production (87% TPR, 0.77% FAR) 
vs Normalizer+v1+v3 for monitoring (87% TPR, 49.2% novel TPR, 12.3% FAR).
```

---

### In Appendix or Supplementary Materials

**INSERT: Figure 20 - Execution Timeline**
```
File: MANUSCRIPT_PREPARATION/GENERATED_FIGURES/figure_20_execution_timeline.png
Caption: Figure 20: Execution Timeline by Phase. Gantt-style chart showing execution 
time for each phase. Phase 1 dominates with 4.0 hours (LLaMA-2 + Falcon-7b testing), 
while other phases range from 0.25-0.75 hours, totaling ~7.33 hours.
```

---

## SUMMARY: ALL 20 FIGURES

| # | Figure | Location | File |
|---|--------|----------|------|
| 1 | Attack Success Rate | Phase 1 Results | figure_1_asr_comparison.png |
| 2 | Evasion Heatmap | Phase 1 Evasion Table | figure_2_evasion_heatmap.png |
| 3 | Schema Smuggling | Phase 1 Part B | figure_3_schema_smuggling.png |
| 4 | Detector Performance | Phase 2 Metrics | figure_4_detector_performance.png |
| 5 | Fusion Comparison | Phase 3 Configurations | figure_5_fusion_comparison.png |
| 6 | Complementarity | Phase 3 Analysis | figure_6_complementarity.png |
| 7 | Threshold Robustness | Phase 4 Results | figure_7_threshold_robustness.png |
| 8 | Learned Fusion CV | Phase 5 Performance | figure_8_learned_fusion_cv.png |
| 9 | Lift Baseline | Phase 5 Lift | figure_9_lift_baseline.png |
| 10 | FAR Heatmap | Phase 6a Results | figure_10_far_heatmap.png |
| 11 | TPR Attack Type | Phase 6b Results | figure_11_tpr_attack_type.png |
| 12 | Coverage Gaps | Phase 6b Analysis | figure_12_coverage_gaps.png |
| 13 | Adversarial Tech | Phase 6c Results | figure_13_adversarial_techniques.png |
| 14 | Performance Progression | Cross-Phase | figure_14_performance_progression.png |
| 15 | Generalization Gap | Cross-Phase | figure_15_generalization_gap.png |
| 16 | System Architecture | Architecture | figure_16_system_architecture.png |
| 17 | Confusion Matrices | Phase 2 Detail | figure_17_confusion_matrices.png |
| 18 | Feature Importance | Conclusions | figure_18_feature_importance.png |
| 19 | Deployment Comparison | Recommendations | figure_19_deployment_comparison.png |
| 20 | Execution Timeline | Appendix | figure_20_execution_timeline.png |

---

## INSERTION INSTRUCTIONS

1. **Open** COMPREHENSIVE_METHODS_AND_RESULTS_PART1.md and PART2.md
2. **Locate** each figure reference (marked with "See Figure X:")
3. **Insert** the corresponding PNG file from GENERATED_FIGURES/
4. **Add** the caption from this guide
5. **Format** with appropriate figure numbering and captions

All figures are 300 DPI PNG files, publication-ready.

---

**Status:** ✅ **ALL 20 FIGURES GENERATED & LOCATION GUIDE COMPLETE**
