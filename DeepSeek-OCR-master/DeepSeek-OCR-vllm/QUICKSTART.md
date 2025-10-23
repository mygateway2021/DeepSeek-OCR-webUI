# Quick Start Guide - DeepSeek-OCR Gradio Web App

## 5-Minute Setup

### Step 1: Install Dependencies (First Time Only)

```bash
# Install Gradio and PDF processing libraries
pip install gradio>=4.0.0 PyMuPDF>=1.23.0 img2pdf>=0.5.0
```

Or use the requirements file:
```bash
pip install -r requirements_gradio.txt
```

### Step 2: Configure Model Path

Edit `config.py` and set your model path:

```python
MODEL_PATH = 'deepseek-ai/DeepSeek-OCR'  # or your local path
```

### Step 3: Launch the App

**Option A: WSL2 Script (Recommended)**
```bash
# From WSL terminal
./launch_gradio_wsl.sh
```

**Option B: Manual Launch**
```bash
# From WSL terminal
cd /home/huangz/github/DeepSeek-OCR/DeepSeek-OCR-master/DeepSeek-OCR-vllm
conda activate deepseek-ocr
python gradio_app.py
```

**Option C: Windows Launchers**
```cmd
REM From Windows Command Prompt
launch_gradio.bat
```

**Option D: Direct Python**
```bash
python gradio_app.py
```

### Step 4: Open in Browser

Navigate to: **http://localhost:7860**

## Basic Usage

### For Images:
1. Go to "Image OCR" tab
2. Upload an image (drag & drop or click)
3. Select "Document to Markdown" prompt
4. Click "Process Image"
5. View results!

### For PDFs:
1. Go to "PDF OCR" tab
2. Upload a PDF file
3. Select prompt template
4. Set max pages (0 = all)
5. Click "Process PDF"
6. Wait for processing

## Common Use Cases

### Extract Text from Document
- **Prompt**: "Document to Markdown"
- **Cropping**: Enabled
- **Best for**: Papers, books, articles

### OCR a Screenshot
- **Prompt**: "Free OCR"
- **Cropping**: Disabled (if small)
- **Best for**: Screenshots, simple images

### Parse Charts/Diagrams
- **Prompt**: "Parse Figure"
- **Cropping**: Enabled
- **Best for**: Graphs, flowcharts, diagrams

### Extract Table Data
- **Prompt**: "Document to Markdown"
- **Cropping**: Enabled
- **Best for**: Tables, forms

## Tips

✅ **DO:**
- Enable cropping for images > 640x640 pixels
- Use "Document to Markdown" for structured documents
- Process PDFs in smaller batches if low on memory

❌ **DON'T:**
- Process extremely large PDFs all at once
- Use cropping on small images (<640x640)
- Forget to set the correct MODEL_PATH

## Troubleshooting

**App won't start?**
```bash
# Check if port is in use
python gradio_app.py  # Try running directly
```

**Out of memory?**
- Reduce MAX_CROPS in config.py to 4
- Disable cropping
- Process fewer PDF pages at once

**Model not found?**
- Check MODEL_PATH in config.py
- Ensure model is downloaded

**Slow processing?**
- First run is slower (model loading)
- Enable cropping only for large images
- Use a stronger GPU

## Example Outputs

### Input: Document Image
```
[Image: Research paper page]
```

### Output: Markdown
```markdown
# Introduction

This paper presents a novel approach to...

## Related Work

Previous studies have shown...
```

## Need Help?

- 📖 Read the full [GRADIO_README.md](GRADIO_README.md)
- 🐛 Check the troubleshooting section
- 💬 Open an issue on GitHub

## Next Steps

Once comfortable with the basics:
1. Experiment with custom prompts
2. Adjust cropping settings for your use case
3. Try batch processing multiple files
4. Explore the API for automation

Happy OCR-ing! 🎉
