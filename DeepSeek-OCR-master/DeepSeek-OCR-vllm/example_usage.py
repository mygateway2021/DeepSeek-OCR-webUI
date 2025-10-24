"""
Example script showing how to use DeepSeek-OCR programmatically
This can be useful for integrating OCR into your own applications
"""

import asyncio
from PIL import Image
from gradio_app import (
    load_image,
    initialize_engine,
    generate_ocr_result,
    process_ocr_image,
    re_match
)
from process.image_process import DeepseekOCRProcessor


async def simple_ocr_example(image_path: str, prompt: str = None):
    """
    Simple example: OCR a single image
    
    Args:
        image_path: Path to image file
        prompt: OCR prompt (default: Document to Markdown)
    
    Returns:
        str: Extracted text
    """
    if prompt is None:
        prompt = "<image>\n<|grounding|>Convert the document to markdown."
    
    # Load image
    print(f"Loading image: {image_path}")
    image = load_image(image_path)
    if image is None:
        print("Failed to load image")
        return None
    
    # Initialize engine
    print("Initializing OCR engine...")
    await initialize_engine()
    
    # Process image
    print("Processing image...")
    image_features = DeepseekOCRProcessor().tokenize_with_images(
        images=[image], bos=True, eos=True, cropping=True
    )
    
    # Generate OCR result
    print("Running OCR...")
    result = await generate_ocr_result(image_features, prompt)
    
    # Clean up result
    matches_ref, matches_images, matches_other = re_match(result)
    clean_text = result
    for match in matches_images + matches_other:
        clean_text = clean_text.replace(match, '')
    clean_text = clean_text.replace('\\coloneqq', ':=').replace('\\eqqcolon', '=:')
    
    return clean_text


async def batch_ocr_example(image_paths: list, prompt: str = None):
    """
    Batch processing example: OCR multiple images
    
    Args:
        image_paths: List of image file paths
        prompt: OCR prompt (default: Document to Markdown)
    
    Returns:
        list: List of extracted texts
    """
    if prompt is None:
        prompt = "<image>\n<|grounding|>Convert the document to markdown."
    
    # Initialize engine once
    print("Initializing OCR engine...")
    await initialize_engine()
    
    results = []
    for i, image_path in enumerate(image_paths):
        print(f"\nProcessing image {i+1}/{len(image_paths)}: {image_path}")
        
        # Load image
        image = load_image(image_path)
        if image is None:
            print(f"Failed to load image: {image_path}")
            results.append(None)
            continue
        
        # Process image
        image_features = DeepseekOCRProcessor().tokenize_with_images(
            images=[image], bos=True, eos=True, cropping=True
        )
        
        # Generate OCR result
        result = await generate_ocr_result(image_features, prompt)
        
        # Clean up result
        matches_ref, matches_images, matches_other = re_match(result)
        clean_text = result
        for match in matches_images + matches_other:
            clean_text = clean_text.replace(match, '')
        clean_text = clean_text.replace('\\coloneqq', ':=').replace('\\eqqcolon', '=:')
        
        results.append(clean_text)
        print(f"Completed: {len(clean_text)} characters extracted")
    
    return results


async def custom_prompt_example(image_path: str):
    """
    Example with different prompt types
    
    Args:
        image_path: Path to image file
    """
    prompts = {
        "Markdown": "<image>\n<|grounding|>Convert the document to markdown.",
        "OCR with Grounding": "<image>\n<|grounding|>OCR this image.",
        "Free OCR": "<image>\nFree OCR.",
        "Parse Figure": "<image>\nParse the figure.",
        "Describe": "<image>\nDescribe this image in detail.",
    }
    
    # Initialize engine
    await initialize_engine()
    
    # Load image once
    image = load_image(image_path)
    if image is None:
        print("Failed to load image")
        return
    
    results = {}
    for name, prompt in prompts.items():
        print(f"\n{'='*50}")
        print(f"Testing prompt: {name}")
        print(f"{'='*50}")
        
        image_features = DeepseekOCRProcessor().tokenize_with_images(
            images=[image], bos=True, eos=True, cropping=True
        )
        
        result = await generate_ocr_result(image_features, prompt)
        
        # Clean up result
        matches_ref, matches_images, matches_other = re_match(result)
        clean_text = result
        for match in matches_images + matches_other:
            clean_text = clean_text.replace(match, '')
        clean_text = clean_text.replace('\\coloneqq', ':=').replace('\\eqqcolon', '=:')
        
        results[name] = clean_text
        print(f"\nResult preview (first 200 chars):")
        print(clean_text[:200] + "..." if len(clean_text) > 200 else clean_text)
    
    return results


def main():
    """
    Main function with examples
    """
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python example_usage.py <image_path>                    # Simple OCR")
        print("  python example_usage.py <image1> <image2> ...          # Batch OCR")
        print("  python example_usage.py --prompts <image_path>         # Try all prompts")
        print("\nExamples:")
        print("  python example_usage.py document.jpg")
        print("  python example_usage.py page1.jpg page2.jpg page3.jpg")
        print("  python example_usage.py --prompts figure.png")
        return
    
    if sys.argv[1] == "--prompts":
        if len(sys.argv) < 3:
            print("Please provide an image path")
            return
        
        print("Testing all prompt types...")
        results = asyncio.run(custom_prompt_example(sys.argv[2]))
        
        print("\n" + "="*50)
        print("SUMMARY")
        print("="*50)
        for name, text in results.items():
            print(f"\n{name}: {len(text)} characters")
    
    elif len(sys.argv) == 2:
        # Single image
        print("Processing single image...")
        result = asyncio.run(simple_ocr_example(sys.argv[1]))
        
        if result:
            print("\n" + "="*50)
            print("RESULT")
            print("="*50)
            print(result)
            print(f"\nTotal characters: {len(result)}")
    
    else:
        # Multiple images
        image_paths = sys.argv[1:]
        print(f"Processing {len(image_paths)} images...")
        results = asyncio.run(batch_ocr_example(image_paths))
        
        print("\n" + "="*50)
        print("RESULTS SUMMARY")
        print("="*50)
        for i, (path, result) in enumerate(zip(image_paths, results)):
            if result:
                print(f"\n{i+1}. {path}")
                print(f"   Characters: {len(result)}")
                print(f"   Preview: {result[:100]}...")
            else:
                print(f"\n{i+1}. {path}")
                print(f"   Status: FAILED")


if __name__ == "__main__":
    main()
