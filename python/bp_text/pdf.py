"""
This module implements functionality for PDF files. 

Created: 2025-03-27
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  21:24:00 Fri Mar 28 2025 CET
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

from . import language
from . import utilities

################################################################################

class Page(ABC):
    """
    Abstract base class for a page. 
    """
    def __init__(self,
                 page_num = None,
                 page_label = None,
                 data = None,
                 text = "",
                 lang = ""):
        ## the page number / index
        self._page_num = page_num
        ## the page number (number) label
        ## this might differ from the actual page number e.g.
        ## when sections of a document are labeled with roman
        ## numerals
        self._page_label = page_label
        ## additional data
        self._data = data
        ## the text contents of the page
        self._text = text
        ## the primary language of the page's content
        self._lang = lang
        self.update()

    ########################################

    @property
    def page_num(self):
        return self._page_num

    @page_num.setter
    def page_num(self, val):
        self._page_num = val

    @property
    def page_label(self):
        return self._page_label

    @page_label.setter
    def page_label(self, val):
        self._page_label = val

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        self._data = val

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        if isinstance(val, str):
            self._text = val
        else:
            print("Error: value for text is not a String.")
        self.update()

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, val):
        if val != "":
            self._lang = langcodes.standardize_tag(val)
        else:
            self._lang = ""

    ########################################

    def update(self):
        ## detect and update language
        self.detect_lang(set_lang = True)

    def detect_lang(self, set_lang = True):
        """Detect the language of text"""
        lang = None
        detector = language.LanguageDetector().detector
        if self.text != "":
            lang = detector.detect_language_of(self.text)
        else:
            return False
        langcode = lang.iso_code_639_1.name
        if set_lang:
            self.lang = langcode
        return langcode

    def count_words(self):
        return len(self._text.split())




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
                ## Initialize the number tree
                self._number_tree = self._reader.trailer['/Root'] \
                                                .get('/PageLabels')
            else:
                pass
        else:
            print(f"Error: The file '{self._file}' does not exist.")
            return False
        ## calculate file checksum
        self._file_checksum = utilities.file_checksum(self._file,
                                                      algorithm = "sha256")
        ## auto-extract
        if self._auto_extract:
            self.data = self.extract_text()
        ## set (primary) language if not given
        if self.lang == "" or not self.lang:
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
            if page_text:
                page_ob = PdfPage(lang = self.lang,
                                  text = page_text,
                                  data = page,
                                  page_num = i,
                                  page_label = "" # TODO
                                  )
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
                                  page_label = "", # TODO
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

    def get_primary_lang(self):
        """
        Get the primary language of a PDF.
        """
        if self.data == "":
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
