@echo off
REM DeepSeek-OCR Gradio Web Application Launcher for Windows
REM This script helps you launch the Gradio web interface for DeepSeek-OCR

echo ================================================
echo   DeepSeek-OCR Gradio Web Application Launcher
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import gradio" 2>nul
if errorlevel 1 (
    echo Warning: Gradio is not installed.
    echo Installing Gradio dependencies...
    pip install -r requirements_gradio.txt
)

REM Set default GPU if not specified
if not defined CUDA_VISIBLE_DEVICES (
    set CUDA_VISIBLE_DEVICES=0
    echo Using GPU: 0 (set CUDA_VISIBLE_DEVICES to change^)
) else (
    echo Using GPU: %CUDA_VISIBLE_DEVICES%
)

REM Launch the application
echo.
echo Starting DeepSeek-OCR Web Application...
echo The application will be available at: http://localhost:7860
echo.
echo Press Ctrl+C to stop the server
echo.

python gradio_app.py

pause
