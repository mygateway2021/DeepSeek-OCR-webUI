# Quick Fix Guide: OOM (Exit Code 137) and Timeout Errors

## What Was Fixed

✅ **Exit Code 137 (OOM Killer)** - Process being killed by system
✅ **vLLM Engine Timeout** - "Engine iteration timed out" errors  
✅ **Background Loop Errors** - Cascade failures after timeout
✅ **AsyncEngineDeadError** - Unresponsive engine issues

## Key Changes

### 1. Automatic Engine Restart
- Engine automatically restarts after 3 consecutive errors
- Detects critical errors (dead engine, CUDA errors, OOM)
- Force restart capability with cleanup

### 2. Retry Logic with Timeout Protection
- Each page gets 2 retry attempts (180s per page)
- Exponential backoff between retries
- Per-page error isolation (one failure doesn't stop batch)

### 3. Memory Pressure Protection
- Monitors GPU and CPU memory usage
- Skips batches automatically when pressure is high
- Tracks and reports memory trends

### 4. Reduced Resource Usage
- GPU memory: 35% (was 40%)
- Max sequences: 16 (was 32)
- Batch tokens: 1536 (was 2048)
- Generation tokens: 1024 per page

## How to Use

### Start the Application
```bash
bash improved_launch_gradio_wsl.sh
```

The enhanced monitoring will show:
- Memory status checks
- OOM handling configuration
- Real-time memory alerts

### Process PDFs Safely

**For Small PDFs (<10 pages):**
- Use default settings
- Batch size: 2 pages
- Watch console for warnings

**For Large PDFs (>10 pages):**
- Reduce max_pages: Try 20-30 pages first
- Batch size: 1-2 pages
- Results saved to separate files

**If You See Exit Code 137:**
1. Reduce max_pages to 10
2. Set batch_size to 1
3. Disable cropping if possible
4. Close other GPU applications

**If You See Timeout Errors:**
- Engine will auto-restart (wait 2-5 seconds)
- Processing will continue with remaining pages
- Partial results are saved

## What to Watch For

### Good Messages
```
✓ Engine initialized successfully
GPU Memory - Allocated: X.XXG B (Usage: 65.2%)
```

### Warning Messages
```
WARNING: High GPU memory usage (78%)
[BATCH] Error on page X, attempt 1
[MEMORY] High memory pressure detected
```
**Action**: Reduce batch size or max_pages

### Critical Messages
```
CRITICAL: GPU memory usage: 92%
URGENT: System may trigger OOM killer soon!
[ENGINE] Critical error detected, restarting engine
Process exited with code 137
```
**Action**: Restart with smaller settings

## Emergency Recovery

If the app crashes with exit code 137:

```bash
# 1. Check memory
free -h

# 2. Clear GPU memory
# Close any other GPU apps

# 3. Restart with reduced settings
bash improved_launch_gradio_wsl.sh

# 4. In the web interface:
#    - Set max_pages to 5
#    - Set batch_size to 1
#    - Try again
```

## Settings for Different Scenarios

### High-Quality Books (Many Pages)
```
Max Pages: 20
Batch Size: 1
Enable Cropping: ✓
```

### Simple Documents
```
Max Pages: 0 (all pages)
Batch Size: 2
Enable Cropping: ✗
```

### If Memory is Limited
```
Max Pages: 10
Batch Size: 1
Enable Cropping: ✗
Use "Free OCR" prompt (simpler)
```

## Success Indicators

✅ Engine restarts automatically on errors  
✅ Individual pages can fail without stopping the batch  
✅ Partial results saved to files  
✅ Memory warnings show before OOM  
✅ Processing continues after timeouts  

## Getting Help

If issues persist:

1. Check `OOM_AND_TIMEOUT_FIXES.md` for detailed explanation
2. Look at console logs for specific error messages
3. Try processing just 1 page to isolate the issue
4. Verify system has adequate memory: `free -h`
5. Check GPU availability: `nvidia-smi`

## Performance Notes

- Processing may be 10-15% slower due to safety checks
- But reliability is MUCH higher for long-running tasks
- Memory usage is more stable
- Fewer unexpected crashes

---

**Last Updated**: Based on fixes for exit code 137 and vLLM timeout errors
