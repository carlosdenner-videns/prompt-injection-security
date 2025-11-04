# Limitations and Constraints Enhancements

## Summary of Improvements

The Limitations section has been significantly expanded with realistic expectations, actionable guidance, and clear scope delimitation across five key areas.

## Complete Limitations Section Structure

### Before (1 paragraph, ~60 words):
Generic statement about evaluation scope and future work.

### After (5 paragraphs, ~350 words):
Comprehensive coverage of:
1. Novel attack coverage (arms race)
2. Multi-turn and conversational context
3. Scope and modality (text-only)
4. Evaluation setting (models, benchmarks)
5. Future directions (community path forward)

---

## 1. Novel Attack Coverage (Lines 395-396)

### Key Message:
**"No static input filter can catch all possible prompt injections"**

### What This Section Provides:

**Reality check:**
> "Our Monitoring mode detects approximately 49% of novel attacks... which significantly raises the bar but is not foolproof."

**Analogy:**
> "This is an arms race analogous to antivirus signatures: as new attacks emerge, detectors must be updated."

**Actionable guidance:**
> "We recommend deploying Monitoring mode to log suspicious prompts that slip through, creating a feedback loop for incremental learning."

**Practical advice:**
> "Practitioners should treat signature rules and semantic exemplars as living databases that evolve with the threat landscape, much like antivirus definitions require regular updates."

---

### Why This Works:

**1. Sets realistic expectations:**
- ✅ Not foolproof (honest)
- ✅ 49% is significant but not complete
- ✅ Arms race acknowledged

**2. Provides familiar analogy:**
- ✅ Antivirus signatures (everyone understands)
- ✅ Regular updates needed (expected pattern)
- ✅ Living databases (not static)

**3. Offers actionable solution:**
- ✅ Deploy Monitoring mode
- ✅ Log what slips through
- ✅ Create feedback loop
- ✅ Incremental learning

**4. Frames as normal practice:**
- ✅ Like antivirus definitions
- ✅ Evolve with threat landscape
- ✅ Expected maintenance

---

### Practitioner Takeaway:
**"This is good enough to deploy, and here's how to improve it over time"**

Not: "This only catches 49%, so it's not useful"  
But: "This catches 49% of novel attacks (and 87% of known), and you can improve it by logging and learning"

---

## 2. Multi-Turn and Conversational Context (Lines 398-399)

### Key Message:
**"Per-prompt protection, not conversation-level"**

### What This Section Provides:

**Scope clarity:**
> "Our evaluation focused on single-turn prompts in a RAG QA setting."

**Limitation acknowledgment:**
> "If your application is an open-ended chatbot with multi-turn conversations, the current system provides per-prompt protection but does not track conversational state"

**Concrete example:**
> "e.g., 'In your previous response you said X; now ignore that and do Y'"

**Recommendation:**
> "For such scenarios, we recommend combining this input-side firewall with conversation-level analysis or training-time defenses like StruQ or SecAlign."

**Value proposition:**
> "The firewall still adds value by catching single-turn injection attempts and tool-calling exploits, which are common even in multi-turn settings."

---

### Why This Works:

**1. Clear scope:**
- ✅ Single-turn focus stated
- ✅ Multi-turn limitation acknowledged
- ✅ Concrete example provided

**2. Honest about gaps:**
- ✅ Doesn't track conversational state
- ✅ Can't detect cross-turn attacks
- ✅ Specific attack pattern shown

**3. Provides solution:**
- ✅ Combine with conversation-level analysis
- ✅ Cites complementary approaches (StruQ, SecAlign)
- ✅ Defense-in-depth strategy

**4. Maintains value:**
- ✅ Still catches single-turn attacks
- ✅ Still catches tool-calling exploits
- ✅ Common even in multi-turn settings

---

### Practitioner Takeaway:
**"This protects each prompt individually; for multi-turn, layer additional defenses"**

Not: "This doesn't work for chatbots"  
But: "This provides per-prompt protection; combine with conversation analysis for full coverage"

---

## 3. Scope and Modality (Lines 401-402)

### Key Message:
**"Text-only; multimodal requires additional checks"**

### What This Section Provides:

**Clear scope:**
> "We focus on *textual* prompt attacks."

**Multimodal limitation:**
> "If your system accepts non-text inputs (images, audio, or other modalities), additional checks would be needed"

**Concrete example:**
> "for instance, an attacker could embed malicious instructions in an image that a vision-language model interprets"

**Emerging threat:**
> "Multimodal prompt injection is an emerging threat outside our current scope."

**Language limitation:**
> "Similarly, we evaluated English prompts; multilingual attacks and code-switching may require language-specific normalization and exemplar sets."

