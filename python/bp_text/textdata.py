"""
This module implements text functions.

Created: 2025-03-27
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  13:29:15 Thu Mar 27 2025 CET
"""

import os
import sys
import re
from pathlib import Path

from lingua import Language, LanguageDetectorBuilder
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

################################################################################
## pdf extraction

def extract_text_without_ocr(pdf_path):
    """Extract text from a PDF using PyPDF2."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
                
        return text.strip()
    except Exception as e:
        print(f"Error extracting text without OCR: {e}")
        return ""

def extract_text_with_ocr(pdf_path, dpi=300, lang='eng'):
    """Extract text from a PDF using Tesseract OCR."""
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=dpi)
        
        text = ""
        for image in images:
            page_text = pytesseract.image_to_string(image, lang=lang)
            text += page_text + "\n\n"
            
        return text.strip()
    except Exception as e:
        print(f"Error extracting text with OCR: {e}")
        return ""

def extract_text_from_pdf(pdf_path, use_ocr=False,
                          ocr_dpi=300, ocr_lang='eng',
                          fallback_to_ocr=True):
    """
    Extract text from a PDF file using direct extraction or OCR.
    
    Args:
        pdf_path (str): Path to the PDF file
        use_ocr (bool): Whether to use OCR for text extraction
        ocr_dpi (int): DPI for OCR processing
        ocr_lang (str): Language for OCR (default: 'eng')
        fallback_to_ocr (bool): Use OCR if direct extraction yields little text
        
    Returns:
        str: Extracted text
    """
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        return ""
    
    # Try direct extraction first
    if not use_ocr:
        text = extract_text_without_ocr(pdf_path)
        
        # Fall back to OCR if needed
        if fallback_to_ocr and (not text or len(text.split()) < 20):
            print("Direct extraction yielded little text, falling back to OCR")
            use_ocr = True
    
    # Use OCR if required
    if use_ocr:
        text = extract_text_with_ocr(pdf_path, dpi=ocr_dpi, lang=ocr_lang)
    return text


################################################################################
## EOF text.py
