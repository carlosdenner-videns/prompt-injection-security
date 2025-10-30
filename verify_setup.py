"""
Verify system setup and dependencies before running experiments.
"""

import sys
import importlib
from pathlib import Path


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("  ✗ ERROR: Python 3.9+ required")
        return False
    
    print("  ✓ Python version OK")
    return True


def check_dependencies():
    """Check required Python packages."""
    required = [
        "torch",
        "transformers",
        "accelerate",
        "yaml",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scipy",
        "tqdm"
    ]
    
    print("\nChecking dependencies:")
    all_ok = True
    
    for package in required:
        try:
            module = importlib.import_module(package if package != "yaml" else "yaml")
            version = getattr(module, "__version__", "unknown")
            print(f"  ✓ {package}: {version}")
        except ImportError:
            print(f"  ✗ {package}: NOT INSTALLED")
            all_ok = False
    
    return all_ok


def check_cuda():
    """Check CUDA availability."""
    print("\nChecking CUDA:")
    
    try:
        import torch
        
        if torch.cuda.is_available():
            print(f"  ✓ CUDA available: {torch.version.cuda}")
            print(f"  ✓ Device: {torch.cuda.get_device_name(0)}")
            print(f"  ✓ Total memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
            
            # Test GPU
            try:
                x = torch.randn(100, 100).cuda()
                y = x @ x.t()
                del x, y
                torch.cuda.empty_cache()
                print("  ✓ GPU test passed")
                return True
            except Exception as e:
                print(f"  ✗ GPU test failed: {e}")
                return False
        else:
            print("  ⚠ CUDA not available - will run on CPU (VERY SLOW)")
            return False
            
    except ImportError:
        print("  ✗ PyTorch not installed")
        return False


def check_config_files():
    """Check required configuration files exist."""
    print("\nChecking configuration files:")
    
    required_files = [
        "partA_kb_generator.yaml",
        "tool_registry.yaml",
        "schema_smuggling_variations.json",
        "generate_kb.py",
        "partA_experiment.py",
        "partB_experiment.py",
        "model_utils.py",
        "analyze_results.py"
    ]
    
    all_exist = True
    
    for filename in required_files:
        if Path(filename).exists():
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} - MISSING")
            all_exist = False
    
    return all_exist


def check_huggingface_auth():
    """Check HuggingFace authentication."""
    print("\nChecking HuggingFace authentication:")
    
    try:
        from huggingface_hub import HfFolder
        
        token = HfFolder.get_token()
        if token:
            print("  ✓ HuggingFace token found")
            print("  ℹ You can access gated models like LLaMA-2")
            return True
        else:
            print("  ⚠ No HuggingFace token found")
            print("  ℹ Run: huggingface-cli login")
            print("  ℹ This is required for LLaMA-2 but not Falcon")
            return False
            
    except ImportError:
        print("  ⚠ huggingface_hub not installed")
        return False


def estimate_disk_space():
    """Estimate required disk space."""
    print("\nDisk space requirements:")
    print("  • Models: ~28 GB (2 models × ~14 GB each)")
    print("  • Results: ~500 MB")
    print("  • Cache: ~2 GB")
    print("  • Total: ~30-35 GB")
    
    try:
        import shutil
        stats = shutil.disk_usage(Path.cwd())
        free_gb = stats.free / 1e9
        print(f"\n  Available: {free_gb:.1f} GB")
        
        if free_gb < 35:
            print("  ⚠ WARNING: Low disk space")
            return False
        else:
            print("  ✓ Sufficient disk space")
            return True
    except Exception:
        print("  ⚠ Could not check disk space")
        return True


def main():
    """Run all verification checks."""
    print("="*70)
    print(" PHASE 1 SETUP VERIFICATION")
    print("="*70)
    
    checks = [
        ("Python Version", check_python_version()),
        ("Dependencies", check_dependencies()),
        ("CUDA/GPU", check_cuda()),
        ("Config Files", check_config_files()),
        ("HuggingFace Auth", check_huggingface_auth()),
        ("Disk Space", estimate_disk_space())
    ]
    
    print("\n" + "="*70)
    print(" SUMMARY")
    print("="*70)
    
    critical_passed = True
    warnings = []
    
    for check_name, passed in checks:
        if check_name in ["Python Version", "Dependencies", "Config Files"]:
            # Critical checks
            if not passed:
                print(f"✗ {check_name}: FAILED (critical)")
                critical_passed = False
            else:
                print(f"✓ {check_name}: OK")
        else:
            # Non-critical checks
            if not passed:
                print(f"⚠ {check_name}: WARNING")
                warnings.append(check_name)
            else:
                print(f"✓ {check_name}: OK")
    
    print("\n" + "="*70)
    
    if not critical_passed:
        print("✗ CRITICAL ISSUES DETECTED - Cannot proceed")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
        return 1
    
    if warnings:
        print(f"⚠ {len(warnings)} warnings detected:")
        for w in warnings:
            print(f"  • {w}")
        print("\nYou can proceed but may encounter issues.")
        print("Recommended actions:")
        if "CUDA/GPU" in warnings:
            print("  • Experiments will be very slow on CPU")
        if "HuggingFace Auth" in warnings:
            print("  • Run: huggingface-cli login")
        if "Disk Space" in warnings:
            print("  • Free up disk space before downloading models")
    else:
        print("✓ ALL CHECKS PASSED - Ready to run experiments!")
    
    print("\nNext steps:")
    print("  1. Generate KB:     python generate_kb.py")
    print("  2. Run Part A:      python partA_experiment.py")
    print("  3. Run Part B:      python partB_experiment.py")
    print("  4. Analyze results: python analyze_results.py")
    print("\n  Or run full pipeline: python run_phase1.py")
    print("="*70 + "\n")
    
    return 0 if critical_passed else 1


if __name__ == "__main__":
    sys.exit(main())
