# Progress Tracking Quick Reference

## 🎯 What You'll See During Experiments

### Main Terminal (Running Experiment)

```
[1/2] falcon-7b |████████░░░░░░░░| 45/200 [00:32<01:10, 2.2query/s] ASR:67.3%
```

**Reading the progress bar:**
- `[1/2]` - Model 1 of 2 (currently on first model)
- `falcon-7b` - Current model being tested
- `████████░░░` - Visual progress bar
- `45/200` - Completed 45 out of 200 queries/cases
- `[00:32<01:10]` - 32 seconds elapsed, 1 min 10 sec remaining
- `2.2query/s` - Processing speed (queries or cases per second)
- `ASR:67.3%` - Current Attack Success Rate (live updated)

### Second Terminal (Live Monitor)

Open another terminal and run:
```powershell
python monitor_progress.py
```

You'll see:
```
======================================================================
 PART A LIVE PROGRESS MONITOR
 2025-10-30 10:15:32
======================================================================

📋 RECENT LOG ENTRIES:
----------------------------------------------------------------------
Part A Experiment Started: 2025-10-30T10:05:15
Models: ['llama2-7b', 'falcon-7b']
Test queries: 200
============================================================

[10:07:42] falcon-7b - Query 20/200
  Current ASR: 65.00% (13/20)
  Avg generation time: 1.45s
  ETA for this model: 4.3 minutes

[10:10:15] falcon-7b - Query 40/200
  Current ASR: 67.50% (27/40)
  Avg generation time: 1.42s
  ETA for this model: 3.8 minutes
----------------------------------------------------------------------

📊 LIVE STATISTICS:
----------------------------------------------------------------------
Current Model:       falcon-7b
Completed:           45 queries
Current ASR:         67.3% (30/45)
Avg Gen Time:        1.43s per query
Avg Throughput:      28.5 tokens/sec
Last Checkpoint:     2025-10-30T10:12:30
ETA (this model):    ~3.7min
----------------------------------------------------------------------

🔄 Auto-refresh every 5 seconds | Press Ctrl+C to stop
```

---

## 📁 Progress Files Generated

### During Experiment

**Part A:**
- `partA_progress.log` - Timestamped log entries (text file)
- `partA_checkpoint.json` - Resume data (auto-deleted when model completes)

**Part B:**
- `partB_progress.log` - Timestamped log entries (text file)
- `partB_checkpoint.json` - Resume data (auto-deleted when model completes)

### After Completion

**Final Results:**
- `partA_results.json` or `partB_results.json` - Complete experimental data

**Checkpoint files are automatically deleted** when a model finishes successfully.

---

## 🔄 Checkpoint & Resume System

### Automatic Checkpoints

**Part A:** Saves every **20 queries**
**Part B:** Saves every **10 cases**

### If Experiment Stops

1. **Power loss**, **crash**, or **Ctrl+C** → Checkpoint saved
2. **Re-run same command** → Automatically resumes
3. **Progress preserved** → Picks up where it left off

Example output when resuming:
```
Testing model: falcon-7b
============================================================

✓ Resumed from checkpoint: 80/200 queries completed

[1/2] falcon-7b |████████░░░░░░░░| 80/200 [01:55<02:25, 2.1query/s] ASR:68.1%
```

### Manual Resume Control

To start fresh (ignore checkpoint):
```python
# In partA_experiment.py or partB_experiment.py
experiment.run_experiment(resume_from_checkpoint=False)
```

---

## 📊 What Gets Logged

### Every Checkpoint (20 queries / 10 cases)

```
[10:15:42] falcon-7b - Query 80/200
  Current ASR: 68.75% (55/80)
  Avg generation time: 1.43s
  ETA for this model: 2.9 minutes
```

**Includes:**
- ⏰ Timestamp
- 🎯 Progress counter
- 📈 Current ASR with success/total counts
- ⚡ Average generation time per query/case
- ⏱️ Estimated time remaining for current model

### Model Completion

```
[10:18:35] ✓ falcon-7b COMPLETED
  Final ASR: 69.00%
  Total queries: 200
```

---

## 🛠️ Troubleshooting Progress Tracking

### Progress Bar Not Updating?

**Possible causes:**
1. Model is loading (takes 1-2 minutes first time)
2. Very slow query (complex injection, long context)
3. GPU bottleneck

**Check:**
- Monitor shows last checkpoint time
- Log file shows recent activity
- GPU usage (Task Manager → Performance → GPU)

