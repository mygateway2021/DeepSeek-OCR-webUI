#!/bin/bash

# DeepSeek-OCR Gradio Web Application Launcher
# This script helps you launch the Gradio web interface for DeepSeek-OCR

echo "================================================"
echo "  DeepSeek-OCR Gradio Web Application Launcher"
echo "================================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python -c "import gradio" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: Gradio is not installed."
    echo "Installing Gradio dependencies..."
    pip install -r requirements_gradio.txt
fi

# Set default GPU if not specified
if [ -z "$CUDA_VISIBLE_DEVICES" ]; then
    export CUDA_VISIBLE_DEVICES=0
    echo "Using GPU: 0 (set CUDA_VISIBLE_DEVICES to change)"
else
    echo "Using GPU: $CUDA_VISIBLE_DEVICES"
fi

# Launch the application
echo ""
echo "Starting DeepSeek-OCR Web Application..."
echo "The application will be available at: http://localhost:7860"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python gradio_app.py
