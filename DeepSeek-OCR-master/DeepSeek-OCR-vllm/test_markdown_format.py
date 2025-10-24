#!/usr/bin/env python3
"""
Test script for the improved markdown formatting function
"""

import re

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

def format_as_markdown(text, page_num=None, doc_title=None):
    """Format OCR output as proper markdown with structure"""
    if not text or text.strip() == "":
        return text
    
    # Clean the text first
    matches_ref, matches_images, matches_other = re_match(text)
    clean_text = text
    for match in matches_images + matches_other:
        clean_text = clean_text.replace(match, '')
    clean_text = clean_text.replace('\\coloneqq', ':=').replace('\\eqqcolon', '=:')
    
    # Remove existing page headers (--- Page X ---)
    clean_text = re.sub(r'^---\s*Page\s+\d+\s*---\s*\n?', '', clean_text, flags=re.MULTILINE)
    
    # Split into lines and process
    lines = clean_text.strip().split('\n')
    formatted_lines = []
    
    # Add page header if specified
    if page_num is not None:
        formatted_lines.append(f"# Page {page_num}")
        if doc_title:
            formatted_lines.append(f"*From: {doc_title}*")
        formatted_lines.append("")
    
    # Process each line
    current_paragraph = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines but preserve paragraph breaks
        if not line:
            if current_paragraph:
                formatted_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            if not in_list:
                formatted_lines.append("")
            continue
        
        # Skip remaining page markers
        if re.match(r'^---\s*Page\s+\d+\s*---\s*$', line):
            continue
        
        # Detect headers (lines that are likely titles)
        if (
            len(line) < 120 and 
            not line.endswith(('.', ',', ';', ':', '!', '?')) and
            not line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')) and
            (line.isupper() or 
             any(char in line for char in ['第', '章', 'Chapter', 'Section', '序言']) or
             re.match(r'^\d+[\.\s]', line) or
             (len(line.split()) <= 10 and '：' not in line and '(' not in line))
        ):
            # Finish current paragraph
            if current_paragraph:
                formatted_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            
            # Add header
            formatted_lines.append("")
            formatted_lines.append(f"## {line}")
            formatted_lines.append("")
            in_list = False
            continue
        
        # Detect lists
        if line.startswith(('•', '-', '*', '・')):
            if current_paragraph:
                formatted_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            formatted_lines.append(f"- {line[1:].strip()}")
            in_list = True
            continue
        elif re.match(r'^\d+[\.\)\s]', line):
            if current_paragraph:
                formatted_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            match = re.match(r'^(\d+)[\.\)\s](.*)', line)
            if match:
                formatted_lines.append(f"{match.group(1)}. {match.group(2).strip()}")
            else:
                formatted_lines.append(f"- {line}")
            in_list = True
            continue
        
        # Regular text - accumulate into paragraph
        in_list = False
        current_paragraph.append(line)
    
    # Add final paragraph
    if current_paragraph:
        formatted_lines.append(' '.join(current_paragraph))
    
    return '\n'.join(formatted_lines)

# Test with sample OCR output
test_input = """--- Page 1 ---

7天學會大數據資料處理 NoSQL MongoDB 第三版

黃士嘉、林敬傑 著 入門與活用

快速具備MongoDB的基本使用技能活用大數據資料處理的實用人門書！

- 内容精簡、淺顯易懂，可7天快速學會MongoDB
- 搭配Robo3T的圖形介面操作，一步步帶領你上手
- 透過實際範例，準確掌握精髓技巧

序言

本書第一版和第二版分别在2016年和2017年出版，在博客來網路書店榮登電腦書籍資料庫類第一名。

MongoDB的特性如下：

1. 文件型導向的資料儲存及操作
2. Map-Reduce的聚合資料運算
3. 高度彈性的擴展功能"""

print("=== ORIGINAL ===")
print(test_input)
print("\n=== FORMATTED ===")
print(format_as_markdown(test_input, page_num=1, doc_title="MongoDB教學書"))