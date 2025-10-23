# DeepSeek-OCR WSL2 Launcher Script

This script automates the process of launching the DeepSeek-OCR Gradio web application in a WSL2 environment.

## What it does:

1. **Navigate to project directory**: Changes to `/home/huangz/github/DeepSeek-OCR/DeepSeek-OCR-master/DeepSeek-OCR-vllm`
2. **Activate conda environment**: Activates the `deepseek-ocr` conda environment
3. **Launch Gradio app**: Runs `python gradio_app.py` to start the web interface

## Usage:

```bash
# From WSL terminal
./launch_gradio_wsl.sh
```

## Prerequisites:

- WSL2 with Ubuntu installed
- Conda/miniconda installed
- `deepseek-ocr` conda environment created and configured
- DeepSeek-OCR project cloned to the expected path
- Gradio dependencies installed (`pip install -r requirements_gradio.txt`)

## Troubleshooting:

If the script fails:

1. **Environment not found**: Create the conda environment:
   ```bash
   conda create -n deepseek-ocr python=3.10
   conda activate deepseek-ocr
   pip install -r requirements.txt
   pip install -r requirements_gradio.txt
   ```

2. **Path not found**: Update the script if your project is in a different location

3. **Permission denied**: Make sure the script is executable:
   ```bash
   chmod +x launch_gradio_wsl.sh
   ```

## After running:

The Gradio web application will be available at: **http://localhost:7860**

Press `Ctrl+C` in the terminal to stop the server.