### Monitor Says "No Active Experiment"?

**Solution:**
1. Make sure experiment is actually running
2. Check files exist:
   ```powershell
   Get-ChildItem *progress.log, *checkpoint.json
   ```
3. Specify experiment type explicitly:
   ```powershell
   python monitor_progress.py A  # For Part A
   python monitor_progress.py B  # For Part B
   ```

### Checkpoint Not Resuming?

**Check:**
1. Checkpoint file exists: `partA_checkpoint.json` or `partB_checkpoint.json`
2. Model name matches (checkpoint is model-specific)
3. Resume enabled (default: True)

**Force fresh start:**
```powershell
# Delete checkpoint files
Remove-Item *checkpoint.json

# Then re-run experiment
python partA_experiment.py
```

---

## 💡 Pro Tips

### 1. Always Use Two Terminals

**Terminal 1:** Run experiment
**Terminal 2:** Monitor progress

This lets you:
- See detailed stats without cluttering main output
- Check progress without interrupting experiment
- Get better ETA estimates

### 2. Check Logs Anytime

```powershell
# View last 20 lines, auto-update
Get-Content partA_progress.log -Tail 20 -Wait

# View entire log
Get-Content partA_progress.log

# Search for specific model
Get-Content partA_progress.log | Select-String "llama2"
```

### 3. Adjust Checkpoint Frequency

**More frequent** (safer, more I/O):
```python
experiment.run_experiment(checkpoint_every=10)  # Part A: every 10 queries
```

**Less frequent** (faster, less safe):
```python
experiment.run_experiment(checkpoint_every=50)  # Part A: every 50 queries
```

### 4. Monitor GPU Usage

While experiment runs:
```powershell
# Open Task Manager
# Performance tab → GPU
# Watch GPU Utilization and Memory
```

Should see:
- GPU Utilization: 80-100% (good)
- GPU Memory: 6-8 GB used (normal for 7B models)

---

## 📈 Expected Progress Timeline

### Part A (200 queries, 2 models)

```
00:00 - KB Generation
00:01 - Loading falcon-7b model
00:03 - Start queries
01:30 - Checkpoint: 100/200 (50%) ASR: ~65%
02:45 - falcon-7b complete (Final ASR: ~67%)
02:47 - Loading llama2-7b model
02:49 - Start queries
04:20 - Checkpoint: 100/200 (50%) ASR: ~62%
05:35 - llama2-7b complete (Final ASR: ~64%)
05:36 - Part A DONE ✓
```

### Part B (72 cases, 2 models)

```
00:00 - Loading falcon-7b model
00:02 - Start cases
00:45 - Checkpoint: 36/72 (50%) ASR: ~72%
01:25 - falcon-7b complete (Final ASR: ~74%)
01:27 - Loading llama2-7b model
01:29 - Start cases
02:15 - Checkpoint: 36/72 (50%) ASR: ~69%
02:50 - llama2-7b complete (Final ASR: ~71%)
02:51 - Part B DONE ✓
```

**Total:** 5-6 hours for complete Phase 1

---

## 🎯 What Success Looks Like

### Healthy Progress

✅ Progress bar advancing steadily  
✅ ASR updating (between 50-80% typical)  
✅ Tokens/sec around 25-35 (GPU) or 3-5 (CPU)  
✅ Checkpoints saving regularly  
✅ ETA decreasing over time  

### Warning Signs

⚠️ Progress frozen for >5 minutes  
⚠️ ASR at 0% or 100% (check for bugs)  
⚠️ Tokens/sec < 1 (very slow, GPU issue?)  
⚠️ No checkpoints being saved  
⚠️ GPU memory at 0% (not using GPU)  

---

## 📞 Quick Commands Reference

```powershell
# Start Part A
python partA_experiment.py

# Monitor Part A (separate terminal)
python monitor_progress.py A

# Watch Part A log
Get-Content partA_progress.log -Tail 20 -Wait

# Start Part B
python partB_experiment.py

# Monitor Part B (separate terminal)
python monitor_progress.py B

# Watch Part B log
Get-Content partB_progress.log -Tail 20 -Wait

# Full pipeline (all steps)
python run_phase1.py

# Check GPU status
nvidia-smi  # If NVIDIA drivers installed
```

---

**Ready to start?** Open two terminals and run:

**Terminal 1:**
```powershell
python partA_experiment.py
```

**Terminal 2:**
```powershell
python monitor_progress.py
```

Sit back and watch the science happen! ☕🔬
