#!/bin/bash

# DeepSeek-OCR Gradio Web Application Launcher for WSL2
# This script navigates to the project directory, activates the conda environment,
# and launches the Gradio web application

echo "================================================"
echo "  DeepSeek-OCR Gradio Web Application Launcher"
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

# Step 3: Launch the Gradio application
echo "Step 3: Launching DeepSeek-OCR Gradio Web Application..."
echo "The application will be available at: http://localhost:7860"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python gradio_app.py

# Deactivate environment when done
echo ""
echo "Shutting down..."
conda deactivate
echo "✓ Environment deactivated"