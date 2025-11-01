# System Architecture Visualization & Documentation

**Date**: November 1, 2025  
**Status**: ✅ **ARCHITECTURE DOCUMENTATION**  
**Purpose**: Provide clear visual representation of system design for publication

---

## 1. High-Level System Architecture

### Publication-Ready ASCII Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         INPUT TEXT                              │
│                    (User Query or RAG Doc)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NORMALIZER (Phase 5)                       │
│  • NFKC Unicode normalization                                   │
│  • Zero-width character stripping                               │
│  • Homoglyph mapping (Cyrillic/Greek → ASCII)                  │
│  • Mixed-script detection & safeguard                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
        ┌─────────────────────┐  ┌──────────────────────┐
        │  DETECTOR LAYER     │  │  FEATURE EXTRACTION  │
        │  (Phase 2)          │  │  (Phase 5 Optional)  │
        │                     │  │                      │
        │ v1: 80% TPR         │  │ • Detector outputs   │
        │ v2: 44% TPR         │  │ • Normalizer metrics │
        │ v3: 57% TPR         │  │ • Rule one-hots      │
        │                     │  │ • Text statistics    │
        └──────────┬──────────┘  └──────────┬───────────┘
                   │                        │
                   │         ┌──────────────┘
                   │         │
                   ▼         ▼
        ┌─────────────────────────────────┐
        │  FUSION LAYER                   │
        │  • OR Fusion: 87% TPR, 0% FAR   │
        │  • Learned: 99% TPR (Phase 1)   │
        └──────────────┬──────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │  DECISION: ATTACK or BENIGN     │
        └─────────────────────────────────┘
```

---

## 2. Detector Specifications

### v1: Signature-Based (80% TPR)

**Patterns**:
- Instruction Override: "ignore all previous", "override", etc.
- Direct Output: "respond only with", "output only", etc.
- Role Confusion: "you are now", "act as", "pretend", etc.
- Urgency Ploy: "urgent", "critical", "emergency", etc.
- Delimiter Markers: "---", "===", "***", "###", etc.
- System Instruction: "system prompt", "internal instruction"

**Additional**: Base64 encoding, homoglyph detection

---

### v2: Heuristic Rule-Based (44% TPR)

**Rules**:
- High Symbol Density (>15%)
- Long Numeric Strings (15+ digits)
- Uncommon Unicode (non-ASCII symbols)
- YAML Injection Patterns
- JSON Injection Patterns
- Unusual Capitalization (>40% capitals)

**Note**: Independent from v1 (different patterns)

---

### v3: Semantic/Contextual (57% TPR)

**Layers**:
1. **Keyword Matching** (18 keywords with weights)
   - High-confidence: ignore, override, bypass
   - Medium-confidence: system, prompt, admin
   - Rule: 2+ keywords OR 1 high-confidence

2. **Pattern Matching** (Regex)
   - "tell me X", "show me X", "ignore Y"
   - Only flags if combined with keywords

3. **Formatting Detection**
   - Delimiters (--- or ===)
   - Excessive punctuation (>30%)
   - All-caps emphasis (>50% of words)

**Note**: Originally planned as ML classifier, implemented as semantic detector

---

## 3. Fusion Strategies

### OR Fusion (Phase 3): 87% TPR, 0% FAR

```
is_attack = v1.is_attack OR v3.is_attack
confidence = max(v1.confidence, v3.confidence)

Decision Table:
v1    v3    Result
─────────────────────
False False → BENIGN
False True  → ATTACK ✓
True  False → ATTACK ✓
True  True  → ATTACK ✓
```

**Complementarity**:
- v1 catches: Plain text, delimiters, roles
- v3 catches: Semantic patterns, formatting
- Together: 87% TPR (vs 80% and 57% alone)

---

### Learned Fusion (Phase 5): 99% TPR (Phase 1), 49.2% TPR (Novel)

**Features** (25 total):
- Detector outputs (6): v1, v2, v3 is_attack + confidence
- Normalizer metrics (8): Unicode changes, homoglyphs, zero-width
- Rule one-hots (8): Which heuristic rules triggered
- Text statistics (3): Length, entropy, symbol ratio

**Training**:
- Nested cross-validation (5 outer, 5 inner)
- Logistic regression with L2 regularization
- Threshold calibration on inner CV folds

**Performance**:
- Phase 1: 99% TPR, 0% FAR (95% CI: [95.0%, 100.0%])
- Novel attacks: 49.2% TPR (generalization gap: -49.8 pp)

---

## 4. Normalizer Component

**Steps**:
1. NFKC Unicode normalization (compatibility chars)
2. Zero-width character stripping (ZWJ, ZWSP, etc.)
3. Homoglyph mapping with safeguard (Cyrillic/Greek → ASCII)
4. Mixed-script detection (flags suspicious mixing)

**Impact**:
- v1 FAR: 23.1% → 11.5% on obfuscated (50% improvement)
- v3 FAR: 0.77% on obfuscated benign
- Homoglyph attacks: 0% FAR (fixed!)

---

## 5. Data Flow Example: Attack Detection

```
Input: "IGNORE АLL PREVIOUS INSTRUCTIONS"
       (А is Cyrillic, not ASCII)

