"""
This module implements the page class.

Created: 2025-03-28
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  14:33:01 Fri Apr 25 2025 CEST
"""

from abc import ABC, abstractmethod


import roman
import langcodes

from . import language
from . import utilities
from . import text

################################################################################

class Page(ABC):
    """Abstract base class for a page.

    Note: The `text` attribute holds a :py:class:`Text` object containing
    tokenized text derived from the `raw_text`.  

    :param page_num: The page number (zero-based) of the page in the related
        file.
    :type page_num: int
    :param page_label: The actual page label of the page.  Its value and meaning
        differs from the page_num as it is related to the actual page numbering
        e.g. in a document.  Thus, it could also be a roman numeral or be
        counted from a starting index different from 0. 
    :type page_label: string
    :param data: Holds page data.
    :type data: undefined
    :param raw_text: Holds the actual raw text of the page, extracted from the
       data. 
    :type raw_text: string
    :param lang: The language code of the primary language in the alpha3/ISO
        639-1 form.
    :type lang: string
    :param tagger_pos: A Flair POS tagger object. `None` uses the default
       tagger, `False` skips POS tagging. 
       Default = None
    :type tagger_pos: None or a Flair POS tagger object of type
       <class 'flair.models.sequence_tagger_model.SequenceTagger'>.
    :param tagger_ner: A Flair NER tagger object. `None` uses the default
       tagger, `False` skips NER tagging.
       Default = text_tagger_ner
    :type tagger_ner: None or a Flair NER tagger object of type
       <class 'flair.models.sequence_tagger_model.SequenceTagger'>.
    :param verbose: Print additional information during performance when True.
       Default = False
    :type verbose: boolean
    
    """
    def __init__(self,
                 page_num = None,
                 page_label = None,
                 data = None,
                 raw_text = "",
                 lang = "",
                 tagger_pos = None,
                 tagger_ner = None,
                 verbose = False):
        ## the page number / index
        self._page_num = page_num
        ## the page number (number) label
        ## this might differ from the actual page number e.g.
        ## when sections of a document are labeled with roman
        ## numerals
        self._page_label = page_label
        ## additional data
        self._data = data
        ## the slot for the Text object (empty for now)
        self._text = None
        self._tagger_pos = tagger_pos
        self._tagger_ner = tagger_ner
        ## the raw text
        self._raw_text = raw_text
        ## the primary language of the page's content
        self._lang = lang
        ## verbose
        self._verbose = verbose
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
    def raw_text(self):
        return self._raw_text

    @raw_text.setter
    def raw_text(self, val):
        if isinstance(val, str):
            self._raw_text = val
        else:
            print("Error: value for raw_text is not a String.")
        self.update()

    @property
    def text(self):
        """Getter for the Text (read-only).
        """
        return self._text

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, val):
        if val != "":
            self._lang = langcodes.standardize_tag(val)
        else:
            self._lang = ""


    @property
    def verbose(self):
        """Verbose setter/getter (bool)
        """
        return self._verbose

    @verbose.setter
    def verbose(self, val):
        self._verbose = val

    ########################################

    def update(self):
        """Updates the instance. 
        """
        ## detect and update language
        self.detect_lang(set_lang = True)
        # create the text object
        if self._verbose:
            print("Page.update(): Initializing text object. ")
        self._text = text.Text(self._raw_text, lang=self.lang,
                               tagger_pos = self._tagger_pos,
                               tagger_ner = self._tagger_ner)

    def detect_lang(self, set_lang = True):
        """Detect the primary language of text in the page.

        :param set_lang: When true, automatically set the language attribute of
           the page. Default = True.
        :type set_lang: boolean
        """
        lang = None
        detector = language.LanguageDetector().detector
        if self._raw_text != "":
            lang = detector.detect_language_of(self._raw_text)
        else:
            return False
        langcode = lang.iso_code_639_1.name
        if set_lang:
            self.lang = langcode
        return langcode

    def count_words(self):
        """Counts the words in the text.

        :return: The number of words in the text.
        :rtype: integer
        """
        return len(self._raw_text.split())



################################################################################
## EOF page.py
