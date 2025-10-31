"""
Phase 2: Main Orchestrator Script
Runs complete Phase 2 pipeline: evaluation, ablation, and visualization.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(text)
    print("="*70)


def run_script(script_name, description):
    """Run a Python script and report status."""
    print(f"\n🚀 Running: {description}")
    print(f"Script: {script_name}")
    
    script_path = Path(__file__).parent / script_name
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in {description}: {e}")
        return False


def main():
    """Run complete Phase 2 pipeline."""
    start_time = datetime.now()
    
    print_header("PHASE 2: DEFENSE DEVELOPMENT AND EVALUATION")
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Evaluate classifiers
    if not run_script("evaluate_classifiers.py", "Classifier Evaluation (v1, v2, v3)"):
        print("\n❌ Pipeline aborted due to error")
        return 1
    
    # Step 2: Ablation study
    if not run_script("ablation_analysis.py", "Ablation Study"):
        print("\n❌ Pipeline aborted due to error")
        return 1
    
    # Step 3: Generate visualizations
    if not run_script("generate_plots.py", "Plot Generation"):
        print("\n❌ Pipeline aborted due to error")
        return 1
    
    # Success!
    end_time = datetime.now()
    duration = end_time - start_time
    
    print_header("PHASE 2 PIPELINE COMPLETE")
    print(f"Finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total duration: {duration.total_seconds():.1f} seconds")
    
    print("\n📊 Generated outputs:")
    print("  ✓ phase2/results/classifier_metrics.csv")
    print("  ✓ phase2/results/detections_v1.csv")
    print("  ✓ phase2/results/detections_v2.csv")
    print("  ✓ phase2/results/detections_v3.csv")
    print("  ✓ phase2/results/ablation_detailed.csv")
    print("  ✓ phase2/results/ablation_summary.csv")
    print("  ✓ phase2/plots/classifier_comparison.png")
    print("  ✓ phase2/plots/confusion_matrices.png")
    print("  ✓ phase2/plots/defense_overlap.png")
    print("  ✓ phase2/plots/performance_progression.png")
    
    print("\n" + "="*70)
    print("Next steps:")
    print("  1. Review plots in phase2/plots/")
    print("  2. Analyze detailed results in phase2/results/")
    print("  3. Read PHASE2_ANALYSIS_REPORT.md for comprehensive findings")
    print("  4. Consider baseline comparisons (NeMo, Moderation API)")
    print("="*70 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
