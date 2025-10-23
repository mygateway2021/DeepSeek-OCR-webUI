# 🌐 Gradio Web Interface Available!

A user-friendly web interface has been added to this project! You can now use DeepSeek-OCR through a modern web UI.

## 🚀 Quick Start

```bash
# Install Gradio dependencies
pip install -r requirements_gradio.txt

# Launch the web app (WSL2 - Recommended)
./launch_gradio_wsl.sh

# Or use the launcher
./launch_gradio.sh        # Linux/Mac
launch_gradio.bat         # Windows

# Or launch directly
python gradio_app.py
```

Then open your browser to: **http://localhost:7860**

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Full Documentation](GRADIO_README.md)** - Complete feature guide
- **[Summary](GRADIO_SUMMARY.md)** - Overview of all features

## ✨ Features

### Web Interface
- 🖼️ **Image OCR** - Upload images and extract text
- 📄 **PDF OCR** - Process multi-page PDFs
- 🎯 **Multiple Prompts** - Document, figure, free OCR, and more
- 📦 **Bounding Boxes** - Visual detection results
- ⚙️ **Configurable** - Adjust cropping and other settings

### Programmatic Usage
- 📝 **Python API** - Use as a library
- 🔄 **Batch Processing** - Process multiple files
- 🎨 **Custom Prompts** - Full control over OCR behavior

## 📸 Screenshots

### Image OCR Interface
```
┌─────────────────────────────────────────────────┐
│  Upload Image    →    Select Prompt    →  OCR   │
│  [📷 Drag/Drop]       [📋 Templates]    [▶ Run] │
│                                                  │
│  Result:                                         │
│  ✓ Bounding boxes visualization                 │
│  ✓ Extracted text (Markdown)                    │
│  ✓ Raw output with detection tags               │
└─────────────────────────────────────────────────┘
```

### PDF OCR Interface
```
┌─────────────────────────────────────────────────┐
│  Upload PDF      →    Configure    →  Process   │
│  [📎 Select]          [⚙️ Settings]    [▶ Run]  │
│                                                  │
│  Output: Combined text from all pages            │
│  Page 1 | Page 2 | Page 3 | ...                 │
└─────────────────────────────────────────────────┘
```

## 💡 Example Usage

### Web Interface (No Code!)
1. Open http://localhost:7860
2. Upload an image or PDF
3. Click "Process"
4. View results!

### Command Line
```bash
# Single image
python example_usage.py document.jpg

# Multiple images
python example_usage.py page1.jpg page2.jpg page3.jpg

# Test all prompts
python example_usage.py --prompts figure.png
```

### Python Code
```python
import asyncio
from gradio_app import simple_ocr_example

# OCR a document
result = asyncio.run(simple_ocr_example("document.jpg"))
print(result)
```

## 🎯 Use Cases

| Task | Prompt Template | Best For |
|------|----------------|----------|
| Document → Markdown | `<image>\n<\|grounding\|>Convert the document to markdown.` | Papers, articles, books |
| Simple Text Extraction | `<image>\nFree OCR.` | Screenshots, simple images |
| Figure Analysis | `<image>\nParse the figure.` | Charts, diagrams, graphs |
| Table Extraction | `<image>\n<\|grounding\|>Convert the document to markdown.` | Tables, forms |
| Image Description | `<image>\nDescribe this image in detail.` | General images |

## 🔧 Configuration

Edit `config.py` to customize:
```python
MODEL_PATH = 'deepseek-ai/DeepSeek-OCR'  # Your model path
BASE_SIZE = 1024                          # Base resolution
IMAGE_SIZE = 640                          # Crop resolution  
CROP_MODE = True                          # Enable cropping
MAX_CROPS = 6                             # Max tiles (2-9)
```

## 📦 Files Created

```
├── gradio_app.py              ⭐ Main web application
├── example_usage.py           📝 Programmatic examples
├── requirements_gradio.txt    📦 Dependencies
├── launch_gradio.sh          🐧 Linux/Mac launcher
├── launch_gradio.bat         🪟 Windows launcher
├── GRADIO_README.md          📖 Full documentation
├── QUICKSTART.md             🚀 5-minute guide
└── GRADIO_SUMMARY.md         📋 Feature summary
```

## 🎓 Learn More

- Read the **[Quick Start Guide](QUICKSTART.md)** for basic usage
- Check **[Full Documentation](GRADIO_README.md)** for advanced features
- See **[Examples](example_usage.py)** for programmatic usage
- Review **[Summary](GRADIO_SUMMARY.md)** for complete overview

## 🆘 Need Help?

**Common Issues:**

| Problem | Solution |
|---------|----------|
| Out of memory | Reduce `MAX_CROPS` in config.py to 4 |
| Model not found | Check `MODEL_PATH` in config.py |
| Slow processing | First run is slower, enable GPU |
| Port 7860 in use | Change `server_port` in gradio_app.py |

**Full troubleshooting**: See [GRADIO_README.md](GRADIO_README.md#troubleshooting)

## ⚡ Performance

- **First run**: ~30s (model loading)
- **Single image**: 2-10s depending on size
- **PDF page**: 3-15s per page
- **Optimal**: Images < 2000x2000 pixels

**Tips:**
- Enable cropping for images > 640x640
- Process similar images together
- Use a GPU for best performance

## 🌟 Features Summary

✅ **Easy to Use** - No coding required!  
✅ **Powerful** - Full DeepSeek-OCR capabilities  
✅ **Flexible** - Web UI + Python API  
✅ **Fast** - Optimized with vLLM  
✅ **Visual** - Bounding box display  
✅ **Versatile** - Images and PDFs  

## 🚀 Get Started Now!

```bash
# Install and run in 3 commands:
pip install -r requirements_gradio.txt
./launch_gradio_wsl.sh
# Open http://localhost:7860
```

---

**Happy OCR-ing!** 🎉

For the original CLI tools, see the main documentation.
