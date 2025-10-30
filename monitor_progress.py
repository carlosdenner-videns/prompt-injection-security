"""
Live progress monitor for Phase 1 experiments.
Run this in a separate terminal to watch experiment progress in real-time.
"""

import time
import sys
from pathlib import Path
from datetime import datetime
import json


def clear_screen():
    """Clear terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def format_eta(seconds):
    """Format ETA in human-readable format."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}min"
    else:
        return f"{seconds/3600:.1f}hr"


def monitor_experiment(experiment_type="A"):
    """
    Monitor experiment progress in real-time.
    
    Args:
        experiment_type: "A" for Part A or "B" for Part B
    """
    log_file = Path(f"part{experiment_type}_progress.log")
    checkpoint_file = Path(f"part{experiment_type}_checkpoint.json")
    
    print(f"="*70)
    print(f" MONITORING PART {experiment_type} EXPERIMENT")
    print(f"="*70)
    print(f"\nWatching: {log_file}")
    print(f"Press Ctrl+C to stop monitoring\n")
    
    last_size = 0
    last_checkpoint_time = None
    
    try:
        while True:
            # Clear and redraw
            clear_screen()
            
            print(f"="*70)
            print(f" PART {experiment_type} LIVE PROGRESS MONITOR")
            print(f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"="*70)
            
            # Read log file
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    log_content = f.read()
                    
                    # Display last 25 lines
                    lines = log_content.strip().split("\n")
                    display_lines = lines[-25:] if len(lines) > 25 else lines
                    
                    print("\n📋 RECENT LOG ENTRIES:")
                    print("-" * 70)
                    for line in display_lines:
                        print(line)
                    print("-" * 70)
            else:
                print("\n⏳ Waiting for experiment to start...")
                print(f"   Looking for: {log_file}")
            
            # Read checkpoint for live stats
            print("\n📊 LIVE STATISTICS:")
            print("-" * 70)
            
            if checkpoint_file.exists():
                try:
                    with open(checkpoint_file, "r", encoding="utf-8") as f:
                        checkpoint = json.load(f)
                    
                    model = checkpoint.get("model", "Unknown")
                    completed = checkpoint.get("queries_completed" if experiment_type == "A" else "cases_completed", 0)
                    timestamp = checkpoint.get("timestamp", "")
                    results = checkpoint.get("results", [])
                    
                    # Calculate current stats
                    if experiment_type == "A":
                        injected = [r for r in results if r.get("is_injected")]
                        successes = sum(1 for r in injected if r.get("injection_success"))
                        total_injected = len(injected)
                        asr = successes / total_injected if total_injected > 0 else 0
                        label = "queries"
                    else:
                        attacks = [r for r in results if r.get("is_attack")]
                        successes = sum(1 for r in attacks if r.get("attack_success"))
                        total_attacks = len(attacks)
                        asr = successes / total_attacks if total_attacks > 0 else 0
                        label = "cases"
                    
                    # Calculate timing stats
                    if results:
                        gen_times = [r.get("generation_time_sec", 0) for r in results]
                        avg_time = sum(gen_times) / len(gen_times)
                        tokens_per_sec = [r.get("tokens_per_sec", 0) for r in results]
                        avg_tps = sum(tokens_per_sec) / len(tokens_per_sec)
                    else:
                        avg_time = 0
                        avg_tps = 0
                    
                    print(f"Current Model:       {model}")
                    print(f"Completed:           {completed} {label}")
                    print(f"Current ASR:         {asr:.1%} ({successes}/{total_injected if experiment_type == 'A' else total_attacks})")
                    print(f"Avg Gen Time:        {avg_time:.2f}s per {label[:-1]}")
                    print(f"Avg Throughput:      {avg_tps:.1f} tokens/sec")
                    print(f"Last Checkpoint:     {timestamp}")
                    
                    # Estimate remaining time for current model
                    if experiment_type == "A":
                        total_expected = 200  # Default query count
                    else:
                        total_expected = 72   # Default case count per model
                    
                    remaining = total_expected - completed
                    if remaining > 0 and avg_time > 0:
                        eta_seconds = remaining * avg_time
                        print(f"ETA (this model):    ~{format_eta(eta_seconds)}")
                    
                    last_checkpoint_time = checkpoint.get("timestamp")
                    
                except json.JSONDecodeError:
                    print("⚠ Checkpoint file is being written...")
                except Exception as e:
                    print(f"⚠ Error reading checkpoint: {e}")
            else:
                print("⏳ No checkpoint file yet...")
                print(f"   Looking for: {checkpoint_file}")
            
            print("-" * 70)
            print(f"\n🔄 Auto-refresh every 5 seconds | Press Ctrl+C to stop")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n✓ Monitoring stopped by user")
        sys.exit(0)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        exp_type = sys.argv[1].upper()
        if exp_type not in ["A", "B"]:
            print("Usage: python monitor_progress.py [A|B]")
            print("  A - Monitor Part A (RAG-borne injection)")
            print("  B - Monitor Part B (Schema smuggling)")
            sys.exit(1)
    else:
        # Try to detect which experiment is running
        if Path("partA_progress.log").exists() or Path("partA_checkpoint.json").exists():
            exp_type = "A"
            print("Auto-detected Part A experiment\n")
        elif Path("partB_progress.log").exists() or Path("partB_checkpoint.json").exists():
            exp_type = "B"
            print("Auto-detected Part B experiment\n")
        else:
            print("No active experiment detected.")
            print("\nUsage: python monitor_progress.py [A|B]")
            print("  A - Monitor Part A (RAG-borne injection)")
            print("  B - Monitor Part B (Schema smuggling)")
            sys.exit(0)
    
    monitor_experiment(exp_type)


if __name__ == "__main__":
    main()
