"""
This module contains functionality dealing with languages (e.g. detection).

Created: 2025-03-27
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  20:01:33 Fri Mar 28 2025 CET
"""

from lingua import Language, LanguageDetectorBuilder

################################################################################

## globals
## the default languages for detection
default_languages = [Language.ENGLISH, Language.FRENCH,
             Language.GERMAN, Language.SPANISH]

class LanguageDetector:
    """
    A language detector. 
    """
    def __init__(self,
                 languages = default_languages):
        self._languages = languages
        self._detector = None
        ## init
        self.update()


    @property
    def languages(self):
        return self._languages

    @languages.setter
    def languages(self, langList):
        if isinstance(langList, list) \
           and all( isinstance(elem, Language)
                    for ele in langList ):
            self._languages = langList
        else:
            print("Error: languages must be a list of Language objects.")
            return False
        ## update detector
        self.update()

    @property
    def detector(self):
        return self._detector

    ########################################

    def update(self):
        ## instantiate detector
        self._detector = LanguageDetectorBuilder \
            .from_languages(*self._languages).build()




################################################################################
## EOF language.py
