"""Quick status check for running experiment."""

import json
from pathlib import Path
from datetime import datetime

print("="*70)
print(" EXPERIMENT STATUS CHECK")
print(f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

# Check if experiment is running
checkpoint_file = Path("partA_checkpoint.json")
log_file = Path("partA_progress.log")

if not log_file.exists():
    print("\n⏳ Experiment starting... (no log file yet)")
    print("   This is normal - model is loading.")
    print("   Wait 2-3 minutes for LLaMA-2 to load.")
else:
    print("\n📋 PROGRESS LOG:")
    print("-" * 70)
    with open(log_file, "r") as f:
        lines = f.readlines()
        # Show last 10 lines
        for line in lines[-10:]:
            print(line.rstrip())
    print("-" * 70)

if checkpoint_file.exists():
    with open(checkpoint_file, "r") as f:
        cp = json.load(f)
    
    print(f"\n📊 LIVE STATISTICS:")
    print("-" * 70)
    print(f"Current Model:       {cp['model']}")
    print(f"Completed:           {cp['queries_completed']}/200 queries")
    
    results = cp['results']
    injected = [r for r in results if r['is_injected']]
    successful = [r for r in injected if r['injection_success']]
    
    if injected:
        asr = (len(successful) / len(injected)) * 100
        print(f"Current ASR:         {asr:.1f}% ({len(successful)}/{len(injected)})")
        
        # Show attack type breakdown
        print(f"\nAttack type breakdown:")
        evasion_types = {}
        for r in injected:
            et = r.get('evasion_type', 'unknown')
            if et not in evasion_types:
                evasion_types[et] = {'total': 0, 'success': 0}
            evasion_types[et]['total'] += 1
            if r['injection_success']:
                evasion_types[et]['success'] += 1
        
        for et, stats in sorted(evasion_types.items()):
            et_asr = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {et:20s}: {et_asr:5.1f}% ({stats['success']}/{stats['total']})")
    
    if results:
        avg_time = sum(r.get('generation_time_sec', 0) for r in results) / len(results)
        print(f"\nAvg Gen Time:        {avg_time:.2f}s per query")
        
        remaining = 200 - cp['queries_completed']
        eta_min = (remaining * avg_time) / 60
        print(f"ETA (this model):    ~{eta_min:.1f}min")
    
    print("-" * 70)
else:
    print("\n📊 No checkpoint yet - experiment just started")

print("\n💡 TIP: Run 'python monitor_progress.py' in another terminal for live updates!")
print("="*70)
