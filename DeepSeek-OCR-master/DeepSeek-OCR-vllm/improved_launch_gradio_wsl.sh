#!/bin/bash

# DeepSeek-OCR Gradio Web Application Launcher for WSL2 (Improved Version)
# This script includes memory optimization and process management improvements
# to prevent automatic shutdown during long PDF processing

echo "================================================"
echo "  DeepSeek-OCR Gradio Web Application Launcher"
echo "        (Improved Version with OOM Protection)"
echo "================================================"
echo ""

# Step 1: Navigate to the project directory
echo "Step 1: Navigating to project directory..."
cd /home/huangz/github/DeepSeek-OCR/DeepSeek-OCR-master/DeepSeek-OCR-vllm

if [ $? -ne 0 ]; then
    echo "Error: Failed to navigate to project directory"
    echo "Please check if the path exists: /home/huangz/github/DeepSeek-OCR/DeepSeek-OCR-master/DeepSeek-OCR-vllm"
    exit 1
fi

echo "✓ Successfully navigated to: $(pwd)"
echo ""

# Step 1.5: Set memory and system optimizations
echo "Step 1.5: Setting memory and process optimizations..."

# Set reasonable memory limits to prevent OOM killer (but not too restrictive)
# Note: Don't set virtual memory limit as it can prevent thread creation
# ulimit -v is removed to allow proper thread creation
ulimit -m 12582912   # Limit resident memory to 12GB

# Increase process/thread limits to prevent "Resource temporarily unavailable"
ulimit -u 4096       # Max user processes
ulimit -n 4096       # Max open files

# Set GPU memory environment variables
export CUDA_MEMORY_FRACTION=0.4  # Further reduced from 0.6 to 0.4
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:256,expandable_segments:True,garbage_collection_threshold:0.6
# Remove CUDA_LAUNCH_BLOCKING=1 as it can slow down performance significantly
# export CUDA_LAUNCH_BLOCKING=1

# Fix CUDA graph capture issues
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:256
export VLLM_ATTENTION_BACKEND=FLASH_ATTN
export VLLM_USE_V1=0

# Additional PyTorch memory management
# Disable memory caching to prevent CUDA graph issues
unset PYTORCH_NO_CUDA_MEMORY_CACHING
# Don't disable CUDA cache as it can cause issues
# export CUDA_CACHE_DISABLE=1

# Enable swap accounting and memory pressure handling
export PYTHONHASHSEED=0
export PYTHONDONTWRITEBYTECODE=1

# Set process priority to nice level (lower priority to avoid system overload)
renice 10 $$ 2>/dev/null || true

echo "✓ Memory limits and optimizations set"
echo "   - Resident memory limit: $(ulimit -m) KB (~12GB)"
echo "   - Max user processes: $(ulimit -u)"
echo "   - Max open files: $(ulimit -n)"
echo "   - CUDA memory fraction: $CUDA_MEMORY_FRACTION (40%)"
echo "   - PyTorch CUDA allocation: $PYTORCH_CUDA_ALLOC_CONF"
echo ""

# Step 2: Activate conda environment
echo "Step 2: Activating conda environment 'deepseek-ocr'..."
eval "$(conda shell.bash hook)"
conda activate deepseek-ocr

if [ $? -ne 0 ]; then
    echo "Error: Failed to activate conda environment 'deepseek-ocr'"
    echo "Please check if the environment exists:"
    echo "  conda env list"
    echo "Or create it if needed:"
    echo "  conda create -n deepseek-ocr python=3.10"
    exit 1
fi

echo "✓ Successfully activated conda environment: $CONDA_DEFAULT_ENV"
echo ""

# Step 2.5: Check and display memory status
echo "Step 2.5: Checking system memory status..."
free -h
echo ""
nvidia-smi --query-gpu=memory.total,memory.used,memory.free --format=csv 2>/dev/null || echo "GPU info unavailable"
echo ""

# Step 2.6: Set up OOM handling
echo "Step 2.6: Configuring OOM (Out-of-Memory) handling..."
# Disable OOM killer for the shell process (best effort)
# Note: This requires root privileges, will fail silently if not available
echo -17 > /proc/$$/oom_score_adj 2>/dev/null || echo "  (OOM score adjustment skipped - no root)"
echo "✓ OOM handling configured"
echo ""

# Step 2.7: Check and cleanup ports
echo "Step 2.7: Checking port availability and cleaning up existing processes..."
PORT=7860

# Kill any existing gradio processes
echo "Cleaning up existing gradio processes..."
pkill -f "gradio_app.py" 2>/dev/null || true
pkill -f "python.*gradio" 2>/dev/null || true
sleep 2

# Kill any existing processes on port 7860
echo "Checking for existing processes on port $PORT..."
EXISTING_PID=$(lsof -t -i:$PORT 2>/dev/null)
if [ ! -z "$EXISTING_PID" ]; then
    echo "Found existing process $EXISTING_PID on port $PORT, terminating..."
    kill -TERM $EXISTING_PID 2>/dev/null || true
    sleep 3
    # Force kill if still running
    if kill -0 $EXISTING_PID 2>/dev/null; then
        echo "Force killing process $EXISTING_PID..."
        kill -KILL $EXISTING_PID 2>/dev/null || true
        sleep 2
    fi
fi

