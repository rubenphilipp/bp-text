"""
This module contains functionality dealing with languages (e.g. detection).

Created: 2025-03-27
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  17:16:42 Wed Apr 23 2025 CEST
"""

from lingua import Language, LanguageDetectorBuilder

################################################################################

## globals
## the default languages for detection
#: The default languages used by the detection algorithm.
default_languages = [Language.ENGLISH, Language.FRENCH,
             Language.GERMAN, Language.SPANISH]

class LanguageDetector:
    """A language detector.

    :param languages: A list containing all languages (cf. `lingua.Language`)
        to consider. Default = :any:`default_languages`
    :type languages: list of `lingua.Language` objects. 
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
        """This is the actual detector object to use for detection.

        Example::
        
           detector = language.LanguageDetector().detector
           detector.detect_language_of("Hallo Welt")
        
        """
        return self._detector

    ########################################

    def update(self):
        """Update the instance.
        """
        ## instantiate detector
        self._detector = LanguageDetectorBuilder \
            .from_languages(*self._languages).build()




################################################################################
## EOF language.py
