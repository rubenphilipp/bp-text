"""
This module implements functionality for TXT files. 

Created: 2025-03-29
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  22:23:58 Mon May  5 2025 CEST
"""

import os
import sys

import langcodes

from . import language
from . import utilities
from . import text

from .file import File
from .page import Page


################################################################################

class TxtFile(File):
    """Implementation of the text-file (txt) class.

    Note: While the `data` attribute holds the raw text read from the file, the
    `text` attribute holds a :py:class:`Text` object generated from the contents
    of the source file.  This object is already segmented and tokenized.

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
        super(TxtFile, self).__init__(file,
                                      data)
        self._lang = lang
        # this will be a Text object. empty for now
        self._text = None
        self.update()

    @File.file.setter
    def file(self, val):
        # call superclass's setter
        super(TxtFile, self.__class__).file.fset(self, val)
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

        Setting the data (i.e. the raw text) will also update the instace and
        re-initializes the text attribute by re-instantiating a Text-object. 
        """
        return self._data

    @File.data.setter
    def data(self, val):
        # call superclass's setter
        super(TxtFile, self.__class__).data.fset(self, val)
        self.update()

    @property
    def text(self):
        """Getter for the Text (read-only).
        """
        return self._text
    

    ########################################

    def update(self):
        """Updates the instance. 
        """
        if not os.path.isfile(self._file):
            print(f"Error: The file {self._file} does not exist. ")
            return False

        ## set data
        with open(self.file, "r") as f:
            self._data = f.read()

        ## set language
        self.lang = self.get_primary_lang()

        ## create text object
        self._text = text.Text(self._data, lang=self.lang)
        
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
