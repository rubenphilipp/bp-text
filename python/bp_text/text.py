"""This module implements the text class.

A text is at first a string containing information in a given language.  This
text module uses Flair to split the text into sentences and tokenizes them.
It uses various algorithms to e.g. detect parts of speech or entities which can
be later used for analysis or text-production.

Created: 2025-04-24
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  19:41:19 Fri Apr 25 2025 CEST

"""

from functools import lru_cache
import os

import spacy
import subprocess

from . import language

# from flair.tokenization import SegtokTokenizer
# from flair.splitter import SegtokSentenceSplitter
# from flair.nn import Classifier

################################################################################
### spacy

#: the default spacy models for a given language
LANG_SPACY_MODELS = {
    'en': 'en_core_web_sm',
    'de': 'de_core_news_sm',
    'fr': 'fr_core_news_sm',
    'es': 'es_core_news_sm',
    'it': 'it_core_news_sm',
    'pt': 'pt_core_news_sm',
    'nl': 'nl_core_news_sm',
    'pl': 'pl_core_news_sm',
    'sv': 'sv_core_news_sm',
}

#: Helper to cache the spacy modles
@lru_cache(maxsize=5)  # adjust based on number of language models you use
def get_nlp(model_name: str):
    if model_name:
        try:
            return spacy.load(model_name)
        except OSError:
            print(f"Model '{model_name}' not found. "
                  + "Attempting to download...")
            # download the model if it does not exist
            subprocess.run(["python", "-m", "spacy", "download",
                            model_name])
            return spacy.load(model_name)
    else:
        return False


################################################################################

class Text:
    """This is a class implementation of a Text object.  A text holds a natural
    language text as a string and additionally contains segmented and analysed
    data derived from the text.  The text is tokenized (using spaCy) and
    analyzed e.g. for parts of speech or entities.  By default, Text uses
    Flair's most versatile models (e.g.  'pos-multi' for POS tagging and
    'ner-large' for NER tagging).  While introducing some overhead on loading,
    this comes with the advantage of being able to more precisely analyse
    multilingual text.

    Note: The `doc` contains the actual segmented text. 

    :param text: The text to be used as a basis for the analysis.
    :type text: string
    :param lang: The primary language of the text as a ISO 639-1 code.
       Default = "en"
    :type lang: string

    """
    def __init__(self,
                 text = "",
                 lang = "en"):
        self._text = text
        self._lang = lang
        self._doc = None
        
        self.update()

    @property
    def text(self):
        """Getter/setter for text (string).
        
        Changing the text also causes re-generation of the sentence analyses.
        """
        return self._text

    @text.setter
    def text(self, val):
        if isinstance(val, str):
            self._text = val
        else:
            print("Error: value for text is not a String.")

        self.update()

    @property
    def doc(self):
        """Getter for the doc (i.e. the tokenized and analysed elements
        of the text). Read-only.
        """
        return self._doc
    

    def update(self):
        """Update the instance.

        This also method also performs the text segmentation and analysis. 
        """
        # sanity checks
        if not isinstance(self._text, str):
            print("Error: Text.text is not a string.")
            return False

        ## load proper model
        model_name = LANG_SPACY_MODELS.get(self._lang)
        
        ## perform analysis
        nlp = get_nlp(model_name)
        if nlp == False:
            print("Text.update(): ERROR. No spaCy model for language "
              + f"'{self._lang}' in LANG_SPACY_MODELS. ")
            return False
        
        doc = nlp(self._text)
        self._doc = doc

        return True


################################################################################
### EOF text.py
