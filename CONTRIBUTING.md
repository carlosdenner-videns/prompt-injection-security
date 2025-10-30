# Contributing to Prompt Injection Security Research

Thank you for your interest in contributing to this security research project!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/prompt-injection-security.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Push to your fork: `git push origin feature/your-feature-name`
6. Submit a Pull Request

## Development Setup

```bash
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

## Code Style

- Follow PEP 8 conventions
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

## Testing

Before submitting a PR:

```bash
# Run verification
python verify_setup.py

# Test individual components
python test_model_load.py
python test_llama_access.py
```

## Documentation

- Update README.md if adding new features
- Document new evasion techniques in partA_kb_generator.yaml
- Add comments for complex logic
- Update methods_and_results_phase1.md for significant changes

## Reporting Issues

When reporting bugs, please include:
- Python version and OS
- GPU model and CUDA version
- Full error traceback
- Steps to reproduce
- Expected vs actual behavior

## Areas for Contribution

### High Priority
- [ ] Implement defense mechanisms (Phase 2)
- [ ] Test additional models (GPT-3.5, Claude, Mistral)
- [ ] Develop adaptive evasion techniques
- [ ] Create benchmark suite

### Medium Priority
- [ ] Improve documentation
- [ ] Add more evasion techniques
- [ ] Enhance visualization tools
- [ ] Optimize model loading

### Low Priority
- [ ] Code refactoring
- [ ] Performance optimizations
- [ ] Additional test cases
- [ ] Example notebooks

## Commit Messages

Use clear, descriptive commit messages:
```
Add new evasion technique: semantic obfuscation

- Implement semantic-level instruction obfuscation
- Add 5 new test cases
- Update KB generator configuration
- Document technique in methods section
```

## Pull Request Process

1. Update documentation as needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Request review from maintainers
5. Address feedback and re-request review

## Code of Conduct

- Be respectful and constructive
- Focus on the research and code, not individuals
- Report security issues privately
- Maintain confidentiality of sensitive findings

## Questions?

Open an issue or contact: carlos.denner@videns.ai

---

Thank you for contributing to prompt injection security research!
