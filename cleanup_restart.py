"""Cleanup script for fresh experiment restart."""

import os
from pathlib import Path

print("🧹 Cleaning up old experiment files...")

# Remove old checkpoint and logs
files_to_remove = [
    "partA_checkpoint.json",
    "partA_progress.log", 
    "partA_results.json"
]

for file in files_to_remove:
    if Path(file).exists():
        Path(file).unlink()
        print(f"✓ Deleted {file}")
    else:
        print(f"  (no {file} to delete)")

print("\n📊 Verifying KB...")

# Check KB size
with open("partA_kb.jsonl", "r", encoding="utf-8") as f:
    kb_lines = sum(1 for _ in f)

print(f"KB size: {kb_lines} documents")

if kb_lines == 480:
    print("✓ KB has correct size (480 docs = 400 benign + 80 malicious)")
else:
    print(f"⚠ Warning: Expected 480 docs, got {kb_lines}")

# Check for new attack types
with open("partA_kb.jsonl", "r", encoding="utf-8") as f:
    content = f.read()
    
has_new = any(attack in content for attack in ["delimiter_attack", "role_confusion", "multilingual"])

if has_new:
    print("✓ New attack types detected in KB")
else:
    print("✗ Error: New attack types not found!")
    print("  Re-run: python generate_kb.py")
    exit(1)

print("\n🚀 Ready to restart experiment!")
print("Run: python partA_experiment.py")
