"""
This module implements (text) source files.  These are generated from a source
file (e.g. TXT, PDF).  

Created: 2025-03-27
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  15:16:00 Thu Mar 27 2025 CET
"""

import os
import sys
import re
from pathlib import Path
from lingua import Language, LanguageDetectorBuilder
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

from . import database
from . import textdata

################################################################################

languages = [Language.ENGLISH, Language.FRENCH,
             Language.GERMAN, Language.SPANISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

################################################################################

class Text:
    def __init__(
            self,
            file: str,
            lang = ""):
        ## data contains the actual text
        self._data = None
        ## filepath in data dir
        self._lang = lang
        self._file = file
        ## extract data from file
        self.extract_text_from_file(set_data = True)
        ## get language (if not specified)
        if self._lang == "":
            self.detect_lang(set_lang = True)


    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, val: str):
        if not isinstance(val, str):
            raise ValueError("Value must be of type string.")
        self._lang = val.upper()

    @property
    def file(self):
        return self._file

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        self._data = val



    def detect_lang(self, set_lang = False):
        if self.data == "":
            print(f"Error: No text in the data attribute.")
            return False
        lang = detector.detect_language_of(self.data)
        detected_lang = lang.iso_code_639_1.name
        if set_lang:
            self.lang = detected_lang
        return detected_lang

    def extract_text_from_file(self, set_data = True):
        file = self._file
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".txt":
            with open (file, "r") as fl:
                text = fl.read()
        elif file_extension == ".pdf":
            text = textdata.extract_text_from_pdf(file)
        else:
            print(f"Error: No text found")
            text = "" # replace with return when inside function
        if set_data:
            self.data = text
            return True
        else:
            return text


################################################################################
## EOF source.py
