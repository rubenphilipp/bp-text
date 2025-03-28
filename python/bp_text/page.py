"""
This module implements the page class.

Created: 2025-03-28
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  21:30:11 Fri Mar 28 2025 CET
"""

from abc import ABC, abstractmethod


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
## EOF page.py
