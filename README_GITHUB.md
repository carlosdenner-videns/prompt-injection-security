# Prompt Injection Security: Phase 1 Baseline Vulnerability Assessment

A comprehensive security research project evaluating the vulnerability of large language models (LLMs) to prompt injection attacks in Retrieval-Augmented Generation (RAG) and schema smuggling contexts.

## 🎯 Overview

This project establishes baseline vulnerability metrics for prompt injection attacks across two state-of-the-art LLMs:
- **LLaMA-2-7b-chat** (Meta)
- **Falcon-7b-instruct** (TII)

### Key Findings

| Metric | LLaMA-2-7b | Falcon-7b |
|--------|-----------|----------|
| **RAG-Borne Injection ASR** | 65.00% | 5.00% |
| **Schema Smuggling ASR** | 31.58% | 26.32% |
| **Avg Generation Time** | 49.36s | 23.64s |
| **Most Effective Attack** | Plain/Delimiter/Role (100%) | Urgency (20%) |

**Critical Finding:** LLaMA-2 is **13x more vulnerable** to RAG-borne injection attacks than Falcon-7b.

## 📋 Project Structure

```
.
├── README.md                              # Original project README
├── README_GITHUB.md                       # This file
├── methods_and_results_phase1.md          # Comprehensive methods & results (11 sections)
├── requirements.txt                       # Python dependencies
│
├── Core Experiment Scripts
├── generate_kb.py                         # Knowledge base generation
├── partA_experiment.py                    # RAG-borne injection tests
├── partB_experiment.py                    # Schema smuggling tests
├── run_phase1.py                          # Pipeline orchestrator
│
├── Configuration Files
├── partA_kb_generator.yaml                # KB config (480 docs, 8 evasion types)
├── tool_registry.yaml                     # Tool definitions for Part B
├── schema_smuggling_variations.json       # Attack mechanism definitions
│
├── Utilities
├── model_utils.py                         # Model loading & inference
├── analyze_results.py                     # Results analysis & visualization
├── verify_setup.py                        # Environment verification
├── analyze_phase1.py                      # Quick analysis script
│
├── Results (Generated)
├── partA_kb.jsonl                         # Knowledge base (480 documents)
├── partA_results.json                     # Part A test results (400 cases)
├── partB_results.json                     # Part B test results (100 cases)
├── partA_progress.log                     # Execution log with checkpoints
│
└── Documentation
    ├── Phase 1_ Baseline Vulnerability Assessment.pdf
    ├── PROGRESS_TRACKING.md
    ├── ENHANCEMENTS_SUMMARY.md
    └── ADD_LLAMA2.md
```

## 🚀 Quick Start

### Prerequisites

- **Python:** 3.9+
- **GPU:** NVIDIA GPU with CUDA 11.8+ (RTX 4070 or better recommended)
- **Storage:** ~35 GB (models + results + cache)
- **HuggingFace Token:** Required for LLaMA-2 access

### Installation

```bash
# Clone repository
git clone https://github.com/videns-analytics/prompt-injection-security.git
cd prompt-injection-security

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Verify setup
python verify_setup.py
```

### HuggingFace Authentication

```bash
huggingface-cli login
# Paste your HuggingFace token when prompted
# Required for LLaMA-2 access
```

### Run Full Pipeline

```bash
python run_phase1.py
```

**Expected Runtime:** ~4 hours (2.7 hrs LLaMA-2 + 1.3 hrs Falcon-7b)

### Run Individual Steps

```bash
# Step 1: Generate knowledge base
python generate_kb.py

# Step 2: RAG-borne injection tests
python partA_experiment.py

# Step 3: Schema smuggling tests
python partB_experiment.py

# Step 4: Analyze results
python analyze_results.py
```

## 📊 Experiment Details

### Part A: RAG-Borne Injection

**Objective:** Test vulnerability to malicious instructions embedded in retrieved documents.

**Configuration:**
- **Knowledge Base:** 480 documents (400 benign, 80 malicious)
- **Test Queries:** 200 per model (100 injected, 100 benign)
- **Evasion Techniques:** 8 types
  1. Plain (baseline)
  2. Delimiter attack
  3. Role confusion
  4. Urgency manipulation
  5. Multilingual
  6. Payload split
  7. Zero-width joiners (ZWJ)
  8. Homoglyph substitution

**Results:**
- LLaMA-2-7b: 65% ASR (65/100 successful injections)
- Falcon-7b: 5% ASR (5/100 successful injections)

**Most Effective Techniques (LLaMA-2):**
- Plain text: 100%
- Delimiter attack: 100%
- Role confusion: 100%

**Least Effective Techniques:**
- Homoglyph substitution: 0% (both models)

### Part B: Schema Smuggling

**Objective:** Test vulnerability to violations of tool schemas through obfuscation.

**Configuration:**
- **Test Cases:** 100 (50 per model)
- **Attack Mechanisms:** 12 types
- **Tools:** 3 (send_email, db_query, http_get)

**Results:**
- LLaMA-2-7b: 31.58% ASR (12/38 successful attacks)
- Falcon-7b: 26.32% ASR (10/38 successful attacks)

