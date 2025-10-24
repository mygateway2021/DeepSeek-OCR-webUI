# PDF Chunking System - Solution for Large PDF Processing

## Problem Solved

The original PDF processing was failing around page 100 with these errors:
- `Engine iteration timed out. This should never happen!`
- `AsyncEngineDeadError: Task finished unexpectedly`
- Process getting killed due to memory/timeout issues

## Solution Implemented

### 1. **Intelligent Page Chunking**
- **Chunk Size Control**: New slider to control pages per processing session (recommended: 50)
- **Automatic Engine Restart**: Engine restarts between chunks to prevent memory accumulation
- **Flexible Batch Size**: Reduced max batch size to 1-2 pages per batch for stability

### 2. **Enhanced Error Recovery**
- **Per-page Retry Logic**: Each page gets 2 attempts before being marked as failed
- **Engine Health Monitoring**: Automatic engine restart on critical errors
- **Memory Pressure Detection**: Skip processing when GPU memory is too high

### 3. **Optimized Processing Parameters**
- **Reduced Timeouts**: 120s per page (down from 180s)
- **Conservative Token Limits**: 1024 max tokens per page
- **Memory Cleanup**: Aggressive GPU memory clearing between batches

## Usage Guide

### For Small PDFs (≤50 pages)
1. **Max Pages**: Set to desired number (or 0 for all pages)
2. **Chunk Size**: 50 (single chunk processing)
3. **Batch Size**: 1-2 pages per batch
4. **Result**: Single text output

### For Large PDFs (>50 pages)
1. **Max Pages**: Set to 0 (process all) or limit to manageable number
2. **Chunk Size**: 50 pages (recommended for 24GB GPU)
3. **Batch Size**: 1 page per batch (most stable)
4. **Result**: Multiple markdown files + zip download

### For Very Large PDFs (500+ pages)
**Recommended Approach**: Process in iterations
- **Iteration 1**: Pages 1-100 (set max_pages=100)
- **Iteration 2**: Pages 101-200 (manually skip first 100)
- **Continue until complete**

## New UI Controls

### Chunk Size Slider (20-80 pages)
- **20-30 pages**: For high-resolution or complex documents
- **50 pages**: Recommended default for most documents
- **60-80 pages**: For simple text documents (use with caution)

### Enhanced Batch Size (1-5 pages)
- **1 page**: Most stable, recommended for complex documents
- **2 pages**: Good balance of speed and stability
- **3-5 pages**: Only for simple documents, higher risk of timeouts

### Max Pages with Chunking Info
- Shows "(建议≤50页/chunk)" to remind users of chunking behavior
- **0**: Process entire document with automatic chunking
- **>0**: Limit total pages processed

## Memory Management Features

### Automatic Memory Monitoring
- Tracks GPU memory usage before each batch
- Skips batches when memory pressure is too high
- Provides detailed memory usage logs

### Engine Health Tracking
- Monitors consecutive errors
- Forces engine restart after 2-3 critical errors
- Handles timeout and CUDA errors gracefully

### Progressive Cleanup
- GPU memory cleared after each batch
- Python garbage collection between chunks
- Wait periods to allow memory stabilization

## Error Handling Improvements

### Page-Level Recovery
- Individual page failures don't stop entire document
- Error pages marked with diagnostic information
- Processing continues to next page/batch

### Engine Recovery
- Automatic engine restart on critical failures
- Multiple retry attempts with exponential backoff
- Graceful degradation when engine becomes unstable

### File Output Strategy
- **Single chunk**: Combined text output
- **Multiple chunks**: Separate files for each chunk
- **Error recovery**: Partial results saved even on failures

## Performance Optimization

### Reduced Resource Usage
- **GPU Memory**: 35% utilization (down from 40%)
- **Max Sequences**: 16 concurrent (down from 32)
- **Batch Tokens**: 1536 tokens max (down from 2048)

### Timeout Management
- **Per-page timeout**: 120 seconds
- **Engine restart timeout**: Handled separately
- **Total processing**: No artificial time limits

## Monitoring and Debugging

### Enhanced Logging
```
[PDF] Processing 150 pages from PDF with 500 total pages
[PDF] Using chunk size: 50, batch size: 1
[PDF] Split into 3 chunks: [(0, 50), (50, 100), (100, 150)]
[PDF] Processing chunk 1/3: pages 1-50 (50 pages)
[PDF] Restarting engine before chunk 2
[ENGINE] Engine initialized successfully
```

### Memory Usage Tracking
```
GPU Memory - Allocated: 7.87GB, Reserved: 7.97GB, Total: 24.00GB (Usage: 32.8%)
[MEMORY] High memory pressure detected, skipping batch
```

### Error Classification
- **Timeout errors**: Page-level retries
- **Engine errors**: Engine restart required
- **Memory errors**: Batch skipping and cleanup
- **CUDA errors**: Full engine restart

## Best Practices

### For 24GB GPU (RTX 3090/4090)
- **Chunk Size**: 50 pages
- **Batch Size**: 1-2 pages
- **Complex documents**: Use chunk_size=30, batch_size=1

### For 12GB GPU (RTX 3060/4060)
- **Chunk Size**: 30 pages
- **Batch Size**: 1 page only
- **Monitor memory**: Watch for memory pressure warnings

### For Production Use
1. **Start Conservative**: chunk_size=30, batch_size=1
2. **Monitor Performance**: Check logs for memory/timeout issues
3. **Adjust Gradually**: Increase only if stable
4. **Plan for Failures**: Always check output files for errors

## Troubleshooting

### If Processing Still Fails
1. **Reduce chunk_size** to 20-30 pages
2. **Set batch_size** to 1
3. **Check GPU memory** before starting
4. **Process in smaller increments** (max_pages=50)

### If Engine Keeps Restarting
1. **Lower GPU memory utilization** in config
2. **Reduce max_tokens** to 512
3. **Increase delay** between chunks
4. **Check system resources** (RAM, disk space)

### If Output Quality is Poor
1. **Increase timeout** per page
2. **Use smaller batches** (batch_size=1)
3. **Enable cropping** for high-resolution PDFs
4. **Check input document quality**

## Future Improvements

### Planned Features
- **Resume capability**: Continue from last processed page
- **Progress saving**: Save intermediate results automatically
- **Quality validation**: Auto-detect and retry poor results
- **Parallel chunks**: Process multiple chunks on multi-GPU systems

### Configuration Options
- **Memory thresholds**: Configurable memory pressure limits
- **Timeout settings**: Per-document timeout configuration
- **Quality metrics**: Automatic output quality assessment
- **Resource monitoring**: Real-time resource usage display

This chunking system provides a robust solution for processing large PDFs while maintaining stability and providing good error recovery capabilities.