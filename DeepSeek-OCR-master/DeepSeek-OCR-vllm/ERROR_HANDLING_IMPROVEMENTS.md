# Error Handling Improvements

## Overview
This document describes the comprehensive error handling improvements made to prevent application crashes and enable partial result downloads when processing fails.

## Problem Statement
The application was exiting (process killed with exit code 137) when encountering:
- `TimeoutError` - Engine iteration timeouts
- `AsyncEngineDeadError` - Engine background task failures
- `CancelledError` - Asyncio task cancellations
- Memory pressure causing OOM kills

Users lost all progress when errors occurred, with no way to download completed pages.

## Solutions Implemented

### 1. **Global Processing State Tracking**
Added `processing_state` dictionary to track:
- `completed_files`: List of successfully saved chunk files
- `failed_pages`: List of pages that failed with error details
- `current_chunk` / `total_chunks`: Progress tracking
- `processing_active`: Boolean flag for active processing

### 2. **Comprehensive Error Handling in PDF Processing**

#### Per-Page Error Handling
- Wrapped each page generation in try-catch blocks
- Pages that fail are marked with error messages instead of crashing
- Failed pages tracked in `processing_state['failed_pages']`
- Processing continues to next page even after failures

#### Per-Batch Error Handling  
- Batch processing wrapped in try-catch with async error protection
- Errors caught at multiple levels:
  - AsyncEngineDeadError → triggers engine restart
  - TimeoutError → retry with backoff
  - General exceptions → logged and continue

#### Chunk-Level Error Handling
- Each chunk processing wrapped in try-catch
- Completed chunks saved immediately to disk
- Partial results preserved even if later chunks fail

### 3. **Immediate File Saving**
- Files saved to disk as soon as each chunk completes
- Tracked in `processing_state['completed_files']`
- Enables partial downloads even if processing crashes mid-way

### 4. **UI Error Display Without Crashing**

#### PDF Wrapper Function
- Wrapped `process_ocr_pdf()` calls in additional try-catch
- Catches any unhandled exceptions and displays user-friendly messages
- Application continues running after errors

#### Summary Messages
- Success: Shows count of generated files
- Partial success: Shows completed files + failed page list
- Error: Shows error message + partial results if available

#### Cancellation Handling
- Returns completed files when user cancels
- Shows completion status before cancellation

### 5. **Memory Monitoring and OOM Prevention**

#### GPU Memory Monitoring
Enhanced `check_gpu_memory()`:
- Monitors allocated/reserved/total GPU memory
- Clears cache when usage exceeds threshold
- Tracks consecutive high-pressure events

#### System RAM Monitoring
New `check_system_memory()` function:
- Uses `psutil` to check system RAM usage
- Warns at 80% usage
- Stops processing at 90% to prevent OOM kill
- Returns completed files before stopping

#### Proactive Memory Checks
- Check before processing each batch
- Stop gracefully if memory critical
- Return partial results instead of crash

### 6. **Engine Error Recovery**

#### Failed Page Tracking
- Each failed page recorded with:
  - Page number
  - Error type
  - Chunk index
  
#### Automatic Engine Restart
- Critical errors trigger engine restart:
  - AsyncEngineDeadError
  - CUDA errors
  - "Dead" or "Killed" errors
- Engine restarted between chunks for stability
- Non-critical errors retry without restart

## User Experience Improvements

### Before
```
ERROR: AsyncEngineDeadError
Process killed with exit code 137
All progress lost
```

### After
```
⚠️ 3 page(s) failed to process
Failed pages: 108, 125, 142
✓ Generated 5 file(s)

[Download button enabled with partial results]
```

## Error Message Examples

### Complete Success
```
✓ Generated 10 file(s)
```

### Partial Success
```
⚠️ 5 page(s) failed to process
Failed pages: 108, 125, 142, 156, 189
✓ Generated 8 file(s)
```

### Error with Partial Results
```
❌ Processing error: Engine failed after 2 retries

⚠️ Partial results available (3 file(s) completed before error)
```

### Memory Critical Stop
```
⚠️ Critical system memory pressure detected. Stopping to prevent OOM kill.
✓ 5 file(s) completed before stopping.
```

### Cancellation with Partial Results
```
Processing cancelled by user.
✓ 3 file(s) completed before cancellation.
```

## Technical Details

### Error Handling Flow
```
PDF Processing
├── Outer try-catch (critical errors)
│   ├── Chunk Loop
│   │   ├── Memory check (stop if critical)
│   │   ├── Engine restart (between chunks)
│   │   ├── Batch Loop
│   │   │   ├── Memory check (skip if pressure)
│   │   │   ├── Batch try-catch
│   │   │   │   ├── Async execution wrapper
│   │   │   │   ├── Engine recovery wrapper
│   │   │   │   └── Per-page try-catch
│   │   │   └── Save results (mark errors)
│   │   └── Save chunk immediately
│   └── Return partial results on error
└── Finally: Reset processing state
```

### File Saving Strategy
1. Process pages in batch
2. Format results (including errors)
3. Save chunk immediately to disk
4. Add to `completed_files` list
5. Continue to next chunk
6. On error: return `completed_files`

### Memory Protection Levels
1. **GPU Memory** (75% threshold):
   - Clear cache
   - Increment pressure counter
   - Skip batch if pressure > 2

2. **System RAM** (80% warning, 90% critical):
   - Warn at 80%
   - Stop processing at 90%
   - Return completed files

## Configuration Recommendations

### For Stability
```python
max_pages: 30-40 per chunk
batch_size: 1-2 pages
chunk_size: 30-40 pages
```

### Why These Values?
- **max_pages**: Limits total processing scope
- **batch_size**: 1-2 prevents memory spikes
- **chunk_size**: 30-40 allows engine restarts without too many files

## Testing Recommendations

1. **Timeout Scenarios**: Test with complex pages that timeout
2. **Memory Pressure**: Test with limited GPU memory
3. **Engine Failures**: Test with unstable engine conditions
4. **Cancellation**: Test mid-processing cancellation
5. **Partial Results**: Verify files downloadable after errors

## Future Enhancements

1. **Resume from Checkpoint**: Save progress to allow resuming failed jobs
2. **Retry Queue**: Automatically retry failed pages with different settings
3. **Memory Prediction**: Estimate memory needs before processing
4. **Progressive Download**: Stream results as they complete
5. **Error Analytics**: Track error patterns for optimization

## Summary

These improvements ensure:
- ✅ **No more application crashes** on errors
- ✅ **Partial results always available** for download
- ✅ **Clear error messages** in UI
- ✅ **Memory pressure monitoring** prevents OOM kills
- ✅ **Graceful degradation** under resource constraints
- ✅ **Progress preservation** even when processing fails

The application now handles errors gracefully, preserves user work, and provides clear feedback about what succeeded and what failed.
