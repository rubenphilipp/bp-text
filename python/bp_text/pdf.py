"""
This module implements functionality for PDF files. 

Created: 2025-03-27
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  22:56:33 Sat Mar 29 2025 CET
"""

import os
import sys
import re
from pathlib import Path
from abc import ABC, abstractmethod

from lingua import Language, LanguageDetectorBuilder
import PyPDF2
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from pdf2image import convert_from_path
import pytesseract
import roman
import langcodes

from .page import Page
from . import language
from . import utilities


################################################################################

class PdfPage(Page):
    """
    A PDF page.
    """
    def __init__(self,
                 page_num = None,
                 page_label = None,
                 ## here, data holds a PyPDF2.PageObject (or None)
                 data = None,
                 text = "",
                 lang = ""):
        super(PdfPage, self).__init__(page_num,
                                      page_label,
                                      data,
                                      text,
                                      lang)
        ## call this again to perform tests
        self.data = data

    ########################################

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        ## test if data is a PyPDF2 PageObject
        if val != None and not isinstance(val, PyPDF2.PageObject):
            print(f"Error: The value for data is not a PyPDF2.PageObject, but "
                  + "a {type(val)}")
            return False
        self._data = val


    ########################################

    def extract_text(self, update_text = True):
        """
        Extract text from a PDF page using direct extraction.
        Returns the text as a string. 
        """
        if not self.data:
            print("Error: No data.")
            return False
        
        text = self.data.extract_text()

        if update_text:
            self.text = text
        
        return text



################################################################################

