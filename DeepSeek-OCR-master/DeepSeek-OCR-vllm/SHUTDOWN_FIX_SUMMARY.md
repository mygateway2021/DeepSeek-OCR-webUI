# DeepSeek-OCR Automatic Shutdown Fix Summary - UPDATED

## Problem Identified

The DeepSeek-OCR application was experiencing:
1. **Automatic shutdowns** during long PDF processing sessions (OOM killer)
2. **CUDA out of memory errors** on 24GB GPU
3. **Port conflicts** preventing application startup
4. **CPU memory allocation failures**

## Root Causes

1. **High GPU Memory Utilization**: Original setting was 0.75 (75% of GPU memory)
2. **Large Token Limits**: Using 8192 max_tokens for PDF processing
3. **Memory Accumulation**: No garbage collection between PDF page processing
4. **No Timeout Handling**: Requests could run indefinitely
5. **Large Batch Sizes**: Processing too many pages simultaneously
6. **Port Conflicts**: No cleanup of existing processes

## Latest Fixes Applied (v2.0)

### 1. More Aggressive GPU Memory Management

**Before:**
```python
gpu_memory_utilization=0.75,
```

**After:**
```python
gpu_memory_utilization=0.4,  # Further reduced to 40% for 24GB GPU
max_num_seqs=32,  # Reduced concurrent sequences
max_num_batched_tokens=2048,  # Limit batched tokens
```

### 2. Drastically Reduced Token Limits

- **Single images**: 4096 → 1024 tokens (75% reduction)
- **PDF processing**: 8192 → 1024 tokens (87% reduction)

### 3. Smaller Batch Processing

- **Small PDFs**: 15 pages → 10 pages threshold
- **Effective batch size**: 3 → 2 pages maximum
- **File batches**: 10 → 5 pages per file

### 4. Enhanced Memory Management

```python
def clear_gpu_memory():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
        gc.collect()

def check_gpu_memory():
    # Monitor and auto-cleanup when >80% usage
```

### 5. Improved WSL Launcher with Port Management

```bash
# More conservative memory limits
ulimit -v 8388608   # 8GB virtual memory
ulimit -m 6291456   # 6GB resident memory

# Enhanced GPU settings
export CUDA_MEMORY_FRACTION=0.4
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:256,expandable_segments:True
export PYTORCH_NO_CUDA_MEMORY_CACHING=1

# Process and port cleanup
pkill -f "gradio_app.py"
# Auto-detect available ports 7860-7870
```

### 6. Port Conflict Resolution

- **Automatic port detection**: Tries ports 7860-7870
- **Process cleanup**: Kills existing gradio processes
- **Graceful fallback**: Multiple port attempts
- **Manual cleanup script**: `cleanup_processes.sh`

## Files Added/Modified (v2.0)

1. **`gradio_app.py`** - Core fixes + memory management + port flexibility
2. **`improved_launch_gradio_wsl.sh`** - Enhanced launcher with aggressive cleanup
3. **`cleanup_processes.sh`** - Manual process cleanup utility
4. **`SHUTDOWN_FIX_SUMMARY.md`** - This updated documentation

## Usage Instructions (v2.0)

### Method 1: Improved Launcher (Recommended)
```bash
chmod +x improved_launch_gradio_wsl.sh
./improved_launch_gradio_wsl.sh
```

### Method 2: Manual Cleanup + Launch
```bash
chmod +x cleanup_processes.sh
./cleanup_processes.sh
./improved_launch_gradio_wsl.sh
```

### Method 3: Emergency Recovery
```bash
pkill -f gradio_app.py
pkill -f "python.*gradio"
nvidia-smi  # Check GPU status
./improved_launch_gradio_wsl.sh
```

## Expected Results (v2.0)

✅ **No CUDA OOM errors** (40% GPU usage vs 75%)  
✅ **No port conflicts** (automatic detection + cleanup)  
✅ **Stable PDF processing** (1024 tokens, 2-page batches)  
✅ **Memory leak prevention** (aggressive cleanup)  
✅ **Process recovery** (automatic restart capabilities)  

## Configuration for 24GB GPU

The settings are now optimized for 24GB GPUs:
- **GPU Memory**: 40% utilization (~9.6GB allocated)
- **Batch Size**: Maximum 2 pages simultaneously
- **Token Limit**: 1024 tokens (fast processing)
- **Memory Monitoring**: Real-time cleanup triggers

## Troubleshooting (v2.0)

### If you still get CUDA OOM:
1. Run cleanup script: `./cleanup_processes.sh`
2. Reduce GPU fraction to 0.3: Edit `improved_launch_gradio_wsl.sh`
3. Process 1 page at a time: Set `max_pages=1` in UI

### If port conflicts persist:
1. Check processes: `ps aux | grep gradio`
2. Kill manually: `pkill -f gradio`
3. Check ports: `lsof -i:7860`

### If app crashes:
1. Check memory: `free -h`
2. Check GPU: `nvidia-smi`
3. Run cleanup: `./cleanup_processes.sh`
4. Restart: `./improved_launch_gradio_wsl.sh`

## Performance Recommendations

- **Start small**: Test with 1-2 page PDFs first
- **Monitor resources**: Watch GPU memory in nvidia-smi
- **Use max_pages**: Limit to 5-10 pages for large documents
- **Regular cleanup**: Run cleanup script between sessions

The v2.0 fixes should completely resolve the automatic shutdown issues while maintaining good performance for typical document processing tasks.