#!/usr/bin/env python3
"""
Fix all Figure 16 generation scripts - remove "Figure 16:" prefix
"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

# Find all Figure 16 generation scripts
fig16_scripts = list(SCRIPT_DIR.glob("generate_figure_16*.py"))

print(f"Found {len(fig16_scripts)} Figure 16 generation scripts")
print()

fixed_count = 0
skipped_count = 0

for script in fig16_scripts:
    print(f"Processing: {script.name}")
    
    # Read the file
    with open(script, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it has "Figure 16:" prefix
    if "Figure 16:" in content:
        # Remove "Figure 16: " from title
        original_content = content
        content = re.sub(
            r"(ax\.text\([^,]+,\s*[^,]+,\s*['\"])Figure 16:\s*",
            r"\1",
            content
        )
        
        if content != original_content:
            # Write back
            with open(script, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Fixed: Removed 'Figure 16:' prefix")
            fixed_count += 1
        else:
            print(f"  ⚠ Pattern not found for replacement")
            skipped_count += 1
    else:
        print(f"  ✓ Already correct (no 'Figure 16:' prefix)")
        skipped_count += 1
    print()

print("=" * 70)
print(f"Fixed: {fixed_count} scripts")
print(f"Skipped (already correct): {skipped_count} scripts")
print("=" * 70)