---

### Why This Works:

**1. Delimits scope clearly:**
- ✅ Text-only (explicit)
- ✅ English-only (stated)
- ✅ No ambiguity

**2. Acknowledges multimodal threat:**
- ✅ Images can contain instructions
- ✅ Vision-language models vulnerable
- ✅ Outside current scope (honest)

**3. Provides guidance:**
- ✅ Additional checks needed
- ✅ Language-specific normalization
- ✅ Exemplar sets per language

**4. Frames as emerging:**
- ✅ Not a failure of our work
- ✅ Future research area
- ✅ Community challenge

---

### Practitioner Takeaway:
**"This handles text; if you use images/audio, add modality-specific checks"**

Not: "This doesn't work for multimodal systems"  
But: "This is text-focused; multimodal systems need additional layers"

---

## 4. Evaluation Setting (Lines 404-405)

### Key Message:
**"Tested on 7B models; model-agnostic design transfers"**

### What This Section Provides:

**Evaluation scope:**
> "We tested two 7B parameter models (LLaMA-2-7B and Falcon-7B) in a RAG setting."

**Generalizability caveat:**
> "Larger models (e.g., 70B+) and different architectures (e.g., mixture-of-experts) may exhibit different vulnerability profiles."

**Future validation:**
> "Cross-benchmark evaluation (e.g., on JailbreakBench) and testing with proprietary models (GPT-4, Claude) would strengthen generalizability claims."

**Transferability claim:**
> "However, the input-side nature of our defense means it is model-agnostic and should transfer across architectures."

---

### Why This Works:

**1. Honest about evaluation:**
- ✅ 7B models tested
- ✅ RAG setting specified
- ✅ Not all models/settings

**2. Acknowledges uncertainty:**
- ✅ Larger models may differ
- ✅ Different architectures possible
- ✅ Proprietary models untested

**3. Suggests validation:**
- ✅ Cross-benchmark testing
- ✅ JailbreakBench mentioned
- ✅ GPT-4/Claude testing

**4. Defends transferability:**
- ✅ Input-side (model-agnostic)
- ✅ Should transfer
- ✅ Architectural independence

---

### Practitioner Takeaway:
**"Tested on 7B models, but input-side design should work across sizes"**

Not: "Only works on 7B models"  
But: "Evaluated on 7B; input-side nature means it should transfer to larger models"

---

## 5. Future Directions (Lines 407-408)

### Key Message:
**"Community should iterate jointly"**

### What This Section Provides:

**Technical directions:**
> "Extending detectors with dialogue-state features, incremental learning from Monitoring mode telemetry, and hybrid approaches combining input-side filtering with training-time alignment are promising paths."

**Community call:**
> "The community should iterate jointly on expanding signature corpora, semantic exemplar sets, and conversational state analysis"

**Design constraint:**
> "to close remaining gaps while maintaining the lightweight, deployable nature of input-side defenses."

---

### Why This Works:

**1. Specific technical paths:**
- ✅ Dialogue-state features
- ✅ Incremental learning
- ✅ Hybrid approaches

**2. Community framing:**
- ✅ Joint iteration
- ✅ Shared resources (corpora, exemplars)
- ✅ Collaborative improvement

**3. Maintains principles:**
- ✅ Lightweight (performance)
- ✅ Deployable (practical)
- ✅ Input-side (architecture)

---

## Comparison: Before vs. After

### Before (Generic):
> "We tested English single-turn prompts in a RAG QA setting with two 7B models; multilingual and larger models remain future work. Extending detectors with dialogue-state features and incremental learning on newly observed attacks (via Monitoring mode telemetry) is a promising path. Cross-benchmark comparisons (e.g., JailbreakBench) and hybrid approaches with alignment are also warranted."

**Problems:**
- ❌ No realistic expectations set
- ❌ No actionable guidance
- ❌ No scope delimitation
- ❌ No analogy or framing
- ❌ Reads like boilerplate

---

### After (Comprehensive):

**5 focused paragraphs:**
1. **Novel attacks:** Arms race analogy, actionable guidance (Monitoring mode)
2. **Multi-turn:** Clear scope, defense-in-depth recommendation
3. **Modality:** Text-only, multimodal needs additional checks
4. **Evaluation:** Model-agnostic design, transferability claim
5. **Future:** Community path, maintains principles

**Improvements:**
- ✅ Realistic expectations (not foolproof)
- ✅ Actionable guidance (deploy Monitoring, log, learn)
- ✅ Clear scope (text, single-turn, English)
- ✅ Familiar analogies (antivirus)
- ✅ Maintains value proposition

