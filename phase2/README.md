# Phase 2: Defense Development and Evaluation

This folder contains the defense development pipeline for prompt injection attacks, building on Phase 1's baseline vulnerability assessment.

## Folder Structure

```
phase2/
├── data/              # Input data and annotations
│   └── (populated by scripts)
├── scripts/           # Phase 2 scripts
│   ├── prompt_injection_classifier.py  # Classifier v1, v2, v3
│   ├── evaluate_classifiers.py         # Evaluation pipeline
│   ├── annotation_updater.py           # Update Phase 1 annotations
│   └── ablation_analysis.py            # Ablation study
├── results/           # Evaluation results
│   ├── classifier_metrics.csv
│   ├── detections_v1.csv
│   ├── detections_v2.csv
│   ├── detections_v3.csv
│   └── ablation_results.csv
├── plots/             # Visualizations
│   ├── classifier_comparison.png
│   ├── confusion_matrix.png
│   └── defense_overlap.png
└── README.md          # This file
```

## Objectives

### 1. Iterative Classifier Development (v1 → v3)

**Version 1 (v1): Minimal Keywords**
- Obvious keywords: "ignore", "DAN", "developer mode", etc.
- Baseline detection performance
- Expected TPR: ~40-50%

**Version 2 (v2): Phase 1 Patterns**
- Adds patterns from Phase 1 evasion types
- Delimiter attacks, role confusion, multilingual variants
- Expected TPR: ~60-70%

**Version 3 (v3): Enhanced Logic**
- Weighted patterns
- Regex for character obfuscation (ZWJ, homoglyphs)
- Pattern combinations
- Expected TPR: ~75-85%

### 2. Evaluation Metrics

- **TPR (True Positive Rate)**: Detection rate on actual attacks
- **FAR (False Alarm Rate)**: False positive rate on benign prompts
- **Accuracy**: Overall correctness
- **Precision**: Reliability of positive predictions
- **F1 Score**: Harmonic mean of precision and recall
- **Wilson 95% CI**: Confidence intervals for all rates

### 3. Ablation Study

Analyze defense combinations:
- Signature-only (canary token detection)
- Rules-only (classifier)
- Signature + Rules (combined)
- Identify complementary strengths

### 4. Baseline Comparisons

- NeMo Guardrails default rules
- OpenAI Moderation API
- Published heuristic filters

## Running Phase 2

### Quick Start

```bash
# From root directory
python phase2/scripts/evaluate_classifiers.py

# Or from phase2 directory
cd phase2
python scripts/evaluate_classifiers.py
```

### Step-by-Step

#### Step 1: Evaluate Classifiers
```bash
python phase2/scripts/evaluate_classifiers.py
```
**Output**: 
- `phase2/results/classifier_metrics.csv` - Performance metrics for v1, v2, v3
- `phase2/results/detections_v1.csv` - Detailed detections from v1
- `phase2/results/detections_v2.csv` - Detailed detections from v2
- `phase2/results/detections_v3.csv` - Detailed detections from v3

#### Step 2: Update Phase 1 Annotations
```bash
python phase2/scripts/annotation_updater.py
```
**Output**: 
- `phase1/data/phase1_output_annotated_with_defenses.json` - Updated with defense results

#### Step 3: Run Ablation Study
```bash
python phase2/scripts/ablation_analysis.py
```
**Output**:
- `phase2/results/ablation_results.csv` - Ablation study results
- `phase2/plots/defense_overlap.png` - Venn diagram of defense coverage

#### Step 4: Generate Visualizations
```bash
python phase2/scripts/generate_plots.py
```
**Output**:
- `phase2/plots/classifier_comparison.png` - TPR/FAR comparison
- `phase2/plots/confusion_matrix.png` - Confusion matrices for each version

## Key Findings (Expected)

### Classifier Performance Progression

| Metric | v1 | v2 | v3 |
|--------|----|----|-----|
| TPR | ~45% | ~65% | ~80% |
| FAR | ~5% | ~8% | ~10% |
| F1 | ~0.60 | ~0.72 | ~0.80 |

### Evasion Type Coverage

- **Highly Detectable (v1)**: Plain text, delimiter attacks, role confusion
- **Moderately Detectable (v2)**: Multilingual, payload split, urgency
- **Challenging (v3)**: Homoglyphs, ZWJ, complex combinations

### Defense Complementarity

- Signature detection: Catches ~65% of attacks (those with success tokens)
- Rule-based detection: Catches ~80% of attacks (pattern-based)
- Combined: Catches ~90%+ of attacks (synergistic)

## Data Sources

- **Phase 1 Results**: `phase1/data/partA_results.json` (400 samples)
- **Phase 1 Annotations**: `phase1/data/phase1_output_annotated.json`
- **Config Files**: `phase1/data/tool_registry.yaml`, `schema_smuggling_variations.json`

## Path Resolution

All scripts use automatic path detection:

```python
script_dir = Path(__file__).parent        # phase2/scripts
phase2_dir = script_dir.parent            # phase2
phase1_dir = phase2_dir.parent / "phase1" # phase1
```

Scripts work from any directory:
- Root: `python phase2/scripts/evaluate_classifiers.py`
- phase2: `cd phase2 && python scripts/evaluate_classifiers.py`
- phase2/scripts: `cd phase2/scripts && python evaluate_classifiers.py`

## Next Steps

1. Run classifier evaluation
2. Analyze results and identify high-impact patterns
3. Develop defenses based on findings
4. Test on out-of-distribution data
5. Proceed to Phase 3 (defense deployment)

## References

- Phase 1 Results: `phase1/methods_and_results_phase1.md`
- Classifier Implementation: `prompt_injection_classifier.py`
- Evaluation Methodology: `evaluate_classifiers.py`