**Most Vulnerable Tool:**
- HTTP GET: 100% ASR (both models)

**Most Resistant Tool:**
- Email: 13-21% ASR (both models)

## 🔬 Methodology

### Environment
- **GPU:** NVIDIA RTX 4070 Laptop (15.6 GB VRAM)
- **PyTorch:** 2.7.1+cu118
- **Transformers:** 4.35.0+
- **CUDA:** 11.8

### Model Configuration
- **Quantization:** float16 (memory optimization)
- **Device Mapping:** Automatic
- **Decoding:** Greedy (deterministic, `do_sample=False`)
- **Max Tokens:** 150 (Part A), variable (Part B)

### Reproducibility
- **Random Seed:** 1337
- **Deterministic Decoding:** Enabled
- **Checkpoint System:** Every 20 queries
- **Configuration:** YAML-based, version-controlled

## 📈 Key Insights

### 1. Model Vulnerability Disparity
LLaMA-2's 13x higher vulnerability to RAG injection suggests:
- Aggressive instruction-tuning makes it overly compliant
- Weak context separation between system and user content
- Better instruction-following can be a security liability

### 2. Evasion Technique Effectiveness
- **Semantic-level attacks** (plain, delimiter, role) are highly effective
- **Character-level obfuscation** (homoglyph, unicode) is ineffective
- Models normalize input during tokenization, defeating character tricks

### 3. Speed-Security Trade-off
- Falcon-7b is 2.1x faster (23.64s vs 49.36s avg)
- Faster models show better security (5% vs 65% ASR)
- Hypothesis: More reasoning time enables following injections

### 4. Schema Smuggling Resilience
- Both models show similar vulnerability (~26-32%)
- Much lower than RAG-borne injection (65% vs 31%)
- Schema validation is more effective than context separation

## 🛡️ Recommendations

### Immediate Actions
1. **Urgent:** Develop context isolation techniques for LLaMA-2
2. **Priority:** Implement XML-based role markers to separate contexts
3. **Investigation:** Analyze Falcon-7b's robustness mechanisms

### Phase 2 (Defense Development)
- Develop and test mitigation strategies
- Evaluate defense effectiveness against evolved attacks
- Test on additional models (GPT-3.5, Claude, Mistral)

### Long-term
- Establish prompt injection security benchmarks
- Create defense framework for production RAG systems
- Contribute to LLM safety standards

## 📚 Documentation

- **[methods_and_results_phase1.md](methods_and_results_phase1.md)** - Comprehensive 11-section technical report
- **[README.md](README.md)** - Original project documentation
- **[PROGRESS_TRACKING.md](PROGRESS_TRACKING.md)** - Development history
- **[Phase 1 PDF](Phase%201_%20Baseline%20Vulnerability%20Assessment%20for%20Prompt%20Injection%20Attacks.pdf)** - Formal report

## 📊 Generated Outputs

After running the full pipeline:

| File | Size | Purpose |
|------|------|---------|
| `partA_kb.jsonl` | 124 KB | Knowledge base (480 documents) |
| `partA_results.json` | 400 KB | Part A results (400 test cases) |
| `partB_results.json` | 100 KB | Part B results (100 test cases) |
| `partA_analysis.csv` | - | Detailed Part A analysis |
| `partB_analysis.csv` | - | Detailed Part B analysis |
| `partA_heatmap.png` | - | Evasion technique effectiveness heatmap |
| `partB_heatmap.png` | - | Schema smuggling mechanism heatmap |
| `phase1_comparison.png` | - | Model comparison visualization |
| `phase1_summary.txt` | - | Executive summary |

## 🔧 Troubleshooting

### CUDA Not Available
```bash
# Reinstall PyTorch with CUDA support
pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Out of Memory
```python
# In model_utils.py, enable 8-bit quantization:
runner = ModelRunner("llama2-7b", load_in_8bit=True)
```

### HuggingFace Token Issues
```bash
# Re-authenticate
huggingface-cli logout
huggingface-cli login
```

## 📝 Citation

If you use this research, please cite:

```bibtex
@misc{videns2025promptinjection,
  title={Baseline Vulnerability Assessment for Prompt Injection Attacks in RAG Systems},
  author={VIDENS ANALYTICS Security Research Team},
  year={2025},
  howpublished={\url{https://github.com/videns-analytics/prompt-injection-security}}
}
```

## 📄 License

[Specify your license here - e.g., MIT, Apache 2.0, etc.]

## 👥 Contributors

- **Carlo Denner** - Lead Researcher (carlos.denner@videns.ai)
- VIDENS ANALYTICS Security Research Team

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Submit a Pull Request

## 📧 Contact

For questions or collaboration inquiries:
- Email: carlos.denner@videns.ai
- Organization: VIDENS ANALYTICS

## 🔗 Related Work

- [OWASP Prompt Injection](https://owasp.org/www-community/attacks/Prompt_Injection)
- [LLM Security Research](https://arxiv.org/search/?query=prompt+injection&searchtype=all)
- [RAG System Security](https://arxiv.org/search/?query=retrieval+augmented+generation+security)

---

**Last Updated:** October 30, 2025  
**Status:** Phase 1 Complete ✅ | Phase 2 In Development 🚀
