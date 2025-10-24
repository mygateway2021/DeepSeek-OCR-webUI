#!/bin/bash

# DeepSeek-OCR Quick Start Guide
echo "🚀 DeepSeek-OCR Quick Start Guide"
echo "================================="
echo ""

echo "Available launcher options:"
echo ""
echo "1. 🔧 FULL FEATURED (recommended for production)"
echo "   ./improved_launch_gradio_wsl.sh"
echo "   Features: Memory monitoring, port detection, process cleanup"
echo ""
echo "2. ⚡ SIMPLE (if tools missing)"
echo "   ./simple_launch.sh"
echo "   Features: Basic setup, minimal dependencies"
echo ""
echo "3. 🧹 CLEANUP FIRST (if having issues)"
echo "   ./cleanup_processes.sh"
echo "   Then run option 1 or 2"
echo ""

# Check which tools are available
echo "System compatibility check:"
echo ""

# Check for required tools
if command -v bc >/dev/null 2>&1; then
    echo "✅ bc (calculator) - available"
    BC_AVAILABLE=true
else
    echo "❌ bc (calculator) - missing"
    BC_AVAILABLE=false
fi

if command -v lsof >/dev/null 2>&1; then
    echo "✅ lsof (port scanner) - available"
    LSOF_AVAILABLE=true
else
    echo "❌ lsof (port scanner) - missing"
    LSOF_AVAILABLE=false
fi

if command -v nvidia-smi >/dev/null 2>&1; then
    echo "✅ nvidia-smi (GPU monitor) - available"
    GPU_AVAILABLE=true
else
    echo "❌ nvidia-smi (GPU monitor) - missing"
    GPU_AVAILABLE=false
fi

echo ""

# Provide recommendation
if [ "$BC_AVAILABLE" = true ] && [ "$LSOF_AVAILABLE" = true ]; then
    echo "🎯 RECOMMENDATION: Use ./improved_launch_gradio_wsl.sh"
    echo "   All monitoring tools are available"
else
    echo "🎯 RECOMMENDATION: Use ./simple_launch.sh"
    echo "   Some monitoring tools are missing, but basic functionality will work"
fi

echo ""
echo "Memory and GPU optimizations applied:"
echo "✅ GPU memory reduced to 40% (safe for 24GB cards)"
echo "✅ Token limits reduced to 1024 (prevents timeouts)"
echo "✅ Batch processing limited to 2 pages (prevents OOM)"
echo "✅ Automatic memory cleanup after each operation"
echo "✅ Flexible port selection (7860-7870)"
echo ""

echo "Quick test command:"
echo "  ./simple_launch.sh"
echo ""
echo "For maximum stability, start with small PDFs (1-3 pages)"