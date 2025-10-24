#!/usr/bin/env python3
"""
Script to apply remaining fixes to gradio_app.py for preventing automatic shutdown
during long PDF processing.
"""

import re

def fix_gradio_app():
    """Apply fixes to gradio_app.py"""
    
    # Read the file
    with open('/home/huangz/github/DeepSeek-OCR/DeepSeek-OCR-master/DeepSeek-OCR-vllm/gradio_app.py', 'r') as f:
        content = f.read()
    
    # Fix 1: Replace max_tokens=8192 with 1536 in PDF processing sections
    content = re.sub(
        r'max_tokens=8192,',
        'max_tokens=1536,  # Reduced for PDF processing to prevent timeouts',
        content
    )
    
    # Fix 2: Add timeout and memory management to PDF batch processing
    # Pattern 1: First batch processing section
    pattern1 = r'(\s+)for request in batch_inputs:\s*\n(\s+)request_id = f"request-\{os\.urandom\(16\)\.hex\(\)\}"\s*\n(\s+)full_text = ""\s*\n(\s+)async for request_output in engine\.generate\(request, sampling_params, request_id\):\s*\n(\s+)if request_output\.outputs:\s*\n(\s+)full_text = request_output\.outputs\[0\]\.text\s*\n(\s+)results\.append\(full_text\)'
    
    replacement1 = r'''\1for request in batch_inputs:
\2request_id = f"request-{os.urandom(16).hex()}"
\2
\2# Add timeout for each request in batch
\2async def generate_single():
\2    async for request_output in engine.generate(request, sampling_params, request_id):
\2        if request_output.outputs:
\2            return request_output.outputs[0].text
\2    return ""
\2
\2try:
\2    full_text = await asyncio.wait_for(generate_single(), timeout=120)  # 2 min per page
\2except asyncio.TimeoutError:
\2    full_text = "[TIMEOUT] Page processing timed out"
\2
\2results.append(full_text)
\2
\2# Force cleanup after each page
\2import gc
\2gc.collect()'''
    
    content = re.sub(pattern1, replacement1, content, flags=re.MULTILINE)
    
    # Fix 3: Change batch size from 25 to 10
    content = re.sub(
        r'# Batch into 25 pages and save to files\s*\n\s*batch_size = 25',
        '# Batch into 10 pages and save to files (reduced from 25)\n            batch_size = 10',
        content
    )
    
    # Write back the file
    with open('/home/huangz/github/DeepSeek-OCR/DeepSeek-OCR-master/DeepSeek-OCR-vllm/gradio_app.py', 'w') as f:
        f.write(content)
    
    print("✓ Applied fixes to gradio_app.py")
    print("  - Reduced max_tokens from 8192 to 1536")
    print("  - Added timeout handling for PDF processing")
    print("  - Added memory cleanup after each page")
    print("  - Reduced batch size from 25 to 10 pages")

if __name__ == "__main__":
    fix_gradio_app()