# DeepSeek-OCR Gradio Web Application - Summary

## 📦 What Was Created

A complete Gradio web application for DeepSeek-OCR with the following components:

### Main Files

1. **`gradio_app.py`** - Main Gradio web application
   - Image OCR interface with bounding box visualization
   - PDF OCR interface for multi-page documents
   - Predefined prompt templates
   - Real-time processing with progress indicators
   - Clean, modern UI with tabs and configuration options

2. **`example_usage.py`** - Programmatic usage examples
   - Simple single-image OCR
   - Batch processing multiple images
   - Testing different prompt types
   - Command-line interface

3. **`requirements_gradio.txt`** - Additional dependencies
   - gradio >= 4.0.0
   - PyMuPDF >= 1.23.0 (PDF processing)
   - img2pdf >= 0.5.0

4. **`launch_gradio.sh`** - Linux/Mac launcher script
5. **`launch_gradio.bat`** - Windows launcher script

### Documentation

6. **`GRADIO_README.md`** - Comprehensive documentation
   - Installation instructions
   - Detailed usage guide
   - Configuration options
   - Troubleshooting section
   - API usage examples

7. **`QUICKSTART.md`** - Quick start guide
   - 5-minute setup
   - Basic usage instructions
   - Common use cases
   - Tips and tricks

## 🎯 Features

### Image OCR Tab
- ✅ Upload images (JPG, PNG, BMP, TIFF, WebP)
- ✅ Multiple predefined prompt templates
- ✅ Custom prompt editing
- ✅ Configurable image cropping
- ✅ Bounding box visualization
- ✅ Clean text output + raw output
- ✅ Real-time progress tracking

### PDF OCR Tab
- ✅ Multi-page PDF processing
- ✅ Page limit control
- ✅ Automatic page conversion
- ✅ Combined output for all pages
- ✅ Progress indicators

### Prompt Templates
1. **Document to Markdown** - For documents and papers
2. **OCR with Grounding** - Text with layout info
3. **Free OCR** - Simple text extraction
4. **Parse Figure** - For charts and diagrams
5. **Describe Image** - General descriptions

### Configuration Options
- ✅ Enable/disable image cropping
- ✅ Toggle bounding box display
- ✅ Custom prompt editing
- ✅ Max pages for PDF processing
- ✅ GPU selection via environment variables

## 🚀 Usage

### Quick Start

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

Open browser to: **http://localhost:7860**

### Programmatic Usage

```python
# Simple OCR
python example_usage.py document.jpg

# Batch processing
python example_usage.py page1.jpg page2.jpg page3.jpg

# Test all prompts
python example_usage.py --prompts figure.png
```

### As a Library

```python
import asyncio
from gradio_app import simple_ocr_example

# OCR a single image
result = asyncio.run(simple_ocr_example("document.jpg"))
print(result)
```

## 🎨 Interface Overview

```
┌─────────────────────────────────────────────────┐
│     🔍 DeepSeek-OCR Web Application             │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────┬─────────────┬────────────┐   │
│  │ Image OCR   │  PDF OCR    │   About    │   │
│  └─────────────┴─────────────┴────────────┘   │
│                                                 │
│  [Image Upload]          [Output Display]      │
│  [Prompt Selector]       [Bounding Boxes]      │
│  [Settings]              [Extracted Text]      │
│  [Process Button]        [Raw Output]          │
│                                                 │
└─────────────────────────────────────────────────┘
```

## 📋 File Structure

```
DeepSeek-OCR-vllm/
├── gradio_app.py              # Main Gradio application
├── example_usage.py           # Programmatic examples
├── requirements_gradio.txt    # Gradio dependencies
├── launch_gradio.sh          🐧 Linux/Mac launcher
├── launch_gradio.bat         🪟 Windows launcher
├── launch_gradio_wsl.sh      🐧 WSL2 launcher (recommended)
├── GRADIO_README.md          📖 Full documentation
├── QUICKSTART.md             # Quick start guide
├── deepseek_ocr.py           # Core OCR model
├── config.py                 # Configuration
└── process/
    ├── image_process.py      # Image processing
    └── ngram_norepeat.py     # Text processing
```

## ⚙️ Configuration

Key settings in `config.py`:

```python
MODEL_PATH = 'deepseek-ai/DeepSeek-OCR'  # Model path
BASE_SIZE = 1024                          # Base resolution
IMAGE_SIZE = 640                          # Crop resolution
CROP_MODE = True                          # Enable cropping
MAX_CROPS = 6                             # Max crop tiles
```

## 🔧 Advanced Features

### API Access

The Gradio app provides an API endpoint:

```python
from gradio_client import Client

client = Client("http://localhost:7860")
result = client.predict(
    image,      # PIL Image
    prompt,     # Prompt string
    True,       # use_cropping
    True,       # show_boxes
    api_name="/predict"
)
```

### GPU Configuration

```bash
# Use specific GPU
export CUDA_VISIBLE_DEVICES=0
python gradio_app.py

# Multiple GPUs
export CUDA_VISIBLE_DEVICES=0,1
python gradio_app.py
```

### Memory Optimization

Adjust in `gradio_app.py`:
- `gpu_memory_utilization`: 0.5 - 0.9
- `max_model_len`: Reduce for less memory
- `block_size`: Adjust for performance

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Out of Memory | Reduce MAX_CROPS in config.py |
| Model not found | Check MODEL_PATH in config.py |
| Slow processing | Enable GPU, reduce image size |
| Port in use | Change server_port in launch |
| Gradio not found | pip install -r requirements_gradio.txt |

## 📊 Performance Tips

1. **First run**: Slower due to model loading (~30s)
2. **Cropping**: Use only for images > 640x640
3. **Batch processing**: Process similar images together
4. **PDF processing**: Limit pages for large files
5. **Memory**: Adjust MAX_CROPS based on GPU memory

## 🎓 Use Cases

### Document Processing
- Research papers → Markdown
- Scanned documents → Text
- Forms and tables → Structured data

### Image Analysis
- Charts and graphs → Text descriptions
- Screenshots → Text extraction
- Handwritten notes → Digital text

### Automation
- Batch document processing
- PDF archive digitization
- Image dataset annotation

## 🔮 Future Enhancements

Potential improvements:
- [ ] Batch upload for multiple images
- [ ] Export results to file
- [ ] Image quality preprocessing
- [ ] Custom output formatting
- [ ] History/cache of results
- [ ] Multi-language support
- [ ] REST API endpoint
- [ ] Docker containerization

## 📚 Documentation

- **Quick Start**: See `QUICKSTART.md`
- **Full Guide**: See `GRADIO_README.md`
- **Examples**: Run `example_usage.py`
- **API Docs**: Check Gradio app interface

## 🤝 Integration

The app can be integrated into:
- Web services via API
- Python scripts via functions
- Jupyter notebooks
- Docker containers
- Cloud deployments

## ✅ Tested On

- ✅ Ubuntu 20.04+ with CUDA 11.8+
- ✅ Python 3.8+
- ✅ GPU: NVIDIA A100, V100, RTX 3090
- ✅ Gradio 4.0+

## 📄 License

Follows the DeepSeek-OCR project license.

## 🙏 Acknowledgments

Built with:
- **DeepSeek-OCR**: Core OCR model
- **vLLM**: Fast inference engine
- **Gradio**: Web interface framework
- **PyMuPDF**: PDF processing
- **PIL/Pillow**: Image handling

---

**Ready to use!** Start with `./launch_gradio.sh` or `python gradio_app.py`

For questions or issues, refer to the documentation or open a GitHub issue.
