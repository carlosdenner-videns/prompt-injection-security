"""Check if partA experiment process is running."""

import subprocess
import sys

print("Checking for running Python processes...")

try:
    # Get all Python processes
    result = subprocess.run(
        ['powershell', '-Command', "Get-Process python -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,CPU,WorkingSet"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    print(result.stdout)
    
    if "python" not in result.stdout.lower():
        print("\n⚠️ WARNING: No Python processes found!")
        print("The experiment may have crashed or not started.")
        print("\nTry restarting manually:")
        print("  python partA_experiment.py")
    else:
        print("\n✓ Python processes are running")
        print("The model may still be loading (LLaMA-2 can be slow).")
        
except Exception as e:
    print(f"Error checking processes: {e}")
