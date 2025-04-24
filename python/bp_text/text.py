"""This module implements the text class.

A text is at first a string containing information in a given language.  This
text module uses Flair to split the text into sentences and tokenizes them.
It uses various algorithms to e.g. detect parts of speech or entities which can
be later used for analysis or text-production.

Created: 2025-04-24
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  23:45:25 Thu Apr 24 2025 CEST

"""

import os

from flair.tokenization import SegtokTokenizer
from flair.splitter import SegtokSentenceSplitter
from flair.nn import Classifier

################################################################################
### Flair NLP objects
### NB: loading might take a while here

# Globals, but uninitialized
_text_splitter = None
_text_tagger_pos = None
_text_tagger_ner = None

def get_text_splitter():
    global _text_splitter
    if _text_splitter is None:
        _text_splitter = SegtokSentenceSplitter()
    return _text_splitter

def get_pos_tagger():
    global _text_tagger_pos
    if _text_tagger_pos is None:
        _text_tagger_pos = Classifier.load('pos-multi')
    return _text_tagger_pos

def get_ner_tagger():
    global _text_tagger_ner
    if _text_tagger_ner is None:
        _text_tagger_ner = Classifier.load('ner-large')
    return _text_tagger_ner


################################################################################

class Text:
    """This is a class implementation of a Text object.
    A text holds a natural language text as a string and additionally contains
    segmented and analysed data derived from the text.  The text is tokenized
    into sentences (using Flair) and analyzed e.g. for parts of speech or
    entities.  By default, Text uses Flair's most versatile models (e.g.
    'pos-multi' for POS tagging and 'ner-large' for NER tagging).  While
    introducing some overhead on loading, this comes with the advantage of
    being able to more precisely analyse multilingual text.

    :param text: The text to be used as a basis for the analysis.
    :type text: string
    :param lang: The primary language of the text as a ISO 639-1 code.
       Default = "en"
    :type lang: string
    :param splitter: A Flair sentence splitter object. None uses the default
       splitter. 
       Default = None
    :type splitter: None or <class 'flair.splitter.SegtokSentenceSplitter'> or
       similar.
    :param tagger_pos: A Flair POS tagger object. None uses the default tagger.
       Default = None
    :type tagger_pos: None or a Flair POS tagger object of type
       <class 'flair.models.sequence_tagger_model.SequenceTagger'>.
    :param tagger_ner: A Flair NER tagger object. None uses the default tagger.
       Default = text_tagger_ner
    :type tagger_ner: None or a Flair NER tagger object of type
       <class 'flair.models.sequence_tagger_model.SequenceTagger'>.
    """
    def __init__(self,
                 text = "",
                 lang = "en",
                 splitter = None,
                 tagger_pos = None,
                 tagger_ner = None):
        self._text = text
        self._lang = lang
        self._sentences = None
        
        if not splitter:
            self._splitter = get_text_splitter()
        else:
            self._splitter = splitter
        
        if not tagger_pos:
            self._tagger_pos = get_pos_tagger()
        else:
            self._tagger_pos = tagger_pos

        if not tagger_ner:
            self._tagger_ner = get_ner_tagger()
        else:
            self._tagger_ner = tagger_ner
            
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
    def sentences(self):
        """Getter for the sentences (i.e. the tokenized and analysed elements
        of the text). Read-only.
        """
        return self._sentences
    

    def update(self):
        """Update the instance.

        This also method also performs the text segmentation and analysis. 
        """
        # sanity checks
        if not isinstance(self._text, str):
            print("Error: Text.text is not a string.")
            return False

        ## split sentences
        sentences = self._splitter.split(self._text)
        self._sentences = sentences

        ## analyse the sentences
        self._tagger_pos.predict(self._sentences)
        self._tagger_ner.predict(self._sentences)

        return True



################################################################################
### EOF text.py
