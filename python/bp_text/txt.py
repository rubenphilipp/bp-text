"""
This module implements functionality for TXT files. 

Created: 2025-03-29
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  17:39:37 Wed Apr 23 2025 CEST
"""

import os
import sys

import langcodes

from . import language
from . import utilities

################################################################################

class TxtFile:
    """Implementation of the text-file (txt) class.

    Example::

        ## instantiate the text file object and read its contents
        text = txt.TxtFile("something.txt")
        ## get the primary language
        print(text.lang)
        ## => "en"

    :param file: The path to the text file.
    :type file: string
    :param lang: The language of the text file (e.g. "en", "de" etc.).
    :type lang: string
    :param data: The content of the text file. This will be automatically set
        by reading the data from the file(-path).
    :type data: string
    """
    def __init__(self,
                 file: str,
                 lang = "",
                 data = None):
        self._file = file
        self._lang = lang
        self._data = data
        ## a sha256 checksum for the file
        self._file_checksum = None
        self.update()


    @property
    def file(self):
        """Getter/setter for the file-path. 
        """
        return self._file

    @file.setter
    def file(self, val):
        self._file = val
        self.update()

    @property
    def lang(self):
        """Getter/setter for the language. 
        """
        return self._lang

    @lang.setter
    def lang(self, val):
        self._lang = langcodes.standardize_tag(val)
        return self._lang

    @property
    def data(self):
        """Getter/setter for the data (i.e. the txtfile content). 
        """
        return self._data

    @data.setter
    def data(self, val):
        self._data = val

    @property
    def file_checksum(self):
        return self._file_checksum



    ########################################

    def update(self):
        """Updates the instance. 
        """
        if not os.path.isfile(self._file):
            print(f"Error: The file {self._file} does not exist. ")
            return False

        ## set data
        with open(self.file, "r") as f:
            self.data = f.read()

        ## calculate file checksum
        self._file_checksum = utilities.file_checksum(self._file,
                                                      algorithm = "sha256")

        ## set language
        self.lang = self.get_primary_lang()
        
        return self

    def get_primary_lang(self):
        """Detect the primary language of the text in `data` and set the
        `lang` attribute accordingly. 
        """
        if self._data == "" or self._data == None:
            print("Error: Cannot detect language. No data!")
            return False

        detector = language.LanguageDetector().detector
        lang = detector.detect_language_of(self._data)

        return lang.iso_code_639_1.name




################################################################################
## EOF txt.py
