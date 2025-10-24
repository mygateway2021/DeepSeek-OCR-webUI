#!/bin/bash

# Simple DeepSeek-OCR Launcher (No external dependencies)
# This version avoids bc, lsof, and other tools that might not be available

echo "================================================"
echo "  DeepSeek-OCR Simple Launcher (v2.0)"
echo "================================================"
echo ""

# Navigate to project directory
cd /home/huangz/github/DeepSeek-OCR/DeepSeek-OCR-master/DeepSeek-OCR-vllm

# Set memory optimizations
export CUDA_MEMORY_FRACTION=0.4
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:256,expandable_segments:True
export PYTORCH_NO_CUDA_MEMORY_CACHING=1
export GRADIO_SERVER_PORT=7860

echo "✓ Memory optimizations set"
echo "   - CUDA memory fraction: $CUDA_MEMORY_FRACTION"
echo "   - Server port: $GRADIO_SERVER_PORT"
echo ""

# Activate conda environment
echo "Activating conda environment..."
eval "$(conda shell.bash hook)"
conda activate deepseek-ocr

if [ $? -ne 0 ]; then
    echo "Error: Failed to activate conda environment 'deepseek-ocr'"
    exit 1
fi

echo "✓ Environment activated: $CONDA_DEFAULT_ENV"
echo ""

# Simple process cleanup
echo "Cleaning up existing processes..."
pkill -f "gradio_app.py" 2>/dev/null || true
pkill -f "python.*gradio" 2>/dev/null || true
sleep 2

echo "✓ Process cleanup complete"
echo ""

# Show system status
echo "System status:"
free -h 2>/dev/null || echo "Memory info unavailable"
nvidia-smi --query-gpu=memory.total,memory.used --format=csv 2>/dev/null || echo "GPU info unavailable"
echo ""

# Launch application
echo "Launching DeepSeek-OCR..."
echo "Application will be available at: http://localhost:$GRADIO_SERVER_PORT"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Simple monitoring in background
{
    sleep 60  # Wait for app to start
    while true; do
        sleep 30
        if pgrep -f "gradio_app.py" > /dev/null; then
            MEM_KB=$(ps -o rss= -p $(pgrep -f "gradio_app.py" | head -1) 2>/dev/null || echo "0")
            if [ "$MEM_KB" -gt 8000000 ]; then  # > 8GB
                echo "WARNING: High memory usage detected at $(date)"
            fi
        else
            break
        fi
    done
} &

MONITOR_PID=$!

# Start the main application
python gradio_app.py
EXIT_CODE=$?

# Cleanup
kill $MONITOR_PID 2>/dev/null || true
conda deactivate

echo ""
echo "Application stopped with exit code: $EXIT_CODE"

exit $EXIT_CODE