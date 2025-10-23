import os
import re
import io
import asyncio
import zipfile
from typing import Optional, List, Tuple, Iterator
from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np
import gradio as gr
import torch
import fitz  # PyMuPDF

if torch.version.cuda == '11.8':
    os.environ["TRITON_PTXAS_PATH"] = "/usr/local/cuda-11.8/bin/ptxas"

os.environ['VLLM_USE_V1'] = '0'
# Set default GPU
os.environ["CUDA_VISIBLE_DEVICES"] = os.environ.get("CUDA_VISIBLE_DEVICES", '0')

from vllm import AsyncLLMEngine, SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.model_executor.models.registry import ModelRegistry
from deepseek_ocr import DeepseekOCRForCausalLM
from process.ngram_norepeat import NoRepeatNGramLogitsProcessor
from process.image_process import DeepseekOCRProcessor
from config import MODEL_PATH, IMAGE_SIZE, BASE_SIZE, CROP_MODE

# Register the model
ModelRegistry.register_model("DeepseekOCRForCausalLM", DeepseekOCRForCausalLM)

# Global variable to store the engine
engine = None

# Global cancellation flag for PDF processing
pdf_processing_cancelled = False

# Language translations
TRANSLATIONS = {
    "en": {
        "title": "🔍 DeepSeek-OCR vLLM Web Application",
        "subtitle": "Upload images or PDFs to extract text and document structure using DeepSeek-OCR.",
        "image_ocr_tab": "Image OCR",
        "pdf_ocr_tab": "PDF OCR",
        "about_tab": "About",
        "upload_image": "Upload Image",
        "upload_pdf": "Upload PDF",
        "select_prompt": "Select Prompt Template",
        "custom_prompt": "Custom Prompt (edit if needed)",
        "enable_cropping": "Enable Image Cropping",
        "show_boxes": "Show Bounding Boxes",
        "process_image": "Process Image",
        "process_pdf": "Process PDF",
        "cancel_pdf": "Cancel Processing",
        "result_boxes": "Result with Bounding Boxes",
        "extracted_text": "Extracted Text",
        "raw_output": "Raw Output (with detection tags)",
        "raw_model_output": "Raw Model Output",
        "pdf_output": "Extracted Text from PDF",
        "max_pages": "Max Pages to Process (0 = all pages)",
        "language": "Language",
        "select_markdown_file": "Select Markdown File",
        "download_all_files": "Download All Files",
        "please_upload_image": "Please upload an image first.",
        "failed_load_image": "Failed to load image.",
        "loading_image": "Loading image...",
        "processing_image": "Processing image...",
        "running_ocr": "Running OCR...",
        "processing_results": "Processing results...",
        "complete": "Complete!",
        "please_upload_pdf": "Please upload a PDF file first.",
        "converting_pdf": "Converting PDF to images...",
        "processing_page": "Processing page",
        "error_ocr": "Error during OCR:",
        "error_pdf": "Error processing PDF:",
        "cancelled": "Processing cancelled by user.",
        "prompt_doc_md": "Document to Markdown",
        "prompt_ocr_grounding": "OCR with Grounding",
        "prompt_free_ocr": "Free OCR",
        "prompt_parse_figure": "Parse Figure",
        "prompt_describe_image": "Describe Image",
        "about_title": "## About DeepSeek-OCR",
        "about_content": """
DeepSeek-OCR is a powerful optical character recognition model that can:
- Extract text from images and documents
- Detect document structure and layouts
- Convert documents to Markdown format
- Parse figures and diagrams
- Provide detailed image descriptions

### Usage Tips

1. **Image OCR**: Upload an image and select a prompt template. The model will extract text and optionally show bounding boxes for detected elements.

2. **PDF OCR**: Upload a PDF file to process multiple pages. You can limit the number of pages to process.

3. **Cropping**: Enable image cropping for better results on high-resolution images. This splits the image into tiles for more detailed processing.

4. **Prompts**:
   - **Document to Markdown**: Best for documents, papers, and text-heavy content
   - **OCR with Grounding**: Extracts text with layout information
   - **Free OCR**: Simple text extraction without layout detection
   - **Parse Figure**: Optimized for charts, diagrams, and figures
   - **Describe Image**: General image description

### Model Information

- **Model**: DeepSeek-OCR
- **Base Resolution**: {base_size}x{base_size}
- **Crop Resolution**: {image_size}x{image_size}
- **Default Cropping**: {crop_mode}

For more information, visit the [DeepSeek-OCR repository](https://github.com/deepseek-ai/DeepSeek-OCR).
""",
    },
    "zh": {
        "title": "🔍 DeepSeek-OCR vLLM 黄哥写书",
        "subtitle": "上传图片或PDF文档，使用DeepSeek-OCR提取文本和文档结构。",
        "image_ocr_tab": "图片OCR",
        "pdf_ocr_tab": "PDF OCR",
        "about_tab": "关于",
        "upload_image": "上传图片",
        "upload_pdf": "上传PDF",
        "select_prompt": "选择提示词模板",
        "custom_prompt": "自定义提示词（可编辑）",
        "enable_cropping": "启用图片裁剪",
        "show_boxes": "显示边界框",
        "process_image": "处理图片",
        "process_pdf": "处理PDF",
        "cancel_pdf": "取消处理",
        "result_boxes": "带边界框的结果",
        "extracted_text": "提取的文本",
        "raw_output": "原始输出（包含检测标签）",
        "raw_model_output": "原始模型输出",
        "pdf_output": "从PDF提取的文本",
        "max_pages": "最大处理页数（0 = 所有页面）",
        "language": "语言",
        "select_markdown_file": "选择Markdown文件",
        "download_all_files": "下载所有文件",
        "please_upload_image": "请先上传图片。",
        "failed_load_image": "加载图片失败。",
        "loading_image": "加载图片中...",
        "processing_image": "处理图片中...",
        "running_ocr": "运行OCR中...",
        "processing_results": "处理结果中...",
        "complete": "完成！",
        "please_upload_pdf": "请先上传PDF文件。",
        "converting_pdf": "转换PDF为图片中...",
        "processing_page": "处理页面",
        "error_ocr": "OCR过程出错：",
        "error_pdf": "处理PDF出错：",
        "cancelled": "用户已取消处理。",
        "prompt_doc_md": "文档转Markdown",
        "prompt_ocr_grounding": "OCR（带定位）",
        "prompt_free_ocr": "自由OCR",
        "prompt_parse_figure": "解析图表",
        "prompt_describe_image": "描述图片",
        "about_title": "## 关于 DeepSeek-OCR",
        "about_content": """
DeepSeek-OCR 是一个强大的光学字符识别模型，可以：
- 从图片和文档中提取文本
- 检测文档结构和布局
- 将文档转换为Markdown格式
- 解析图表和图形
- 提供详细的图片描述

### 使用提示

1. **图片OCR**：上传图片并选择提示词模板。模型将提取文本，并可选择显示检测到的元素的边界框。

2. **PDF OCR**：上传PDF文件以处理多页文档。您可以限制要处理的页数。

3. **裁剪**：对高分辨率图片启用图片裁剪可获得更好的结果。这会将图片分割成多个区块以进行更详细的处理。

4. **提示词**：
   - **文档转Markdown**：最适合文档、论文和文本密集型内容
   - **OCR（带定位）**：提取带有布局信息的文本
   - **自由OCR**：简单的文本提取，不检测布局
   - **解析图表**：针对图表、图形和图示进行优化
   - **描述图片**：通用图片描述

### 模型信息

- **模型**：DeepSeek-OCR
- **基础分辨率**：{base_size}x{base_size}
- **裁剪分辨率**：{image_size}x{image_size}
- **默认裁剪**：{crop_mode}

更多信息请访问 [DeepSeek-OCR 仓库](https://github.com/deepseek-ai/DeepSeek-OCR)。
""",
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """Get translated text for a given key and language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


def load_image(image_input):
    """Load and correct image orientation"""
    try:
        print(f"[DEBUG] load_image called with type: {type(image_input)}")
        print(f"[DEBUG] image_input value: {image_input if not isinstance(image_input, np.ndarray) else f'numpy array shape: {image_input.shape}'}")
        
        if isinstance(image_input, str):
            image = Image.open(image_input)
        elif isinstance(image_input, Image.Image):
            image = image_input
        elif isinstance(image_input, np.ndarray):
            # Handle numpy array from webcam or other sources
            image = Image.fromarray(image_input)
        elif isinstance(image_input, dict):
            # Handle potential gr.Image dict formats
            print(f"[DEBUG] image_input is dict with keys: {list(image_input.keys())}")
            arr = image_input.get("image") or image_input.get("array") or image_input.get("value")
            if isinstance(arr, np.ndarray):
                image = Image.fromarray(arr)
            elif isinstance(arr, str):
                image = Image.open(arr)
            else:
                print("[DEBUG] Unsupported dict content for image")
                return None
        elif image_input is None:
            print("[DEBUG] image_input is None")
            return None
        else:
            print(f"[DEBUG] Unhandled image type: {type(image_input)}")
            return None
        
        corrected_image = ImageOps.exif_transpose(image)
        print(f"[DEBUG] Image loaded successfully, size: {corrected_image.size}")
        return corrected_image.convert('RGB')
    except Exception as e:
        print(f"Error loading image: {e}")
        import traceback
        traceback.print_exc()
        return None


def normalize_image_input(image_input):
    """Return the underlying payload for Gradio image inputs when available."""
    if isinstance(image_input, dict):
        return image_input.get("image") or image_input.get("array") or image_input.get("value")
    return image_input


def is_valid_image_input(image_input):
    """Check whether the provided input represents usable image data."""
    candidate = normalize_image_input(image_input)

    if candidate is None:
        return False

    if isinstance(candidate, np.ndarray):
        return candidate.size > 0

    return True


def choose_first_valid_image(*sources: Tuple[str, object]) -> Tuple[str, object]:
    """Return the first (source, payload) tuple that contains usable image data."""
    for label, raw in sources:
        if is_valid_image_input(raw):
            return label, normalize_image_input(raw)
    return "none", None


def iter_pdf_images(pdf_path: str, dpi: int = 144, start_page: int = 0, end_page: Optional[int] = None) -> Iterator[Tuple[int, Image.Image]]:
    """Lazily render PDF pages to PIL images to avoid high RAM usage.

    Yields (page_index, PIL.Image) for each page in [start_page, end_page).
    """
    Image.MAX_IMAGE_PIXELS = None
    doc = fitz.open(pdf_path)
    try:
        total = doc.page_count
        if end_page is None or end_page > total:
            end_page = total

        start_page = max(0, start_page)

        zoom = dpi / 72.0
        matrix = fitz.Matrix(zoom, zoom)

        for page_num in range(start_page, end_page):
            page = doc[page_num]
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            # Use PNG bytes to leverage libpng compression and reduce peak memory during conversion
            img_data = pixmap.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            yield page_num, img
            # Help GC promptly
            del pixmap, img_data
    finally:
        doc.close()


def re_match(text):
    """Extract reference patterns from text"""
    pattern = r'(<\|ref\|>(.*?)<\|/ref\|><\|det\|>(.*?)<\|/det\|>)'
    matches = re.findall(pattern, text, re.DOTALL)
    
    matches_image = []
    matches_other = []
    for a_match in matches:
        if '<|ref|>image<|/ref|>' in a_match[0]:
            matches_image.append(a_match[0])
        else:
            matches_other.append(a_match[0])
    return matches, matches_image, matches_other


def extract_coordinates_and_label(ref_text, image_width, image_height):
    """Extract bounding box coordinates and labels"""
    try:
        label_type = ref_text[1]
        cor_list = eval(ref_text[2])
    except Exception as e:
        print(f"Error extracting coordinates: {e}")
        return None
    return (label_type, cor_list)


def draw_bounding_boxes(image, refs):
    """Draw bounding boxes on image"""
    image_width, image_height = image.size
    img_draw = image.copy()
    draw = ImageDraw.Draw(img_draw)
    
    overlay = Image.new('RGBA', img_draw.size, (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(overlay)
    
    font = ImageFont.load_default()
    
    for i, ref in enumerate(refs):
        try:
            result = extract_coordinates_and_label(ref, image_width, image_height)
            if result:
                label_type, points_list = result
                
                color = (np.random.randint(0, 200), np.random.randint(0, 200), np.random.randint(0, 255))
                color_a = color + (20,)
                
                for points in points_list:
                    x1, y1, x2, y2 = points
                    
                    x1 = int(x1 / 999 * image_width)
                    y1 = int(y1 / 999 * image_height)
                    x2 = int(x2 / 999 * image_width)
                    y2 = int(y2 / 999 * image_height)
                    
                    try:
                        if label_type == 'title':
                            draw.rectangle([x1, y1, x2, y2], outline=color, width=4)
                            draw2.rectangle([x1, y1, x2, y2], fill=color_a, outline=(0, 0, 0, 0), width=1)
                        else:
                            draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
                            draw2.rectangle([x1, y1, x2, y2], fill=color_a, outline=(0, 0, 0, 0), width=1)
                        
                        text_x = x1
                        text_y = max(0, y1 - 15)
                        
                        text_bbox = draw.textbbox((0, 0), label_type, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        text_height = text_bbox[3] - text_bbox[1]
                        draw.rectangle([text_x, text_y, text_x + text_width, text_y + text_height],
                                     fill=(255, 255, 255, 30))
                        draw.text((text_x, text_y), label_type, font=font, fill=color)
                    except:
                        pass
        except:
            continue
    
    img_draw.paste(overlay, (0, 0), overlay)
    return img_draw


async def initialize_engine():
    """Initialize the AsyncLLMEngine"""
    global engine
    if engine is None:
        engine_args = AsyncEngineArgs(
            model=MODEL_PATH,
            hf_overrides={"architectures": ["DeepseekOCRForCausalLM"]},
            block_size=256,
            max_model_len=8192,
            enforce_eager=False,
            trust_remote_code=True,
            tensor_parallel_size=1,
            gpu_memory_utilization=0.75,
        )
        engine = AsyncLLMEngine.from_engine_args(engine_args)
    return engine


async def generate_ocr_result(image_features, prompt: str, progress=gr.Progress()):
    """Generate OCR result using the model"""
    global engine
    
    if engine is None:
        await initialize_engine()
    
    logits_processors = [NoRepeatNGramLogitsProcessor(
        ngram_size=30, window_size=90, whitelist_token_ids={128821, 128822}
    )]
    
    sampling_params = SamplingParams(
        temperature=0.0,
        max_tokens=4096,  # Reduced from 8192 to speed up processing and avoid timeouts
        logits_processors=logits_processors,
        skip_special_tokens=False,
    )
    
    request_id = f"request-{os.urandom(16).hex()}"
    
    if image_features and '<image>' in prompt:
        request = {
            "prompt": prompt,
            "multi_modal_data": {"image": image_features}
        }
    elif prompt:
        request = {
            "prompt": prompt
        }
    else:
        return "Error: No prompt provided!"
    
    try:
        full_text = ""
        async for request_output in engine.generate(request, sampling_params, request_id):
            if request_output.outputs:
                full_text = request_output.outputs[0].text
        
        return full_text
    except Exception as e:
        if "timed out" in str(e).lower() or "timeout" in str(e).lower():
            return "Error: Processing timed out. Try reducing image complexity or using smaller batch sizes."
        else:
            return f"Error during generation: {str(e)}"


def process_ocr_image(
    image,  # Can be PIL Image, numpy array, or file path
    prompt_template: str,
    use_cropping: bool,
    show_bounding_boxes: bool,
    lang: str,
    progress=gr.Progress()
):
    """Process a single image for OCR"""
    print(f"[DEBUG] process_ocr_image called")
    print(f"[DEBUG] image parameter type: {type(image)}")
    print(f"[DEBUG] image parameter value: {image if not isinstance(image, np.ndarray) else f'numpy array shape: {image.shape}'}")
    
    if image is None:
        print("[DEBUG] Image is None, returning error message")
        return None, get_text("please_upload_image", lang), None
    
    progress(0.1, desc=get_text("loading_image", lang))
    image = load_image(image)
    if image is None:
        print("[DEBUG] load_image returned None")
        return None, get_text("failed_load_image", lang), None
    
    progress(0.2, desc=get_text("processing_image", lang))
    try:
        if '<image>' in prompt_template:
            image_features = DeepseekOCRProcessor().tokenize_with_images(
                images=[image], bos=True, eos=True, cropping=use_cropping
            )
        else:
            image_features = ''
        
        progress(0.5, desc=get_text("running_ocr", lang))
        result_text = asyncio.run(generate_ocr_result(image_features, prompt_template, progress))
        
        # Process the output
        progress(0.9, desc=get_text("processing_results", lang))
        matches_ref, matches_images, matches_other = re_match(result_text)
        
        # Clean up the text
        clean_text = result_text
        for match in matches_images + matches_other:
            clean_text = clean_text.replace(match, '')
        clean_text = clean_text.replace('\\coloneqq', ':=').replace('\\eqqcolon', '=:')
        
        # Draw bounding boxes if requested
        output_image = None
        if show_bounding_boxes and matches_ref:
            output_image = draw_bounding_boxes(image.copy(), matches_ref)
        
        progress(1.0, desc=get_text("complete", lang))
        return output_image, clean_text, result_text
        
    except Exception as e:
        return None, f"{get_text('error_ocr', lang)} {str(e)}", None


def process_ocr_pdf(
    pdf_file,
    prompt_template: str,
    use_cropping: bool,
    max_pages: int,
    batch_size: int,
    lang: str,
    progress=gr.Progress()
):
    """Process a PDF file for OCR"""
    global pdf_processing_cancelled
    
    if pdf_file is None:
        return [], get_text("please_upload_pdf", lang)
    
    try:
        progress(0.05, desc=get_text("converting_pdf", lang))

        # Determine total number of pages without rendering all pages up front
        with fitz.open(pdf_file.name) as _doc_probe:
            total_pages = _doc_probe.page_count

        # Respect max_pages selection
        if max_pages and max_pages > 0:
            num_pages = min(max_pages, total_pages)
        else:
            num_pages = total_pages

        os.makedirs("output", exist_ok=True)
        base_name = os.path.splitext(os.path.basename(pdf_file.name))[0]
        
        if num_pages <= 25:
            # Process as single batch
            all_results = []
            effective_batch_size = max(1, min(batch_size, num_pages))

            # Iterate through pages in small chunks to control RAM usage
            for i in range(0, num_pages, effective_batch_size):
                if pdf_processing_cancelled:
                    pdf_processing_cancelled = False
                    return [], get_text("cancelled", lang)
                
                sub_indices = list(range(i, min(i + effective_batch_size, num_pages)))
                
                progress((i + len(sub_indices)) / num_pages, desc=f"{get_text('processing_page', lang)} {i + 1}-{min(i + effective_batch_size, num_pages)}/{num_pages}...")
                
                try:
                    # Prepare batch inputs
                    batch_inputs = []
                    # Lazily render only the pages in this chunk
                    sub_images = []
                    for page_idx, image in iter_pdf_images(pdf_file.name, dpi=144, start_page=sub_indices[0], end_page=sub_indices[-1] + 1):
                        sub_images.append(image)
                        if '<image>' in prompt_template:
                            image_features = DeepseekOCRProcessor().tokenize_with_images(
                                images=[image], bos=True, eos=True, cropping=use_cropping
                            )
                        else:
                            image_features = ''
                        
                        request = {
                            "prompt": prompt_template,
                            "multi_modal_data": {"image": image_features} if image_features else {}
                        }
                        batch_inputs.append(request)
                    
                    # Generate for the batch
                    async def generate_batch():
                        global engine
                        if engine is None:
                            await initialize_engine()
                        
                        logits_processors = [NoRepeatNGramLogitsProcessor(
                            ngram_size=30, window_size=90, whitelist_token_ids={128821, 128822}
                        )]
                        
                        sampling_params = SamplingParams(
                            temperature=0.0,
                            max_tokens=8192,
                            logits_processors=logits_processors,
                            skip_special_tokens=False,
                        )
                        
                        results = []
                        for request in batch_inputs:
                            request_id = f"request-{os.urandom(16).hex()}"
                            full_text = ""
                            async for request_output in engine.generate(request, sampling_params, request_id):
                                if request_output.outputs:
                                    full_text = request_output.outputs[0].text
                            results.append(full_text)
                        return results
                    
                    batch_results = asyncio.run(generate_batch())
                    
                    # Process results
                    for idx_offset, (result_text, global_idx) in enumerate(zip(batch_results, sub_indices)):
                        matches_ref, matches_images, matches_other = re_match(result_text)
                        clean_text = result_text
                        for match in matches_images + matches_other:
                            clean_text = clean_text.replace(match, '')
                        clean_text = clean_text.replace('\\coloneqq', ':=').replace('\\eqqcolon', '=:')
                        
                        all_results.append(f"--- Page {global_idx + 1} ---\n{clean_text}\n")
                    # Help GC between chunks
                    del sub_images, batch_inputs, batch_results
                    import gc
                    gc.collect()
                        
                except Exception as batch_error:
                    for global_idx in sub_indices:
                        error_msg = f"--- Page {global_idx + 1} ---\nError processing page: {str(batch_error)}\n"
                        all_results.append(error_msg)
                    print(f"Error on batch {i//effective_batch_size + 1}: {batch_error}")
                    # Continue processing other batches
            
            progress(1.0, desc=get_text("complete", lang))
            return [], "\n".join(all_results)
        
        else:
            # Batch into 25 pages and save to files
            batch_size = 25
            file_paths = []
            
            for i in range(0, num_pages, batch_size):
                if pdf_processing_cancelled:
                    pdf_processing_cancelled = False
                    return [], get_text("cancelled", lang)
                
                sub_indices = list(range(i, min(i + batch_size, num_pages)))
                
                progress((i + len(sub_indices)) / num_pages, desc=f"{get_text('processing_page', lang)} {i + 1}-{min(i + batch_size, num_pages)}/{num_pages}...")
                
                try:
                    # Prepare batch inputs
                    batch_inputs = []
                    # Lazily render only the pages in this chunk
                    sub_images = []
                    for page_idx, image in iter_pdf_images(pdf_file.name, dpi=144, start_page=sub_indices[0], end_page=sub_indices[-1] + 1):
                        sub_images.append(image)
                        if '<image>' in prompt_template:
                            image_features = DeepseekOCRProcessor().tokenize_with_images(
                                images=[image], bos=True, eos=True, cropping=use_cropping
                            )
                        else:
                            image_features = ''
                        
                        request = {
                            "prompt": prompt_template,
                            "multi_modal_data": {"image": image_features} if image_features else {}
                        }
                        batch_inputs.append(request)
                    
                    # Generate for the batch
                    async def generate_batch():
                        global engine
                        if engine is None:
                            await initialize_engine()
                        
                        logits_processors = [NoRepeatNGramLogitsProcessor(
                            ngram_size=30, window_size=90, whitelist_token_ids={128821, 128822}
                        )]
                        
                        sampling_params = SamplingParams(
                            temperature=0.0,
                            max_tokens=8192,
                            logits_processors=logits_processors,
                            skip_special_tokens=False,
                        )
                        
                        results = []
                        for request in batch_inputs:
                            request_id = f"request-{os.urandom(16).hex()}"
                            full_text = ""
                            async for request_output in engine.generate(request, sampling_params, request_id):
                                if request_output.outputs:
                                    full_text = request_output.outputs[0].text
                            results.append(full_text)
                        return results
                    
                    batch_results = asyncio.run(generate_batch())
                    
                    # Process results
                    batch_texts = []
                    for idx_offset, (result_text, global_idx) in enumerate(zip(batch_results, sub_indices)):
                        matches_ref, matches_images, matches_other = re_match(result_text)
                        clean_text = result_text
                        for match in matches_images + matches_other:
                            clean_text = clean_text.replace(match, '')
                        clean_text = clean_text.replace('\\coloneqq', ':=').replace('\\eqqcolon', '=:')
                        
                        batch_texts.append(f"--- Page {global_idx + 1} ---\n{clean_text}\n")
                    
                    # Save to file
                    file_path = f"output/{base_name}_{i//batch_size + 1:03d}.md"
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("\n\n".join(batch_texts))
                    file_paths.append(file_path)
                    # Help GC between chunks
                    del sub_images, batch_inputs, batch_results, batch_texts
                    import gc
                    gc.collect()
                    
                except Exception as batch_error:
                    error_file_path = f"output/{base_name}_{i//batch_size + 1:03d}.md"
                    error_content = "\n\n".join([f"--- Page {global_idx + 1} ---\nError processing page: {str(batch_error)}\n" for global_idx in sub_indices])
                    with open(error_file_path, 'w', encoding='utf-8') as f:
                        f.write(error_content)
                    file_paths.append(error_file_path)
                    print(f"Error on batch {i//batch_size + 1}: {batch_error}")
                    # Continue processing other batches
            
            progress(1.0, desc=get_text("complete", lang))
            return file_paths, ""
        
    except Exception as e:
        progress(1.0, desc="Error occurred")
        return [], f"{get_text('error_pdf', lang)} {str(e)}"


def load_file_content(file_path):
    """Load content from a Markdown file"""
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def create_zip_of_files(file_paths):
    """Create a zip file containing all markdown files"""
    if not file_paths:
        return None
    
    # Get the base name from the first file
    if file_paths:
        base_name = os.path.basename(file_paths[0]).rsplit('_', 1)[0]
    else:
        base_name = "markdown_files"
    
    zip_path = f"output/{base_name}_all.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            if os.path.exists(file_path):
                zipf.write(file_path, os.path.basename(file_path))
    
    return zip_path


# Create Gradio interface
def create_gradio_app():
    """Create the Gradio web application"""
    
    # Predefined prompts
    prompts = {
        "en": {
            "Document to Markdown": "<image>\n<|grounding|>Convert the document to markdown.",
            "OCR with Grounding": "<image>\n<|grounding|>OCR this image.",
            "Free OCR": "<image>\nFree OCR.",
            "Parse Figure": "<image>\nParse the figure.",
            "Describe Image": "<image>\nDescribe this image in detail.",
        },
        "zh": {
            "文档转Markdown": "<image>\n<|grounding|>将文档转换为markdown。",
            "OCR（带定位）": "<image>\n<|grounding|>OCR 此图像。要求必须使用中文。",
            "自由OCR": "<image>\n自由 OCR,要求必须使用中文。",
            "解析图表": "<image>\n用中文解析图表。要求必须使用中文.",
            "描述图片": "<image>\n用中文详细描述此图像。要求必须使用中文描述图像。",
        }
    }
    
    def update_ui_language(lang):
        """Update all UI elements based on selected language"""
        prompt_choices = list(prompts[lang].keys())
        default_prompt = prompts[lang][prompt_choices[0]]
        
        return {
            title_md: get_text("title", lang) + "\n\n" + get_text("subtitle", lang),
            image_tab: get_text("image_ocr_tab", lang),
            pdf_tab: get_text("pdf_ocr_tab", lang),
            about_tab: get_text("about_tab", lang),
            prompt_dropdown: gr.Dropdown(choices=prompt_choices, value=prompt_choices[0], label=get_text("select_prompt", lang)),
            custom_prompt: gr.Textbox(value=default_prompt, label=get_text("custom_prompt", lang), lines=2),
            use_cropping: gr.Checkbox(value=CROP_MODE, label=get_text("enable_cropping", lang)),
            show_boxes: gr.Checkbox(value=True, label=get_text("show_boxes", lang)),
            process_btn: gr.Button(get_text("process_image", lang), variant="primary"),
            output_image: gr.Image(label=get_text("result_boxes", lang)),
            output_text: gr.Textbox(label=get_text("extracted_text", lang), lines=15, max_lines=20),
            raw_output_accordion: gr.Accordion(get_text("raw_output", lang), open=False),
            raw_output: gr.Textbox(label=get_text("raw_model_output", lang), lines=10),
            pdf_input: gr.File(label=get_text("upload_pdf", lang), file_types=[".pdf"]),
            pdf_prompt_dropdown: gr.Dropdown(choices=prompt_choices, value=prompt_choices[0], label=get_text("select_prompt", lang)),
            pdf_custom_prompt: gr.Textbox(value=default_prompt, label=get_text("custom_prompt", lang), lines=2),
            pdf_use_cropping: gr.Checkbox(value=CROP_MODE, label=get_text("enable_cropping", lang)),
            max_pages: gr.Slider(minimum=0, maximum=50, value=0, step=1, label=get_text("max_pages", lang)),
            batch_size: gr.Slider(minimum=1, maximum=10, value=1, step=1, label="Batch Size (pages per batch)"),
            pdf_process_btn: gr.Button(get_text("process_pdf", lang), variant="primary"),
            pdf_cancel_btn: gr.Button(get_text("cancel_pdf", lang), variant="stop"),
            file_selector: gr.Dropdown(choices=[], label=get_text("select_markdown_file", lang), visible=False),
            download_btn: gr.DownloadButton(label=get_text("download_all_files", lang), visible=False),
            pdf_output: gr.Textbox(label=get_text("pdf_output", lang), lines=25, max_lines=30, show_copy_button=True),
            about_md: get_text("about_content", lang).format(
                base_size=BASE_SIZE,
                image_size=IMAGE_SIZE,
                crop_mode="Enabled" if CROP_MODE else "Disabled"
            ),
        }
    
    with gr.Blocks(title="DeepSeek-OCR Web App", theme=gr.themes.Soft()) as app:
        # State to hold the latest non-empty image from any source
        current_image = gr.State(value=None)
        # Language selector at the top
        with gr.Row():
            with gr.Column(scale=4):
                title_md = gr.Markdown(get_text("title", "zh") + "\n\n" + get_text("subtitle", "zh"))
            with gr.Column(scale=1):
                lang_selector = gr.Radio(
                    choices=[("English", "en"), ("中文", "zh")],
                    value="zh",
                    label=get_text("language", "zh"),
                    container=False
                )
        
        with gr.Tabs() as tabs:
            with gr.Tab(get_text("image_ocr_tab", "zh")) as image_tab:
                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Tabs() as input_tabs:
                            with gr.Tab("Upload/Clipboard") as upload_tab:
                                image_upload = gr.Image(
                                    type="numpy",
                                    label="Upload or Paste Image",
                                    sources=["upload", "clipboard"]
                                )
                            with gr.Tab("Webcam") as webcam_tab:
                                image_webcam = gr.Image(
                                    type="numpy",
                                    label="Webcam Snapshot",
                                    sources=["webcam"]
                                )
                        
                        # Keep track of the latest image from either input
                        def set_image_from_upload(img):
                            payload = normalize_image_input(img)
                            debug_msg = f"[DEBUG] set_current_image from upload, type: {type(img)}"
                            if isinstance(payload, np.ndarray):
                                debug_msg += f", normalized shape: {payload.shape}"
                            print(debug_msg)
                            return payload
                        
                        def set_image_from_webcam(img, previous_image):
                            payload = normalize_image_input(img)
                            debug_msg = f"[DEBUG] set_current_image from webcam, type: {type(img)}"
                            if isinstance(payload, np.ndarray):
                                debug_msg += f", normalized shape: {payload.shape}"
                            print(debug_msg)

                            # Gradio emits None/empty frames when the webcam stops streaming; keep the last good frame
                            if not is_valid_image_input(img):
                                print("[DEBUG] Webcam delivered no usable data; retaining previous image")
                                return previous_image

                            return payload
                        
                        image_upload.change(
                            fn=set_image_from_upload,
                            inputs=[image_upload],
                            outputs=[current_image]
                        )
                        image_webcam.change(
                            fn=set_image_from_webcam,
                            inputs=[image_webcam, current_image],
                            outputs=[current_image]
                        )
                        
                        gr.Markdown("**Note:** For webcam, take a snapshot first, then click 'Process Image'.")
                        
                        prompt_dropdown = gr.Dropdown(
                            choices=list(prompts["zh"].keys()),
                            value="文档转Markdown",
                            label=get_text("select_prompt", "zh")
                        )
                        
                        custom_prompt = gr.Textbox(
                            value=prompts["zh"]["文档转Markdown"],
                            label=get_text("custom_prompt", "zh"),
                            lines=2
                        )
                        
                        with gr.Row():
                            use_cropping = gr.Checkbox(
                                value=CROP_MODE,
                                label=get_text("enable_cropping", "zh")
                            )
                            show_boxes = gr.Checkbox(
                                value=True,
                                label=get_text("show_boxes", "zh")
                            )
                        
                        process_btn = gr.Button(get_text("process_image", "zh"), variant="primary")
                    
                    with gr.Column(scale=1):
                        output_image = gr.Image(label=get_text("result_boxes", "zh"))
                        output_text = gr.Textbox(
                            label=get_text("extracted_text", "zh"),
                            lines=15,
                            max_lines=20
                        )
                
                with gr.Accordion(get_text("raw_output", "zh"), open=False) as raw_output_accordion:
                    raw_output = gr.Textbox(label=get_text("raw_model_output", "zh"), lines=10)
                
                # Update custom prompt when dropdown changes
                def update_prompt(selected, lang):
                    return prompts[lang][selected]
                
                prompt_dropdown.change(
                    fn=update_prompt,
                    inputs=[prompt_dropdown, lang_selector],
                    outputs=[custom_prompt]
                )
                
                # Process using the latest available image: prefer upload, then webcam, then state
                def process_image_with_fallback(upload_img, webcam_img, state_img, prompt, crop, boxes, lang_val):
                    src, img = choose_first_valid_image(
                        ("upload_event", upload_img),
                        ("webcam_event", webcam_img),
                        ("state", state_img),
                    )
                    print(f"[DEBUG] process_image_with_fallback choosing: {src}")

                    out_img, out_text, out_raw = process_ocr_image(img, prompt, crop, boxes, lang_val)

                    updated_state = img if is_valid_image_input(img) else state_img
                    return out_img, out_text, out_raw, updated_state

                process_btn.click(
                    fn=process_image_with_fallback,
                    inputs=[image_upload, image_webcam, current_image, custom_prompt, use_cropping, show_boxes, lang_selector],
                    outputs=[output_image, output_text, raw_output, current_image]
                )
            
            with gr.Tab(get_text("pdf_ocr_tab", "zh")) as pdf_tab:
                with gr.Row():
                    with gr.Column(scale=1):
                        pdf_input = gr.File(
                            label=get_text("upload_pdf", "zh"),
                            file_types=[".pdf"]
                        )
                        
                        pdf_prompt_dropdown = gr.Dropdown(
                            choices=list(prompts["zh"].keys()),
                            value="文档转Markdown",
                            label=get_text("select_prompt", "zh")
                        )
                        
                        pdf_custom_prompt = gr.Textbox(
                            value=prompts["zh"]["文档转Markdown"],
                            label=get_text("custom_prompt", "zh"),
                            lines=2
                        )
                        
                        pdf_use_cropping = gr.Checkbox(
                            value=CROP_MODE,
                            label=get_text("enable_cropping", "zh")
                        )
                        
                        max_pages = gr.Slider(
                            minimum=0,
                            maximum=50,
                            value=0,
                            step=1,
                            label=get_text("max_pages", "zh")
                        )
                        
                        batch_size = gr.Slider(
                            minimum=1,
                            maximum=10,
                            value=1,
                            step=1,
                            label="Batch Size (pages per batch)"
                        )
                        
                        with gr.Row():
                            pdf_process_btn = gr.Button(get_text("process_pdf", "zh"), variant="primary")
                            pdf_cancel_btn = gr.Button(get_text("cancel_pdf", "zh"), variant="stop")
                    
                    with gr.Column(scale=1):
                        with gr.Row():
                            file_selector = gr.Dropdown(choices=[], label=get_text("select_markdown_file", "zh"), visible=False, scale=3)
                            download_btn = gr.DownloadButton(label=get_text("download_all_files", "zh"), visible=False, scale=1)
                        pdf_output = gr.Textbox(
                            label=get_text("pdf_output", "zh"),
                            lines=25,
                            max_lines=30,
                            show_copy_button=True
                        )
                
                # Update PDF prompt when dropdown changes
                pdf_prompt_dropdown.change(
                    fn=update_prompt,
                    inputs=[pdf_prompt_dropdown, lang_selector],
                    outputs=[pdf_custom_prompt]
                )
                
                # State to store file paths
                file_paths_state = gr.State(value=[])
                
                def process_pdf_wrapper(pdf_file, prompt, crop, max_p, batch_s, lang, progress=gr.Progress()):
                    file_paths, content = process_ocr_pdf(pdf_file, prompt, crop, max_p, batch_s, lang, progress)
                    if file_paths:
                        zip_path = create_zip_of_files(file_paths)
                        return (
                            gr.update(choices=file_paths, value=file_paths[0], visible=True),
                            gr.update(value=zip_path, visible=True),
                            load_file_content(file_paths[0]),
                            file_paths
                        )
                    else:
                        return (
                            gr.update(choices=[], visible=False),
                            gr.update(visible=False),
                            content,
                            []
                        )
                
                # Process PDF button
                pdf_process_btn.click(
                    fn=process_pdf_wrapper,
                    inputs=[pdf_input, pdf_custom_prompt, pdf_use_cropping, max_pages, batch_size, lang_selector],
                    outputs=[file_selector, download_btn, pdf_output, file_paths_state],
                    show_progress="full"
                )
                
                # Load file content when selector changes
                file_selector.change(
                    fn=load_file_content,
                    inputs=[file_selector],
                    outputs=[pdf_output]
                )
                
                # Cancel PDF processing
                def cancel_pdf_processing():
                    global pdf_processing_cancelled
                    pdf_processing_cancelled = True
                    return "Cancelling..."
                
                pdf_cancel_btn.click(
                    fn=cancel_pdf_processing,
                    outputs=[pdf_output]
                )
            
            with gr.Tab(get_text("about_tab", "zh")) as about_tab:
                about_md = gr.Markdown(
                    get_text("about_title", "zh") + "\n" + 
                    get_text("about_content", "zh").format(
                        base_size=BASE_SIZE,
                        image_size=IMAGE_SIZE,
                        crop_mode="已启用" if CROP_MODE else "已禁用"
                    )
                )
        
        # Language change handler
        def change_language(lang):
            prompt_choices = list(prompts[lang].keys())
            default_prompt = prompts[lang][prompt_choices[0]]
            
            crop_text = "已启用" if CROP_MODE else "已禁用" if lang == "zh" else "Enabled" if CROP_MODE else "Disabled"
            
            return [
                # Title
                get_text("title", lang) + "\n\n" + get_text("subtitle", lang),
                # Tab labels - using update to change label
                gr.Tab(label=get_text("image_ocr_tab", lang)),
                gr.Tab(label=get_text("pdf_ocr_tab", lang)),
                gr.Tab(label=get_text("about_tab", lang)),
                # Image OCR tab - just update the dropdown and prompt
                gr.Dropdown(choices=prompt_choices, value=prompt_choices[0], label=get_text("select_prompt", lang)),
                gr.Textbox(value=default_prompt, label=get_text("custom_prompt", lang), lines=2),
                gr.Checkbox(value=CROP_MODE, label=get_text("enable_cropping", lang)),
                gr.Checkbox(value=True, label=get_text("show_boxes", lang)),
                gr.Button(get_text("process_image", lang), variant="primary"),
                gr.Image(label=get_text("result_boxes", lang)),
                gr.Textbox(label=get_text("extracted_text", lang), lines=15, max_lines=20),
                gr.Accordion(label=get_text("raw_output", lang), open=False),
                gr.Textbox(label=get_text("raw_model_output", lang), lines=10),
                # PDF OCR tab
                gr.File(label=get_text("upload_pdf", lang), file_types=[".pdf"]),
                gr.Dropdown(choices=prompt_choices, value=prompt_choices[0], label=get_text("select_prompt", lang)),
                gr.Textbox(value=default_prompt, label=get_text("custom_prompt", lang), lines=2),
                gr.Checkbox(value=CROP_MODE, label=get_text("enable_cropping", lang)),
                gr.Slider(minimum=0, maximum=50, value=0, step=1, label=get_text("max_pages", lang)),
                gr.Slider(minimum=1, maximum=10, value=1, step=1, label="Batch Size (pages per batch)"),
                gr.Button(get_text("process_pdf", lang), variant="primary"),
                gr.Button(get_text("cancel_pdf", lang), variant="stop"),
                gr.Dropdown(choices=[], label=get_text("select_markdown_file", lang), visible=False),
                gr.DownloadButton(label=get_text("download_all_files", lang), visible=False),
                gr.Textbox(label=get_text("pdf_output", lang), lines=25, max_lines=30, show_copy_button=True),
                # About tab
                get_text("about_title", lang) + "\n" + get_text("about_content", lang).format(
                    base_size=BASE_SIZE,
                    image_size=IMAGE_SIZE,
                    crop_mode=crop_text
                ),
            ]
        
        lang_selector.change(
            fn=change_language,
            inputs=[lang_selector],
            outputs=[
                title_md, image_tab, pdf_tab, about_tab,
                prompt_dropdown, custom_prompt, use_cropping, show_boxes, process_btn,
                output_image, output_text, raw_output_accordion, raw_output,
                pdf_input, pdf_prompt_dropdown, pdf_custom_prompt, pdf_use_cropping, max_pages, batch_size,
                pdf_process_btn, pdf_cancel_btn, file_selector, download_btn, pdf_output, about_md
            ]
        )
    
    return app


if __name__ == "__main__":
    print("Initializing DeepSeek-OCR Web Application...")
    print(f"Model Path: {MODEL_PATH}")
    print(f"Image Size: {IMAGE_SIZE}, Base Size: {BASE_SIZE}")
    print(f"Crop Mode: {CROP_MODE}")
    
    # Initialize the engine in the background
    print("\nStarting engine initialization...")
    
    app = create_gradio_app()
    app.queue()
    app.launch(
        server_name="localhost",
        server_port=7860,
        share=False,
        show_error=True
    )
