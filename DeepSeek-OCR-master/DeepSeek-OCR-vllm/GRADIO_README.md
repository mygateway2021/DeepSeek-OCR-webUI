# DeepSeek-OCR Gradio Web Application

A user-friendly web interface for DeepSeek-OCR that allows you to perform OCR on images and PDFs through your browser.

## Features

- **Image OCR**: Upload images and extract text with optional bounding box visualization
- **PDF OCR**: Process multi-page PDF documents
- **Multiple Prompt Templates**: Choose from predefined prompts or create custom ones
- **Configurable Settings**: Enable/disable image cropping for optimal results
- **Real-time Processing**: See results as they're generated
- **Clean Interface**: Modern, intuitive UI built with Gradio

## Installation

### 1. Install Core Dependencies

Make sure you have already installed the base DeepSeek-OCR requirements. If not:

```bash
pip install -r requirements.txt
```

### 2. Install Gradio Dependencies

```bash
pip install -r requirements_gradio.txt
```

Or install packages individually:

```bash
pip install gradio>=4.0.0
pip install PyMuPDF>=1.23.0
pip install img2pdf>=0.5.0
```

## Configuration

Before running the app, make sure to configure the model path in `config.py`:

```python
MODEL_PATH = 'deepseek-ai/DeepSeek-OCR'  # or your local model path
INPUT_PATH = ''  # Not required for Gradio app
OUTPUT_PATH = ''  # Not required for Gradio app
```

You can also adjust these settings in `config.py`:
- `BASE_SIZE`: Base resolution for image processing (default: 1024)
- `IMAGE_SIZE`: Crop resolution (default: 640)
- `CROP_MODE`: Enable/disable automatic image cropping (default: True)
- `MIN_CROPS`: Minimum number of crops (default: 2)
- `MAX_CROPS`: Maximum number of crops (default: 6)

## Usage

### Starting the Web Application

```bash
python gradio_app.py
```

The application will start on `http://localhost:7860` by default.

### Using the Interface

#### Image OCR Tab

1. **Upload an Image**: Click or drag an image to the upload area
2. **Select a Prompt**: Choose from predefined templates or create a custom prompt
3. **Configure Settings**:
   - Enable/disable image cropping for better results on high-res images
   - Toggle bounding box visualization
4. **Click "Process Image"**: Wait for the model to process
5. **View Results**:
   - Extracted text appears in the text box
   - Bounding boxes (if enabled) show detected elements
   - Raw output with detection tags is available in the accordion

#### PDF OCR Tab

1. **Upload a PDF**: Select a PDF file from your computer
2. **Select a Prompt**: Choose the appropriate template for your content
3. **Configure Settings**:
   - Enable/disable image cropping
   - Set maximum pages to process (0 = all pages)
4. **Click "Process PDF"**: The app will process each page
5. **View Results**: All pages will be combined in the output text box

### Available Prompt Templates

1. **Document to Markdown**: Best for documents, papers, and text-heavy content
   ```
   <image>
   <|grounding|>Convert the document to markdown.
   ```

2. **OCR with Grounding**: Extracts text with layout information
   ```
   <image>
   <|grounding|>OCR this image.
   ```

3. **Free OCR**: Simple text extraction without layout detection
   ```
   <image>
   Free OCR.
   ```

4. **Parse Figure**: Optimized for charts, diagrams, and figures
   ```
   <image>
   Parse the figure.
   ```

5. **Describe Image**: General image description
   ```
   <image>
   Describe this image in detail.
   ```

### Custom Prompts

You can modify the prompt in the text box to create custom queries. Make sure to include the `<image>` token if you're processing images.

## Advanced Configuration

### Server Settings

You can modify the launch parameters in `gradio_app.py`:

```python
app.launch(
    server_name="0.0.0.0",  # Allow external access
    server_port=7860,        # Port number
    share=False,             # Set to True to create public link
    show_error=True          # Show detailed errors
)
```

### GPU Settings

The application uses the GPU specified in your environment:

```bash
# Use specific GPU
export CUDA_VISIBLE_DEVICES=0

# Then run the app
python gradio_app.py
```

### Memory Optimization

If you have limited GPU memory, adjust these settings in the code:

```python
engine_args = AsyncEngineArgs(
    # ... other args ...
    gpu_memory_utilization=0.75,  # Reduce if needed (0.5 - 0.9)
)
```

## Troubleshooting

### Out of Memory Errors

If you encounter OOM errors:
1. Reduce `MAX_CROPS` in `config.py` (e.g., set to 4 or 6)
2. Disable cropping for large images
3. Lower `gpu_memory_utilization` in the engine initialization
4. Process PDF pages in smaller batches

### Model Not Found

Ensure your model path is correct:
```python
MODEL_PATH = '/path/to/your/model'  # or 'deepseek-ai/DeepSeek-OCR'
```

### Slow Processing

For faster processing:
1. Enable `enforce_eager=False` (default)
2. Reduce `max_model_len` if you don't need long outputs
3. Use a GPU with more memory for larger batch sizes

### Connection Issues

If the web interface doesn't open:
1. Check if port 7860 is available
2. Try changing the port: `server_port=8080`
3. Check firewall settings

## Performance Tips

1. **Image Quality**: Higher resolution images may take longer but provide better results
2. **Cropping**: Enable cropping for images larger than 640x640 pixels
3. **Batch Processing**: For multiple images, use the PDF feature by converting images to PDF
4. **Prompt Selection**: Use specific prompts for better results (e.g., "Parse Figure" for diagrams)

## Features and Limitations

### Supported Formats

**Images:**
- JPEG/JPG
- PNG
- BMP
- TIFF
- WebP

**Documents:**
- PDF (multi-page support)

### Output Features

- Markdown formatting
- Bounding box detection
- Layout preservation
- Figure extraction
- Table recognition

## API Usage

The Gradio app also provides an API endpoint. You can use it programmatically:

```python
from gradio_client import Client

client = Client("http://localhost:7860")
result = client.predict(
    image,  # PIL Image or path
    "<image>\n<|grounding|>Convert the document to markdown.",  # prompt
    True,   # use_cropping
    True,   # show_bounding_boxes
    api_name="/predict"
)
```

## Contributing

To contribute improvements to the Gradio app:
1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This Gradio interface is part of the DeepSeek-OCR project. Please refer to the main project license.

## Support

For issues and questions:
- Check the main DeepSeek-OCR documentation
- Open an issue on GitHub
- Review the troubleshooting section above

## Acknowledgments

Built with:
- [Gradio](https://gradio.app/) - Web interface framework
- [vLLM](https://github.com/vllm-project/vllm) - Inference engine
- [DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR) - OCR model
