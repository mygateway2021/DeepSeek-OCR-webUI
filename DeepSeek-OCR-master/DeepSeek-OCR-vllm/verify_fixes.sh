#!/bin/bash

# Test script to verify the fixes are working
echo "🔍 DeepSeek-OCR Fix Verification Script"
echo "======================================="

# Check if gradio_app.py has the fixes
echo ""
echo "1. Checking GPU memory utilization fix..."
if grep -q "gpu_memory_utilization=0.6" gradio_app.py; then
    echo "✅ GPU memory utilization reduced to 0.6"
else
    echo "❌ GPU memory utilization fix not found"
fi

echo ""
echo "2. Checking max_tokens reductions..."
if ! grep -q "max_tokens=8192" gradio_app.py; then
    echo "✅ All max_tokens=8192 instances have been fixed"
else
    echo "❌ Some max_tokens=8192 instances still remain"
fi

echo ""
echo "3. Checking timeout handling..."
if grep -q "asyncio.wait_for" gradio_app.py; then
    echo "✅ Timeout handling has been added"
else
    echo "❌ Timeout handling not found"
fi

echo ""
echo "4. Checking memory cleanup..."
if grep -q "gc.collect()" gradio_app.py; then
    echo "✅ Garbage collection has been added"
else
    echo "❌ Garbage collection not found"
fi

echo ""
echo "5. Checking batch size optimization..."
if grep -q "Batch into 10 pages" gradio_app.py; then
    echo "✅ Batch size reduced from 25 to 10 pages"
else
    echo "❌ Batch size optimization not found"
fi

echo ""
echo "6. Checking improved launcher script..."
if [ -f "improved_launch_gradio_wsl.sh" ]; then
    echo "✅ Improved launcher script created"
    if grep -q "ulimit -v" improved_launch_gradio_wsl.sh; then
        echo "✅ Memory limits configured in launcher"
    else
        echo "❌ Memory limits not found in launcher"
    fi
else
    echo "❌ Improved launcher script not found"
fi

echo ""
echo "7. Summary of token limits:"
echo "   Single image processing:"
grep "max_tokens.*Further reduced" gradio_app.py | head -1
echo "   PDF processing:"
grep "max_tokens.*Reduced for.*PDF" gradio_app.py | head -2

echo ""
echo "🎉 Fix verification complete!"
echo ""
echo "Next steps:"
echo "1. Test with: ./improved_launch_gradio_wsl.sh"
echo "2. Process a small PDF first (5-10 pages)"
echo "3. Monitor memory usage during processing"
echo "4. Gradually increase PDF size if stable"