class PdfFile:
    """
    A PDF file. 
    """
    def __init__(self,
                 file: str,
                 auto_extract = True,
                 use_ocr = False,
                 fallback_to_ocr = True,
                 ocr_dpi = 300,
                 ocr_default_lang = 'eng'):
        ## The filepath
        self._file = file
        ## a sha256 checksum for the file
        self._file_checksum = None
        ## The PyPDF2.PdfReader object
        self._reader = None
        ## The number tree of the PDF
        ## cf. https://www.w3.org/WAI/GL/WCAG20-TECHS/PDF17.html
        self._number_tree = None
        ## The PDF primary language
        self._lang = ""
        ## Automatically extract data
        self._auto_extract = auto_extract
        ## Extraction args
        self._use_ocr = use_ocr
        self._fallback_to_ocr = fallback_to_ocr
        self._ocr_dpi = ocr_dpi
        self._ocr_default_lang = ocr_default_lang
        ## The PDF text contents
        self._data = None
        ########################################
        self.update()

    ########################################
        
    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, val):
        self._file = val
        self.update()

    @property
    def file_checksum(self):
        return self._file_checksum


    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, val):
        self._lang = langcodes.standardize_tag(val)
        ## also set OCR default lang (alpha3)
        self._ocr_default_lang = langcodes.get(self._lang) \
                                          .to_alpha3()
        return self._lang

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        self._data = val

    @property
    def reader(self):
        return self._reader

    @property
    def auto_extract(self):
        return self._auto_extract

    @auto_extract.setter
    def auto_extract(self, val):
        if isinstance(val, bool):
            self._auto_extract = val
        else:
            print(f"Error: '{val}' is not of type Boolean")
            return False

    ########################################

    def update(self):
        """Update the instance"""
        ## (re-)initialize the reader object
        if os.path.isfile(self._file):
            try:
                self._reader = PdfReader(self._file)
            except PdfReadError:
                print(f"Error: Invalid PDF file {self._file}")
                
            else:
                pass
        else:
            print(f"Error: The file '{self._file}' does not exist.")
            return False
        ## Initialize the number tree
        self._number_tree = self._reader.trailer['/Root'] \
                                        .get('/PageLabels')
        ## calculate file checksum
        self._file_checksum = utilities.file_checksum(self._file,
                                                      algorithm = "sha256")
        ## auto-extract
        if self._auto_extract:
            self.data = self.extract_text()
        ## set (primary) language if not given
        if (self.lang == "" or not self.lang) and self.data:
            self.lang = self.get_primary_lang()
        return self

    def extract_text_without_ocr(self):
        """
        Extract text from a PDF using PyPDF2.
        Returns a list of PdfPage objects. 
        """
        text = []

        for i, page in enumerate(self.reader.pages):
            page_text = page.extract_text()
            
            page_ob = PdfPage(lang = self.lang,
                              text = page_text,
                              data = page,
                              page_num = i,
                              page_label = self.get_page_label(i))
            text.append(page_ob)

        return text

    def extract_text_with_ocr(self):
        """
        Extract text from a PDF using Tesseract OCR.
        Returns a list of PdfPage objects.
        """
        text = []

        try:
            # convert pdf to images
            images = convert_from_path(self._file,
                                       dpi=self._ocr_dpi)
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(
                    image,
                    lang = self._ocr_default_lang)
                page_ob = PdfPage(page_num = i,
                                  page_label = self.get_page_label(i),
                                  text = page_text,
                                  lang = self.lang)
                text.append(page_ob)
                
            return text
        except Exception as e:
            print(f"Error extracting text with OCR: {e}")
            return []


    def extract_text(self):
        """
        Extract text from a PDF using direct extraction or OCR.
        Returns a list of PdfPage objects. 
        """
        if not os.path.exists(self.file):
            print(f"PDF file not found: {self.file}")
            return []

        use_ocr = self._use_ocr
        # Try direct extraction first
        if not use_ocr:
            
            text = self.extract_text_without_ocr()
            
            ## get the sum of words in result
            text_words = sum(map(lambda p: p.count_words(), text))
            # Fall back to OCR if needed
            if self._fallback_to_ocr and (not text or text_words < 20):
                print("Direct extraction yielded little text, "
                      +"falling back to OCR")
                use_ocr = True

        if use_ocr:
            text = self.extract_text_with_ocr()

        return text

    def get_page_label(self, page_num):
        """
        Returns the label (i.e. the page number according to the PDF number
        tree) of a pdf page by index (page_num, zero-based). 
        """
        if not self._number_tree:
            # no number tree, use page numstring instead
            return str(page_num + 1)
        
        label_tuples = self._number_tree.get_object()['/Nums']
        if len(label_tuples) % 2 != 0:
            print("Error: Label number tree is malformed.");
            return str(page_num + 1)

        page_labels = {}
        for i in range(0, len(label_tuples), 2):
            start_index = label_tuples[i]
            label_dict = label_tuples[i + 1].get_object()
            
            prefix = label_dict.get('P', '')
            start_number = label_dict.get('/St', 1)
            style = label_dict.get('/S')

            if style == '/D': # Decimal
                def ret_label(index):
                    return str(start_number + index)
            elif style == '/R': # Uppercase Roman
                def ret_label(index):
                    return roman.toRoman(start_number + index).upper()
            elif style == '/r': # Lowercase Roman
                def ret_label(index):
                    return roman.toRoman(start_number + index).lower()
            else:
                def ret_label(index):
                    return ""
            
            page_labels[start_index] = (prefix, ret_label, start_number)

        ## determine page label
        page_label = str(page_num + 1)
        for start_index, (prefix,
                          label_func,
                          start_number) in page_labels.items():
            if page_num >= start_index:
                page_label = prefix + label_func(page_num - start_index)

        return page_label
    

    def get_primary_lang(self):
        """
        Get the primary language of a PDF.
        """
        if self._data == "" or self._data == None:
            print("Error: Cannot detect language. No data!")
            return False
        pages_langs = map(lambda p: p.lang, self.data)
        pages_langs_lst = list(pages_langs)
        langs = dict.fromkeys(pages_langs_lst)
        if len(langs) == 1:
            return list(langs.keys())[0]
        else:
            ## get most used lang
            for lang in langs:
                langs[lang] = pages_langs_lst.count(lang)
            return sorted(langs.items(),
                          key=lambda item: item[1],
                          reverse=True)[0][0]


        


        
        


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
## EOF pdf.py
