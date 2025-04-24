"""This module implements the text class.

A text is at first a string containing information in a given language.  This
text module uses Flair to split the text into sentences and tokenizes them.
It uses various algorithms to e.g. detect parts of speech or entities which can
be later used for analysis or text-production.

Created: 2025-04-24
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  23:18:24 Thu Apr 24 2025 CEST

"""

import os

from flair.tokenization import SegtokTokenizer
from flair.splitter import SegtokSentenceSplitter
from flair.nn import Classifier

################################################################################
### Flair NLP objects
### NB: loading might take a while here

text_splitter = SegtokSentenceSplitter()
text_tagger_pos = Classifier.load('pos-multi')
text_tagger_ner = Classifier.load('ner-large')


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
    :param splitter: A Flair sentence splitter object.
       Default = `text_splitter`
    :type splitter: <class 'flair.splitter.SegtokSentenceSplitter'> or
       similar.
    :param tagger_pos: A Flair POS tagger object. Default = text_tagger_pos
    :type tagger_pos: A Flair POS tagger object of type
       <class 'flair.models.sequence_tagger_model.SequenceTagger'>.
    :param tagger_ner: A Flair NER tagger object. Default = text_tagger_ner
    :type tagger_ner: A Flair NER tagger object of type
       <class 'flair.models.sequence_tagger_model.SequenceTagger'>.
    """
    def __init__(self,
                 text = "",
                 lang = "en",
                 splitter = text_splitter,
                 tagger_pos = text_tagger_pos,
                 tagger_ner = text_tagger_ner):
        self._text = text
        self._lang = lang
        self._sentences = None
        self._splitter = splitter
        self._tagger_pos = tagger_pos
        self._tagger_ner = tagger_ner
        self.update()

    

    def update(self):
        pass



################################################################################
### EOF text.py