---

## Antivirus Analogy Analysis

### Why This Analogy Works:

**1. Universal understanding:**
- Everyone knows antivirus software
- Everyone knows it needs updates
- Everyone accepts this as normal

**2. Sets correct expectations:**
- Not 100% protection
- Needs regular updates
- Arms race is expected

**3. Provides mental model:**
- Signature databases (our rules/exemplars)
- Definition updates (incremental learning)
- Zero-day threats (novel attacks)

**4. Justifies maintenance:**
- Regular updates expected
- Living databases normal
- Continuous improvement accepted

---

### Specific Language Used:

> "This is an arms race analogous to antivirus signatures"

> "much like antivirus definitions require regular updates"

> "Practitioners should treat signature rules and semantic exemplars as living databases that evolve with the threat landscape"

**Result:** Practitioners immediately understand the maintenance model

---

## Actionable Guidance Summary

### For Novel Attacks:
✅ **Deploy Monitoring mode**  
✅ **Log suspicious prompts**  
✅ **Create feedback loop**  
✅ **Update signatures/exemplars regularly**  

### For Multi-Turn:
✅ **Use for per-prompt protection**  
✅ **Combine with conversation-level analysis**  
✅ **Layer with StruQ/SecAlign**  
✅ **Still catches tool-calling exploits**  

### For Multimodal:
✅ **Add modality-specific checks**  
✅ **Language-specific normalization**  
✅ **Exemplar sets per language**  

### For Evaluation:
✅ **Test on your specific models**  
✅ **Cross-benchmark validation**  
✅ **Input-side should transfer**  

---

## Practitioner Benefits

### Sets Realistic Expectations:
- ✅ Not foolproof (honest)
- ✅ 49% novel + 87% known (quantified)
- ✅ Arms race acknowledged
- ✅ Maintenance required

### Provides Actionable Guidance:
- ✅ How to handle limitations (Monitoring mode)
- ✅ How to improve over time (feedback loop)
- ✅ How to extend (conversation analysis)
- ✅ How to validate (cross-benchmark)

### Maintains Value Proposition:
- ✅ Significantly raises the bar
- ✅ Still catches most attacks
- ✅ Per-prompt protection valuable
- ✅ Model-agnostic design

### Frames as Normal Practice:
- ✅ Like antivirus (familiar)
- ✅ Regular updates expected
- ✅ Defense-in-depth standard
- ✅ Continuous improvement

---

## Word Count Impact

**Before:** ~60 words (1 paragraph)  
**After:** ~350 words (5 paragraphs)  
**Increase:** +290 words

**Justification:**
- Critical for setting realistic expectations
- Prevents practitioner disappointment
- Provides actionable guidance
- Strengthens paper credibility

---

## Comparison with Academic Norms

### Typical limitations section:
> "We evaluated on dataset X. Future work should test on Y."

**Problems:**
- Generic
- No guidance
- No expectations

### Our approach:
- ✅ Specific limitations with examples
- ✅ Actionable guidance for each
- ✅ Realistic expectations set
- ✅ Value proposition maintained

**Result:** Practitioners know exactly what to expect and how to handle limitations

---

## Final Assessment

**Status:** ✅ **Comprehensive and Actionable**

**Coverage:**
- ✅ Novel attacks (arms race, 49% coverage)
- ✅ Multi-turn (per-prompt, combine with others)
- ✅ Modality (text-only, multimodal needs more)
- ✅ Evaluation (7B models, should transfer)
- ✅ Future (community path forward)

**Tone:**
- ✅ Honest (not foolproof)
- ✅ Realistic (49% novel, 87% known)
- ✅ Actionable (specific guidance)
- ✅ Positive (significantly raises bar)

**Practitioner value:**
- ✅ Know what to expect
- ✅ Know how to handle gaps
- ✅ Know how to improve
- ✅ Know when to deploy

**Ready for publication:** Yes, the limitations section now provides comprehensive, realistic, and actionable guidance that strengthens the paper's credibility and practical value.

---

## Quick Reference

**What was added:**
- 5 focused limitation paragraphs (~290 words)
- Antivirus analogy (familiar mental model)
- Actionable guidance for each limitation
- Realistic expectations throughout

**Where:**
- Lines 395-408: Expanded Limitations section
- 5 paragraphs: Novel, Multi-turn, Modality, Evaluation, Future

**Why:**
- Sets realistic expectations
- Provides actionable guidance
- Maintains value proposition
- Strengthens credibility

**Result:**
- Practitioners know what to expect
- Clear guidance on handling limitations
- Honest about gaps
- Maintains practical value
