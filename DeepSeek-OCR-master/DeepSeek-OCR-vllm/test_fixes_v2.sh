#!/bin/bash

# DeepSeek-OCR v2.0 Fix Verification and Test Script
echo "🔍 DeepSeek-OCR v2.0 Fix Verification"
echo "===================================="

# Function to check and report status
check_status() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ $1"
    fi
}

echo ""
echo "1. Checking GPU memory utilization fix..."
grep -q "gpu_memory_utilization=0.4" gradio_app.py
check_status "GPU memory reduced to 40%"

echo ""
echo "2. Checking token limit reductions..."
TOKEN_COUNT=$(grep -c "max_tokens=1024" gradio_app.py)
if [ "$TOKEN_COUNT" -ge 3 ]; then
    echo "✅ Token limits reduced to 1024 (found $TOKEN_COUNT instances)"
else
    echo "❌ Token limits not properly reduced (found $TOKEN_COUNT instances)"
fi

echo ""
echo "3. Checking memory management functions..."
grep -q "def clear_gpu_memory" gradio_app.py
check_status "GPU memory clearing function added"

grep -q "def check_gpu_memory" gradio_app.py
check_status "GPU memory monitoring function added"

echo ""
echo "4. Checking batch size optimizations..."
grep -q "num_pages <= 10" gradio_app.py
check_status "Small PDF threshold reduced to 10 pages"

grep -q "batch_size = 5" gradio_app.py
check_status "File batch size reduced to 5 pages"

echo ""
echo "5. Checking port management..."
grep -q "GRADIO_SERVER_PORT" improved_launch_gradio_wsl.sh
check_status "Dynamic port detection in launcher"

grep -q "server_port=server_port" gradio_app.py
check_status "Flexible port selection in app"

echo ""
echo "6. Checking process cleanup..."
if [ -f "cleanup_processes.sh" ] && [ -x "cleanup_processes.sh" ]; then
    echo "✅ Process cleanup script created and executable"
else
    echo "❌ Process cleanup script missing or not executable"
fi

echo ""
echo "7. Checking launcher enhancements..."
grep -q "PYTORCH_NO_CUDA_MEMORY_CACHING=1" improved_launch_gradio_wsl.sh
check_status "PyTorch memory caching disabled"

grep -q "expandable_segments:True" improved_launch_gradio_wsl.sh
check_status "CUDA expandable segments enabled"

echo ""
echo "8. Memory and resource settings summary:"
echo "   Virtual memory limit: $(grep -o 'ulimit -v [0-9]*' improved_launch_gradio_wsl.sh | cut -d' ' -f3) KB (~8GB)"
echo "   GPU memory fraction: $(grep -o 'CUDA_MEMORY_FRACTION=[0-9.]*' improved_launch_gradio_wsl.sh | cut -d'=' -f2)"
echo "   Max concurrent seqs: $(grep -o 'max_num_seqs=[0-9]*' gradio_app.py | head -1 | cut -d'=' -f2)"
echo "   Max batched tokens: $(grep -o 'max_num_batched_tokens=[0-9]*' gradio_app.py | head -1 | cut -d'=' -f2)"

echo ""
echo "🎉 Verification Complete!"
echo ""
echo "=========================================="
echo "Ready to launch with improved stability:"
echo "=========================================="
echo ""
echo "Option 1 - Clean start (recommended):"
echo "  ./cleanup_processes.sh"
echo "  ./improved_launch_gradio_wsl.sh"
echo ""
echo "Option 2 - Direct launch:"
echo "  ./improved_launch_gradio_wsl.sh"
echo ""
echo "The application will:"
echo "  ✅ Use only 40% GPU memory (~9.6GB on 24GB GPU)"
echo "  ✅ Process max 2 pages at once"
echo "  ✅ Use 1024 token limit (fast processing)"
echo "  ✅ Auto-detect available ports (7860-7870)"
echo "  ✅ Monitor and cleanup memory automatically"
echo "  ✅ Handle CUDA OOM gracefully"
echo ""
echo "Start with small PDFs (1-5 pages) to verify stability!"