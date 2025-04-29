"""
This module implements functionality for PDF files. 

Created: 2025-03-27
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  14:01:02 Tue Apr 29 2025 CEST
"""

import os
import sys
import re
from pathlib import Path
from abc import ABC, abstractmethod

from lingua import Language, LanguageDetectorBuilder

from pypdf import PageObject
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from pdf2image import convert_from_path
import pytesseract
import roman
import langcodes

from .page import Page
from . import language
from . import utilities
from . import text


################################################################################

class PdfPage(Page):
    """This is a class implementation for a PDF page.  A PDF page holds is a
    reference to a page in a PDF document, usually related to a
    :py:class:`bp_text.pdf.PdfFile` object.

    The data attribute is also capable of holding a pypdf.PageObject
    (optional), while the text attribute can contain text retrieved from the
    file (e.g. via OCR or direct extraction --
    cf. :py:func:`PdfPage.extract_text` or :py:func:`PdfFile.extract_text`).
    Please note that the pypdf.PageObject instances in the `data` attribute will
    **not** be (re-)stored when (un-)pickling the PdfPage. 

    :param page_num: The page number (zero-based) of the page in the related
        file.
    :type page_num: int
    :param page_label: The actual page label of the page in the PDF file.
        The actual PDF page number/label is defined in the PDF header and could
        differ from the `page_num` (e.g. by varying the start index being a
        roman instead of an arabic numeral.
    :type page_label: string
    :param data: A `pypdf.PageObject`. Default = None
    :type data: A `pypdf.PageObject`
    :param raw_text: Holds the actual raw text of the page, extracted from the
       data. 
    :type raw_text: string
    :param lang: The language code of the primary language in the ISO-639-1 form
       (e.g. "de" or "en"). 
    :type lang: string
    :param file: An optional (back-)reference to a PdfFile object.
    :type file: A :py:class:`PdfFile` object.
    :param verbose: Print additional information during performance when True.
       Default = True
    :type verbose: boolean

    """
    def __init__(self,
                 page_num = None,
                 page_label = None,
                 ## here, data holds a pypdf.PageObject (or None)
                 data = None,
                 raw_text = "",
                 lang = "",
                 ## can include a reference to a PdfFile object
                 file = None,
                 verbose = True):
        """Constructor method.
        """
        super(PdfPage, self).__init__(page_num,
                                      page_label,
                                      data,
                                      raw_text,
                                      lang,
                                      verbose)
        ## call this again to perform tests
        self._file = file
        self.data = data

    ########################################
    # remove data when pickling
    # RP  Tue Apr 29 12:30:09 2025

    def __getstate__(self):
        """Remove unpicklable PageObject before pickling."""
        state = self.__dict__.copy()
        state['_data'] = None  # Remove pypdf.PageObject
        return state


    ########################################

    @property
    def data(self):
        """
        Read/write property for the data of the object. 
        """
        return self._data

    @data.setter
    def data(self, val):
        """
        Set the `data` value of the object. 
        """
        ## test if data is a pypdf PageObject
        if val != None and not isinstance(val, PageObject):
            print(f"Error: The value for data is not a pypdf.PageObject, but "
                  + "a {type(val)}")
            return False
        self._data = val

    @property
    def file(self):
        """
        Read/write property. 
        """
        return self._file

    @file.setter
    def file(self, val):
        if isinstance(val, PdfFile):
            self._file = val
        else:
            print("Error: val is not of type PdfFile. ")
            return False

    ########################################

    def extract_text(self, update_text = True):
        """
        Extract text from a PDF page using direct extraction.
        Returns the text as a string.

        :param update_text: Update the text attribute with the extracted text?
        :type update_text: boolean
        :return: The retrieved text.
        :rtype: string
        
        """
        if not self.data:
            print("Error: No data.")
            return False
        
        text = self.data.extract_text()

        if update_text:
            self._raw_text = text
        
        return text



################################################################################