Normalizer: А → A
Output: "IGNORE ALL PREVIOUS INSTRUCTIONS"

v1 (Signature):
├─ Match: "IGNORE ALL PREVIOUS"
└─ Result: is_attack=True, confidence=0.8

v3 (Semantic):
├─ Keywords: "ignore" (0.8), "instructions" (0.7)
└─ Result: is_attack=True, confidence=0.75

OR Fusion:
├─ True OR True = True
└─ Decision: ATTACK ✓
```

---

## 6. Performance Comparison

| Configuration | Phase 1 TPR | Phase 1 FAR | Phase 6a FAR | Phase 6b TPR |
|---|---|---|---|---|
| v1 | 80% | 0% | 23.1% | 11.7% |
| v3 | 57% | 0% | 0.77% | 44.2% |
| v1+v3 (OR) | 87% | 0% | 23.8% | 49.2% |
| Norm+v3 | 87% | 0% | 0.77% | 44.2% |
| Norm+v1+v3 | 87% | 0% | 12.3% | 49.2% |
| Learned Fusion | 99%* | 0%* | N/A | 49.2%** |

*Nested CV on Phase 1; **Evaluated on novel attacks

---

## 7. Deployment Recommendations

**Production**: Normalizer + v3
- TPR: 87% on known attacks
- FAR: 0.77% on obfuscated benign
- Best balance of detection and safety

**Monitoring**: Normalizer + v1 + v3
- TPR: 49.2% on novel attacks
- FAR: 12.3% on obfuscated benign
- Higher detection for security research

---

## 8. Key Design Decisions

### Why Three Independent Detectors?

**Complementarity**:
- v1 (Signature): Keyword-based attacks
- v2 (Rules): Formatting anomalies
- v3 (Semantic): Contextual attacks
- Together: 87% TPR (vs 80%, 44%, 57% alone)

### Why OR Fusion?

- **OR**: Any detector flags = attack (87% TPR, 0% FAR)
- **AND**: All detectors flag = attack (lower recall)
- **Chosen**: OR provides optimal balance

### Why Normalizer?

- **Problem**: Homoglyphs, zero-width chars evade detection
- **Solution**: Normalize before detection
- **Result**: 50% FAR improvement on obfuscated text

---

## 9. Limitations & Future Work

**Coverage Gaps** (Phase 6b):
- Multi-turn manipulation: 40% TPR
- Context confusion: 25% TPR
- Encoding/obfuscation: 45% TPR

**Future Work**:
- Multi-turn manipulation detection
- Context confusion detection
- Encoding layer (Base64, ROT13, Hex)
- Semantic similarity matching (embeddings)
- Adversarial robustness testing

---

## 10. Compact Diagram for Publication

```
INPUT
  │
  ├─→ Normalizer (remove obfuscation)
  │
  ├─→ v1 (Signature, 80%)
  ├─→ v2 (Rules, 44%)
  ├─→ v3 (Semantic, 57%)
  │
  ├─→ OR Fusion (87% TPR, 0% FAR)
  │
  └─→ DECISION: ATTACK or BENIGN
```

---

## Summary

This architecture provides:

✅ **Modular Design**: Independent detectors can be updated separately  
✅ **Complementarity**: OR fusion captures different attack patterns  
✅ **Robustness**: Normalizer handles obfuscation  
✅ **Transparency**: Clear decision logic and feature engineering  
✅ **Scalability**: Stateless design enables parallelization  

**Suitable for Publication**: Diagrams can be converted to figures for papers, with detailed component descriptions supporting technical sections.