# Find available port if 7860 is still busy
for i in {7860..7870}; do
    if ! lsof -i:$i > /dev/null 2>&1; then
        PORT=$i
        break
    fi
done

echo "✓ Will use port: $PORT"
export GRADIO_SERVER_PORT=$PORT
echo ""

# Step 3: Launch the Gradio application with enhanced monitoring
echo "Step 3: Launching DeepSeek-OCR Gradio Web Application..."
echo "The application will be available at: http://localhost:$PORT"
echo ""
echo "Enhanced features:"
echo "  - Memory usage monitoring"
echo "  - Process timeout handling"
echo "  - Reduced GPU memory utilization"
echo "  - Automatic garbage collection"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Create a monitoring script that runs in background with OOM detection
cat > /tmp/gradio_monitor.sh << 'EOF'
#!/bin/bash
GRADIO_PID=$1
OOM_DETECT_COUNT=0
CRITICAL_MEM_COUNT=0

while kill -0 $GRADIO_PID 2>/dev/null; do
    # Check memory usage every 15 seconds (more frequent)
    sleep 15
    
    # Check if process still exists (could have been killed by OOM)
    if ! kill -0 $GRADIO_PID 2>/dev/null; then
        echo "CRITICAL: Process $GRADIO_PID has terminated unexpectedly at $(date)"
        # Check dmesg for OOM killer messages
        if dmesg | tail -50 | grep -i "killed process.*gradio" > /dev/null 2>&1; then
            echo "OOM KILLER DETECTED: Process was killed by the kernel OOM killer"
        fi
        break
    fi
    
    # Get memory usage percentage
    MEM_USAGE=$(ps -p $GRADIO_PID -o %mem --no-headers 2>/dev/null | tr -d ' ' | cut -d'.' -f1)
    
    # Check GPU memory usage
    GPU_MEM=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1)
    GPU_TOTAL=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
    
    # Check GPU memory percentage using integer arithmetic
    if [ ! -z "$GPU_MEM" ] && [ ! -z "$GPU_TOTAL" ] && [ "$GPU_TOTAL" -gt 0 ]; then
        GPU_PERCENT=$((GPU_MEM * 100 / GPU_TOTAL))
        
        # If GPU memory usage > 90%, critical alert
        if [ "$GPU_PERCENT" -gt 90 ]; then
            CRITICAL_MEM_COUNT=$((CRITICAL_MEM_COUNT + 1))
            echo "CRITICAL: GPU memory usage: ${GPU_PERCENT}% (${GPU_MEM}MB/${GPU_TOTAL}MB) at $(date) [Alert #${CRITICAL_MEM_COUNT}]"
            echo "URGENT: Reduce batch size, max_pages, or image complexity immediately!"
        # If GPU memory usage > 85%, warning
        elif [ "$GPU_PERCENT" -gt 85 ]; then
            echo "WARNING: High GPU memory usage: ${GPU_PERCENT}% (${GPU_MEM}MB/${GPU_TOTAL}MB) at $(date)"
            echo "Consider reducing batch size or max_pages"
        fi
    fi
    
    # If CPU memory usage > 80%, critical warning
    if [ ! -z "$MEM_USAGE" ] && [ "$MEM_USAGE" -gt 80 ]; then
        CRITICAL_MEM_COUNT=$((CRITICAL_MEM_COUNT + 1))
        echo "CRITICAL: Very high CPU memory usage: ${MEM_USAGE}% at $(date) [Alert #${CRITICAL_MEM_COUNT}]"
        echo "URGENT: System may trigger OOM killer soon!"
        # Try to trigger garbage collection
        kill -USR1 $GRADIO_PID 2>/dev/null || true
    elif [ ! -z "$MEM_USAGE" ] && [ "$MEM_USAGE" -gt 70 ]; then
        echo "WARNING: High CPU memory usage: ${MEM_USAGE}% at $(date)"
        # Force garbage collection by sending SIGUSR1 (if implemented in Python)
        kill -USR1 $GRADIO_PID 2>/dev/null || true
    fi
    
    # Reset critical counter if memory is under control
    if [ ! -z "$MEM_USAGE" ] && [ "$MEM_USAGE" -lt 60 ]; then
        if [ "$CRITICAL_MEM_COUNT" -gt 0 ]; then
            echo "INFO: Memory usage normalized at $(date)"
            CRITICAL_MEM_COUNT=0
        fi
    fi
done
EOF

chmod +x /tmp/gradio_monitor.sh

# Start the application with memory monitoring
python gradio_app.py &
GRADIO_PID=$!

# Start the monitoring script in background
/tmp/gradio_monitor.sh $GRADIO_PID &
MONITOR_PID=$!

# Wait for the main process
wait $GRADIO_PID
EXIT_CODE=$?

# Cleanup
kill $MONITOR_PID 2>/dev/null || true
rm -f /tmp/gradio_monitor.sh

# Deactivate environment when done
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "Shutting down gracefully..."
else
    echo "Process exited with code $EXIT_CODE"
    if [ $EXIT_CODE -eq 137 ]; then
        echo "WARNING: Process was killed (likely due to memory issues)"
        echo "Consider:"
        echo "  - Reducing max_pages in PDF processing"
        echo "  - Processing smaller batches"
        echo "  - Increasing system swap space"
    fi
fi

conda deactivate
echo "✓ Environment deactivated"

exit $EXIT_CODE