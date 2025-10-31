"""Analyze false positives from classifiers."""
import pandas as pd
from pathlib import Path

script_dir = Path(__file__).parent
phase2_dir = script_dir.parent

# Load results
v1_df = pd.read_csv(phase2_dir / "results" / "detections_v1.csv")
v2_df = pd.read_csv(phase2_dir / "results" / "detections_v2.csv")
v3_df = pd.read_csv(phase2_dir / "results" / "detections_v3.csv")

print("="*70)
print("FALSE POSITIVE ANALYSIS")
print("="*70)

# Find false positives (samples incorrectly flagged as attacks)
# Ground truth: is_injected AND injection_success = actual attack
# False positive: NOT(is_injected AND injection_success) but detected=True

v1_fp = v1_df[~(v1_df['is_injected'] & v1_df['injection_success']) & (v1_df['detected'] == True)]
v2_fp = v2_df[~(v2_df['is_injected'] & v2_df['injection_success']) & (v2_df['detected'] == True)]
v3_fp = v3_df[~(v3_df['is_injected'] & v3_df['injection_success']) & (v3_df['detected'] == True)]

print(f"\nV1 False Positives: {len(v1_fp)}")
if len(v1_fp) > 0:
    for idx, row in v1_fp.iterrows():
        print(f"  Query: {row['query']}")
        print(f"  Patterns: {row['matched_patterns']}")
        print()

print(f"\nV2 False Positives: {len(v2_fp)}")
if len(v2_fp) > 0:
    for idx, row in v2_fp.iterrows():
        print(f"  Query: {row['query']}")
        print(f"  Patterns: {row['matched_patterns']}")
        print()

print(f"\nV3 False Positives: {len(v3_fp)}")
if len(v3_fp) > 0:
    for idx, row in v3_fp.iterrows():
        print(f"  Query: {row['query']}")
        print(f"  Patterns: {row['matched_patterns']}")
        print()

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"V1: {len(v1_fp)} false positives")
print(f"V2: {len(v2_fp)} false positives")
print(f"V3: {len(v3_fp)} false positives")
