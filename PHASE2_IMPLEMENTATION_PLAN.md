# Phase 2: Defense Development and Evaluation - Implementation Plan

Status: Ready to Execute
Created: October 31, 2025
Objective: Develop and evaluate pattern-driven defenses against prompt injection attacks

---

## Executive Summary

Phase 2 builds on Phase 1 baseline to develop iterative defenses:

1. Develop 3 classifier versions (v1 to v3) with increasing sophistication
2. Evaluate on Phase 1 dataset (400 samples from Part A)
3. Perform ablation analysis to understand defense complementarity
4. Benchmark against baselines (NeMo, Moderation API)
5. Document findings with statistical rigor (Wilson CIs, McNemar tests)

---

## Phase 1 Recap: Key Insights

### Attack Vulnerability
- LLaMA-2-7b: 65% ASR (RAG-borne), 31.58% (schema smuggling)
- Falcon-7b: 5% ASR (RAG-borne), 26.32% (schema smuggling)
- 13x difference in RAG vulnerability between models

### Most Effective Evasion Techniques (LLaMA-2)
1. Plain text injection: 100% success
2. Delimiter attacks: 100% success
3. Role confusion: 100% success
4. Multilingual: 84.6% success
5. Payload split: 50% success

### Least Effective Techniques
- Homoglyph substitution: 0% success
- Unicode obfuscation: 0% success
- Character-level tricks ineffective due to tokenization

### Dataset Composition
- Total samples: 400 (200 per model)
- Injected queries: 100 per model (50% of total)
- Benign queries: 100 per model (50% of total)
- Evasion types: 8 variants tested
- Success tokens: 3 variants

---

## Implementation Roadmap

### Task 1: Classifier Development

#### Classifier v1: Minimal Keywords
Objective: Establish baseline detection with obvious patterns

Patterns:
- Ignore instructions: "ignore all previous", "forget all previous"
- Role play: "you are now", "pretend you are"
- Jailbreak: "dan mode", "developer mode", "unrestricted"
- Direct output: "respond only with", "output only"

Expected Performance:
- TPR: 40-50% (catches obvious attacks)
- FAR: 2-3% (very few false alarms)
- F1: ~0.55

#### Classifier v2: Phase 1 Patterns
Objective: Expand with patterns learned from Phase 1 evasion types

Additional Patterns:
- Delimiter attacks: ---END OF CONTEXT---, NEW SYSTEM INSTRUCTION
- Role confusion: [Assistant's internal reasoning], system has instructed
- Urgency manipulation: URGENT SECURITY UPDATE, required security protocol
- Multilingual: German, Spanish, French, Russian variants
- Payload split: CRITICAL SYSTEM NOTE, override standard behavior

Expected Performance:
- TPR: 60-70% (catches most semantic attacks)
- FAR: 5-8% (slight increase in false alarms)
- F1: ~0.70

#### Classifier v3: Enhanced Logic
Objective: Maximize detection with weighted patterns and combinations

Enhancements:
- Weighted patterns: High-confidence patterns get higher weights
- Regex patterns: Catch character obfuscation
- Pattern combinations: Boost confidence for multi-category matches

Expected Performance:
- TPR: 75-85% (catches most attacks including obfuscated)
- FAR: 8-12% (acceptable trade-off)
- F1: ~0.80

---

## Evaluation Metrics

- TPR (True Positive Rate): Detection rate on actual attacks
- FAR (False Alarm Rate): False positive rate on benign prompts
- Accuracy: Overall correctness
- Precision: Reliability of positive predictions
- F1 Score: Harmonic mean of precision and recall
- Wilson 95% CI: Confidence intervals for all rates

---

## File Structure

phase2/
├── scripts/
│   ├── prompt_injection_classifier.py     (Implemented)
│   ├── evaluate_classifiers.py            (Implemented)
│   ├── annotation_updater.py              (To implement)
│   ├── ablation_analysis.py               (To implement)
│   └── generate_plots.py                  (To implement)
├── data/
├── results/
├── plots/
└── README.md

---

## Success Criteria

- v1, v2, v3 implemented and tested
- Clear improvement trend (TPR: 45% to 65% to 80%)
- All metrics computed with Wilson CIs
- McNemar significance tests performed
- Defense complementarity quantified
- Comprehensive documentation

---

## Next Steps

1. Run classifier evaluation
2. Update Phase 1 annotations with defense results
3. Perform ablation study
4. Generate visualizations
5. Document findings in methods-and-results report

Document Version: 1.0
Last Updated: October 31, 2025
Status: Ready for Implementation