class PdfFile:
    """
    This is a class implementation of a PDF file.  A PDF file object is related
    to an actual PDF file (e.g. retrieved from a database entry).  Its methods
    facilitate e.g. the retrieval of data/text from the pages.

    The `data` attribute holds the :py:class:`PdfPage` objects. 

    Examples::

        ## load a PDF file and extract the content from its pages
        pdfFile = pdf.PdfFile("bajohr2024a.pdf", auto_extract=True)
        
        ## get the primary language
        print(pdfFile.lang)
        ## => "de"
        
        ## get the label from the second page (in this case a roman numeral)
        pdfFile.data[1].page_label
        ## => "II"

        ## get the text from the third page
        pdfFile.data[2].text
        

    :param file: The filepath.
    :type file: string
    :param auto_extract: Automatically extract the text from all pages in the
        file when instantiating the object? This also automatically creates
        :py:class:`PdfPage` objects for each page. Default = True
    :type auto_extract: boolean
    :param use_ocr: Use OCR by default for text extraction? Default = False
    :type ose_ocr: boolean
    :param fallback_to_ocr: If text extraction without OCR yields little text,
        fallback to OCR? Default = True
    :type fallback_to_ocr: boolean
    :param ocr_dpi: The DPI amount for OCR. Default = 300
    :type ocr_dpi: integer
    :param ocr_default_lang: The default language for OCR. Default = "eng"
    :type ocr_default_lang: string
    :param verbose: Print additional information during performance when True.
       Default = True
    :type verbose: boolean
    
    """
    def __init__(self,
                 file: str,
                 auto_extract = True,
                 use_ocr = False,
                 fallback_to_ocr = True,
                 ocr_dpi = 300,
                 ocr_default_lang = 'eng',
                 verbose=True):
        ## The filepath
        self._file = file
        ## a sha256 checksum for the file
        self._file_checksum = None
        ## The pypdf.PdfReader object
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
        self._verbose = verbose
        ########################################
        self.update()

    ########################################
    # remove pypdf objects before pickling
    # RP  Tue Apr 29 11:54:22 2025

    def __getstate__(self):
        """Customize pickling: remove unpicklable attributes."""
        state = self.__dict__.copy()
        state['_reader'] = None  # Exclude reader
        state['_number_tree'] = None
        # Remove unpicklable PageObject references from each PdfPage
        if state['_data']:
            for page in state['_data']:
                page.data = None
                
        return state

    def __setstate__(self, state):
        """Customize unpickling: restore state and update reader."""
        self.__dict__.update(state)
        if self._file:
            self.set_reader()  # Recreate PdfReader TODO
    

    ########################################
        
    @property
    def file(self):
        """The filepath to the PDF. 
        """
        return self._file

    @file.setter
    def file(self, val):
        self._file = val
        self.update()

    @property
    def file_checksum(self):
        """Checksum (SHA256) of the PDF file (read-only). 
        """
        return self._file_checksum


    @property
    def lang(self):
        """The language. 
        """
        return self._lang

    @lang.setter
    def lang(self, val):
        # fallback to "en" if no lang is set
        # TODO: is there a better solution?
        # RP  Tue Apr 29 00:55:31 2025
        if not val:
            val = "en"
        self._lang = langcodes.standardize_tag(val)
        ## also set OCR default lang (alpha3)
        self._ocr_default_lang = langcodes.get(self._lang) \
                                          .to_alpha3()
        return self._lang

    @property
    def data(self):
        """The data.
        This is a list of :py:class:`PdfPage` objects, provided the data has
        been extracted (cf. `auto_extract`). 
        """
        return self._data

    @data.setter
    def data(self, val):
        self._data = val

    @property
    def reader(self):
        """The `pypdf.PdfReader` object (read-only). 
        """
        return self._reader

    @property
    def auto_extract(self):
        """Do auto-extraction?
        """
        return self._auto_extract

    @auto_extract.setter
    def auto_extract(self, val):
        if isinstance(val, bool):
            self._auto_extract = val
        else:
            print(f"Error: '{val}' is not of type Boolean")
            return False


    @property
    def verbose(self):
        """Verbose setter/getter (bool)
        """
        return self._verbose

    @verbose.setter
    def verbose(self, val):
        self._verbose = val

    ########################################

    def set_reader(self):
        """This method sets the reader slot to the file.

        This was previously done in the update method, but since pypdf objects
        (just as the reader) cannot be pickled, we seperate this process here
        in order to be at least able to reconstruct the reader when unpickling
        a PdfFile object. 
        """
        if self._file and os.path.isfile(self._file):
            try:
                self._reader = PdfReader(self._file)
            except PdfReadError:
                print(f"Error: Invalid PDF file {self._file}")
                return False
                
            else:
                return True
        else:
            # the file does not exist
            return False
            

    def update(self):
        """Updates the instance.
        """
        ## (re-)initialize the reader object
        if not self.set_reader():
            print(f"PdfFile.update(): Error: The file '{self._file}' does not "
                  + "exist or could not be read.")
            return False
        
        ## Initialize the number tree
        self._number_tree = self._reader.trailer['/Root'] \
                                        .get('/PageLabels')
        ## calculate file checksum
        self._file_checksum = utilities.file_checksum(self._file,
                                                      algorithm = "sha256")
        ## auto-extract
        if self._auto_extract:
            self._data = self.extract_text()
        ## set (primary) language if not given
        if (self.lang == "" or not self.lang) and self.data:
            self.lang = self.get_primary_lang()
        return self

    def extract_text_without_ocr(self):
        """
        Extract text from a PDF using pypdf.
        Returns a list of PdfPage objects. 
        """
        text = []

        if self._verbose:
            print(f"NO OCR: Processing {self._file}:")

        # workaround for now (using try/catch)
        # TODO: need to update to pypdf
        # RP  Tue Apr 29 01:13:42 2025
        try:
            pages = self.reader.pages
        except KeyError as e:
            print("Error with PDF...")
            return ""
        for i, page in enumerate(pages):
            if self._verbose:
                print(f"NO OCR: Processing page {i+1}/"
                      + f"{len(self.reader.pages)}...")

            # since some pdf files might contain corrupted or encrypted data,
            # we need to use this fallback
            # RP  Tue Apr 29 14:01:01 2025
            try:
                page_text = page.extract_text()
            except Exception as e:
                print(f"Failed to extract text from page {i}: {e}. ")
                page_text = ""
            
            page_ob = PdfPage(lang = self.lang,
                              raw_text = page_text,
                              data = page,
                              file = self,
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
            if self._verbose:
                print(f"OCR: Processing {self._file}:")
                print("OCR: Converting pages to images...")
                
            images = convert_from_path(self._file,
                                       dpi=self._ocr_dpi)
            for i, image in enumerate(images):
                if self._verbose:
                    print(f"OCR: Processing page {i+1}/{len(images)}...")
                    
                page_text = pytesseract.image_to_string(
                    image,
                    lang = self._ocr_default_lang)
                page_ob = PdfPage(page_num = i,
                                  page_label = self.get_page_label(i),
                                  raw_text = page_text,
                                  file = self,
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

        :param page_num: The page number (zero-based) the label should be
            retrieved from.
        :type page_num: integer
        
        """
        if not self._number_tree:
            # no number tree, use page numstring instead
            return str(page_num + 1)
        
        label_tuples = self._number_tree.get_object().get('/Nums')

        if label_tuples:
        
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
                        page_label = prefix + label_func(page_num
                                                             - start_index)
        # edge case: non label mapping defined
        # RP  Tue Apr 29 00:52:36 2025
        else:
            page_label = str(1 + page_num)
            
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

    def get_page(self, page_index):
        """Returns the `PdfPage` object for the page at index (zero-based).
        """
        if page_index < len(self.data):
            return self.data[page_index]
        else:
            return False

    

        
################################################################################
## EOF pdf.py
