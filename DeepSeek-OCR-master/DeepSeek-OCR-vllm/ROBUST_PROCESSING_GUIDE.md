# Robust PDF Processing Guide

## Quick Start - Preventing Errors

### Recommended Settings for Stability
```
Max Pages: 30-40
Batch Size: 1-2
Chunk Size: 30-40
```

## What Happens When Errors Occur?

### ✅ **Your Work is Protected**
- Completed pages are saved immediately
- You can download partial results even if processing fails
- Failed pages are clearly marked
- Application continues running (no crashes!)

## Understanding Error Messages

### 📊 **Processing Summary**
After processing completes (or stops), you'll see:

```
⚠️ 3 page(s) failed to process
Failed pages: 108, 125, 142
✓ Generated 5 file(s)
```

**What this means:**
- 5 chunks/files were successfully created
- 3 pages failed (listed with page numbers)
- **You can download the 5 successful files**

### 💾 **Partial Results Available**
```
❌ Processing error: Engine timeout

⚠️ Partial results available (3 file(s) completed before error)
```

**What to do:**
1. Look for completed files in the dropdown
2. Click "Download All Files" to get what was completed
3. Try processing the remaining pages with smaller settings

### 🛑 **Memory Critical**
```
⚠️ Critical system memory pressure detected. Stopping to prevent OOM kill.
✓ 5 file(s) completed before stopping.
```

**What to do:**
1. Download the 5 completed files
2. Reduce batch size to 1
3. Reduce chunk size to 20-30
4. Close other applications to free memory
5. Try processing remaining pages

### ⏸️ **User Cancellation**
```
Processing cancelled by user.
✓ 3 file(s) completed before cancellation.
```

**What to do:**
1. Download the 3 completed files
2. Note which pages were processed
3. Adjust settings if needed
4. Continue with remaining pages

## Common Issues and Solutions

### Issue: Pages Timing Out
**Symptoms:**
```
⚠️ 5 page(s) failed to process
Failed pages: 108, 125, 142, 156, 189
```

**Solutions:**
1. Reduce batch size to 1
2. Reduce chunk size to 30
3. These pages may be complex - try processing them individually
4. Check if these pages have many images or complex layouts

### Issue: Memory Warnings
**Symptoms:**
```
⚠️ WARNING: System RAM usage at 85% - approaching limits
```

**Solutions:**
1. **Immediate:** Reduce batch size to 1
2. Close other applications
3. Reduce chunk size to 20-30
4. Consider processing fewer pages at a time (max_pages: 20)
5. If running in WSL, increase WSL memory limit

### Issue: Engine Errors
**Symptoms:**
```
AsyncEngineDeadError
TimeoutError
Engine restart required
```

**What happens automatically:**
- Engine restarts between chunks
- Failed pages marked with errors
- Processing continues with next page
- Completed pages saved

**What you should do:**
- Download partial results
- Wait for engine to restart (happens automatically)
- Try again with smaller settings

### Issue: Process Killed (Exit 137)
**Prevention measures now active:**
1. System memory monitoring
2. Automatic stop before OOM
3. Partial results saved
4. Clear error messages

**If it still happens:**
1. Your system is out of memory
2. Close ALL other applications
3. Use these ultra-conservative settings:
   ```
   Max Pages: 20
   Batch Size: 1
   Chunk Size: 20
   ```

## Best Practices

### 📝 **For Large PDFs (100+ pages)**
1. Set Max Pages: 40
2. Set Batch Size: 1
3. Set Chunk Size: 40
4. Process in multiple runs if needed
5. Download completed files after each run

### 🖼️ **For Image-Heavy PDFs**
1. Set Batch Size: 1
2. Reduce Chunk Size: 30
3. Enable Cropping: Yes
4. Monitor memory warnings

### ⚡ **For Fast Processing**
1. Start with default settings
2. Monitor for errors
3. Reduce settings if you see failures
4. Download partial results regularly

### 🔄 **For Resuming Failed Jobs**
1. Note which pages completed (check file names)
2. Upload same PDF again
3. Adjust settings based on error messages
4. Process remaining pages
5. Combine markdown files manually

## Downloading Results

### Multiple Chunk Files
1. Use dropdown to preview each file
2. Click "Download All Files" for ZIP
3. ZIP contains all completed chunks

### Single File
1. File available in dropdown
2. Click download button
3. Or copy text from preview

## Memory Management Tips

### Check Memory Usage
- Watch for warnings in the output
- Green: < 75% GPU, < 80% RAM ✅
- Yellow: 75-85% ⚠️
- Red: > 85% 🛑

### Free Memory
```bash
# In WSL terminal
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'

# In Python/Terminal
pkill -f gradio_app.py
# Then restart application
```

### Adjust WSL Memory (if needed)
Create/edit `~/.wslconfig`:
```ini
[wsl2]
memory=16GB
processors=4
```

## Error Recovery Flowchart

```
Processing Fails
    ↓
Check Error Message
    ↓
┌───────────────────────────────┐
│ Partial Results Available?    │
│ YES → Download them first     │
│ NO → Check error type         │
└───────────────────────────────┘
    ↓
┌───────────────────────────────┐
│ Memory Error?                 │
│ YES → Reduce settings         │
│ NO → Check timeout errors     │
└───────────────────────────────┘
    ↓
┌───────────────────────────────┐
│ Timeout Errors?               │
│ YES → Reduce batch/chunk size │
│ NO → Engine error            │
└───────────────────────────────┘
    ↓
Try Again with New Settings
    ↓
Download Partial Results
```

## Quick Settings Reference

| Scenario | Max Pages | Batch | Chunk | Cropping |
|----------|-----------|-------|-------|----------|
| **Stable Default** | 40 | 1 | 40 | Yes |
| **Memory Limited** | 20 | 1 | 20 | Yes |
| **Fast Processing** | 0 (all) | 2 | 50 | No |
| **Complex Pages** | 30 | 1 | 30 | Yes |
| **Ultra Safe** | 20 | 1 | 20 | No |

## Questions & Troubleshooting

### Q: Why did some pages fail?
**A:** Pages can fail due to:
- Complexity (many images/formulas)
- Memory pressure
- Engine timeouts
- CUDA errors

**Action:** Download successful pages, try failed pages separately

### Q: Can I resume processing?
**A:** Not automatically, but you can:
1. Note which pages completed
2. Process remaining pages separately
3. Combine markdown files manually

### Q: Will I lose all my work?
**A:** No! The new error handling:
- Saves pages immediately
- Preserves partial results
- Allows downloading completed work
- Prevents application crashes

### Q: What if the application crashes anyway?
**A:** Check the `output/` folder:
- Completed chunk files are saved there
- Named with pattern: `{filename}_chunk_{number}.md`
- You can recover these manually

## Contact & Support

If you encounter persistent issues:
1. Check `output/` folder for partial results
2. Review error messages in terminal
3. Try ultra-safe settings first
4. Report bugs with error logs

## Summary

🎯 **Key Takeaways:**
- ✅ Errors don't crash the application anymore
- ✅ Partial results are always saved and downloadable
- ✅ Clear error messages guide you
- ✅ Memory monitoring prevents OOM kills
- ✅ Engine automatically recovers from errors
- ✅ You can always download what was completed

**Remember:** Start with recommended settings, monitor errors, adjust as needed!
