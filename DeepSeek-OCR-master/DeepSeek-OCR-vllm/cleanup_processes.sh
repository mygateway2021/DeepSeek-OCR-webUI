#!/bin/bash

# DeepSeek-OCR Process Cleanup Script
# Use this script to manually clean up any stuck processes

echo "🧹 DeepSeek-OCR Process Cleanup"
echo "=============================="

# Function to kill processes gracefully
cleanup_processes() {
    local pattern="$1"
    local description="$2"
    
    echo "Searching for $description processes..."
    PIDS=$(pgrep -f "$pattern" 2>/dev/null)
    
    if [ ! -z "$PIDS" ]; then
        echo "Found $description processes: $PIDS"
        echo "Terminating gracefully..."
        pkill -TERM -f "$pattern" 2>/dev/null || true
        sleep 3
        
        # Check if any are still running
        REMAINING=$(pgrep -f "$pattern" 2>/dev/null)
        if [ ! -z "$REMAINING" ]; then
            echo "Force killing remaining processes: $REMAINING"
            pkill -KILL -f "$pattern" 2>/dev/null || true
            sleep 1
        fi
        echo "✓ $description processes cleaned up"
    else
        echo "✓ No $description processes found"
    fi
}

# Clean up various process patterns
cleanup_processes "gradio_app.py" "gradio_app.py"
cleanup_processes "python.*gradio" "Python gradio"
cleanup_processes "deepseek.*ocr" "DeepSeek OCR"
cleanup_processes "vllm" "vLLM engine"

echo ""
echo "Checking port usage..."

# Check and free up ports 7860-7870
for port in {7860..7870}; do
    PID=$(lsof -t -i:$port 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo "Port $port is used by process $PID"
        
        # Get process name
        PROCESS_NAME=$(ps -p $PID -o comm= 2>/dev/null || echo "unknown")
        echo "Process name: $PROCESS_NAME"
        
        # Ask user if they want to kill it
        read -p "Kill process $PID on port $port? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Killing process $PID..."
            kill -TERM $PID 2>/dev/null || true
            sleep 2
            if kill -0 $PID 2>/dev/null; then
                kill -KILL $PID 2>/dev/null || true
            fi
            echo "✓ Process killed"
        fi
    fi
done

echo ""
echo "Clearing GPU memory..."
if command -v nvidia-smi >/dev/null 2>&1; then
    # Reset GPU if possible
    nvidia-smi --gpu-reset 2>/dev/null || echo "GPU reset not available (normal for non-admin users)"
else
    echo "nvidia-smi not available"
fi

echo ""
echo "Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

echo ""
echo "Memory status after cleanup:"
free -h

echo ""
echo "🎉 Cleanup complete!"
echo ""
echo "You can now run:"
echo "  ./improved_launch_gradio_wsl.sh"
echo ""
echo "Or check what's still running:"
echo "  ps aux | grep -E '(gradio|python|deepseek)'"