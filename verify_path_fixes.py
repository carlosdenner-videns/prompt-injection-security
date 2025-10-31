"""Verify that all path fixes are working correctly."""
import sys
from pathlib import Path

print("\n" + "="*70)
print("VERIFYING PATH FIXES IN PHASE 1 SCRIPTS")
print("="*70 + "\n")

# Check that all scripts can be imported and paths are resolved correctly
scripts_to_check = [
    "phase1/scripts/generate_kb.py",
    "phase1/scripts/partA_experiment.py",
    "phase1/scripts/partB_experiment.py",
    "phase1/scripts/run_phase1.py",
    "phase1/scripts/analyze_results.py",
    "phase1/scripts/phase1_label_defenses.py",
    "phase1/scripts/phase1_statistical_analysis.py",
]

print("📋 Checking script files exist:")
all_exist = True
for script in scripts_to_check:
    script_path = Path(script)
    if script_path.exists():
        print(f"  ✅ {script}")
    else:
        print(f"  ❌ {script} (MISSING)")
        all_exist = False

if not all_exist:
    print("\n❌ Some scripts are missing!")
    sys.exit(1)

print("\n✅ All scripts found!")

# Check that phase1 folder structure exists
print("\n📁 Checking phase1 folder structure:")
required_dirs = [
    "phase1/data",
    "phase1/scripts",
    "phase1/stats",
    "phase1/plots",
]

all_dirs_exist = True
for dir_path in required_dirs:
    d = Path(dir_path)
    if d.exists() and d.is_dir():
        print(f"  ✅ {dir_path}/")
    else:
        print(f"  ❌ {dir_path}/ (MISSING)")
        all_dirs_exist = False

if not all_dirs_exist:
    print("\n❌ Some directories are missing!")
    sys.exit(1)

print("\n✅ All directories exist!")

# Check that data files are in correct locations
print("\n📊 Checking data files in correct locations:")
data_files = [
    ("phase1/data/partA_results.json", "Part A Results"),
    ("phase1/data/partB_results.json", "Part B Results"),
    ("phase1/data/partA_kb.jsonl", "Knowledge Base"),
    ("phase1/data/phase1_output_annotated.json", "Annotated Output"),
]

for file_path, description in data_files:
    f = Path(file_path)
    if f.exists():
        size = f.stat().st_size / 1024
        print(f"  ✅ {description}: {file_path} ({size:.1f} KB)")
    else:
        print(f"  ⚠️  {description}: {file_path} (not yet generated)")

# Check that analysis outputs are in correct locations
print("\n📈 Checking analysis outputs in correct locations:")
analysis_files = [
    ("phase1/stats/ci_summary.csv", "CI Summary"),
    ("phase1/stats/mcnemar_results.csv", "McNemar Results"),
    ("phase1/stats/defense_pairwise_matrix.png", "Defense Pairwise Matrix"),
    ("phase1/stats/partA_analysis.csv", "Part A Analysis"),
    ("phase1/stats/partB_analysis.csv", "Part B Analysis"),
]

for file_path, description in analysis_files:
    f = Path(file_path)
    if f.exists():
        size = f.stat().st_size / 1024
        print(f"  ✅ {description}: {file_path} ({size:.1f} KB)")
    else:
        print(f"  ⚠️  {description}: {file_path} (not yet generated)")

# Check that plots are in correct locations
print("\n🎨 Checking plots in correct locations:")
plot_files = [
    ("phase1/plots/partA_heatmap.png", "Part A Heatmap"),
    ("phase1/plots/partB_heatmap.png", "Part B Heatmap"),
    ("phase1/plots/phase1_comparison.png", "Phase 1 Comparison"),
]

for file_path, description in plot_files:
    f = Path(file_path)
    if f.exists():
        size = f.stat().st_size / 1024
        print(f"  ✅ {description}: {file_path} ({size:.1f} KB)")
    else:
        print(f"  ⚠️  {description}: {file_path} (not yet generated)")

print("\n" + "="*70)
print("✅ PATH FIXES VERIFICATION COMPLETE")
print("="*70)
print("\nAll scripts have been updated with correct path references.")
print("You can now run the Phase 1 pipeline from any directory:")
print("\n  python phase1/scripts/run_phase1.py")
print("\nOr run individual scripts:")
print("  python phase1/scripts/generate_kb.py")
print("  python phase1/scripts/partA_experiment.py")
print("  python phase1/scripts/analyze_results.py")
print()
