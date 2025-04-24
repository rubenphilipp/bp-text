"""
This module contains functionality dealing with languages (e.g. detection).

Created: 2025-03-27
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  20:45:39 Thu Apr 24 2025 CEST
"""

from lingua import Language, LanguageDetectorBuilder
import langcodes

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
################################################################################


# Table/dict to convert a BibLaTeX `langid` to a ISO-639-1 code.
biblatex_langid_to_iso = {
    "basque": "eu",
    "bulgarian": "bg",
    "catalan": "ca",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dutch": "nl",
    "american": "en",
    "USenglish": "en",
    "english": "en",
    "british": "en",
    "UKenglish": "en",
    "canadian": "en",
    "australian": "en",
    "newzealand": "en",
    "estonian": "et",
    "finnish": "fi",
    "french": "fr",
    "german": "de",
    "austrian": "de",
    "swissgerman": "de",
    "ngerman": "de",
    "naustrian": "de",
    "nswissgerman": "de",
    "greek": "el",
    "magyar": "hu",
    "hungarian": "hu",
    "icelandic": "is",
    "italian": "it",
    "latvian": "lv",
    "lithuanian": "lt",
    "marathi": "mr",
    "norsk": "no",
    "nynorsk": "nn",
    "polish": "pl",
    "brazil": "pt",
    "portuguese": "pt",
    "portuges": "pt",
    "romanian": "ro",
    "russian": "ru",
    "serbian": "sr",
    "serbianc": "sr",
    "slovak": "sk",
    "slovene": "sl",
    "slovenian": "sl",
    "spanish": "es",
    "swedish": "sv",
    "turkish": "tr",
    "ukrainian": "uk"
}

# Table/dict to convert an ISO-639-1 code to a BibLaTeX langid. 
iso_to_biblatex_langid = {
    'eu': 'basque',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'ngerman',
    'el': 'greek',
    'hu': 'hungarian',
    'is': 'icelandic',
    'it': 'italian',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'mr': 'marathi',
    'no': 'norsk',
    'nn': 'nynorsk',
    'pl': 'polish',
    'pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'sr': 'serbian',
    'sk': 'slovak',
    'sl': 'slovenian',
    'es': 'spanish',
    'sv': 'swedish',
    'tr': 'turkish',
    'uk': 'ukrainian'}

def langid_to_iso_639_1(langid, fallback="en"):
    """Standardize (i.e. convert to ISO-639-1) a Bib(La)TeX `langid` (see
    BibLaTeX documentation for a list of supported langids,
    https://ctan.org/pkg/biblatex).  If no matches are found, it falls back to
    the given fallback variable and prints a notice.  If no fallback is
    specified, it returns None and prints a notice. 

    Example::

       langid_to_iso_639_1("ngerman")
       # => 'de'
    
    :param langid: The langid to standardize/parse.
    :type langid: string
    :param fallback: Any string (preferably an ISO-639-1 code) the function
       should fall back to in the case no matching translation is found.
       Default = "en"
    :type fallback: string

    """
    result = biblatex_langid_to_iso.get(langid)
    if result:
        return result
    elif fallback:
        print(f"langid '{langid}' not found. Falling back to '{fallback}'.")
        return fallback
    else:
        print(f"langid '{langid}' not found. No fallback specified.")
        return None

def iso_639_1_to_langid(iso_code, fallback="english"):
    """The inverse of :py:func:`langid_to_iso_639_1`.  Converts an ISO-639-1
    code to a BibLaTeX `langid`.

    :param iso_code: The ISO-639-1 code (e.g. "de") to convert. 
    :type iso_code: string
    :param fallback: The fallback language to return if no translation found
       in the translation table. Should be a valid BibLaTeX langid (cf.
       BibLaTeX documentation). Default = "english"
    :type fallback: string
    """
    result = iso_to_biblatex_langid.get(iso_code)
    if result:
        return result
    elif fallback:
        print(f"no langid found for iso_code '{iso_code}'. " +
              f"Falling back to '{fallback}'.")
        return fallback
    else:
        print(f"no langid found for iso_code '{iso_code}'. " +
              "No fallback specified.")
        return None


def convert_langcode(langcode, inFormat="langid", outFormat="iso_code_639_1"):
    """Convert a language code to a different form.  This could for example
    be used to translate a Bib(La)TeX `langid` to an ISO-639-3 code (or vice
    versa).

    Possible in- and out-formats are:
    
    * `langid`: a Bib(La)TeX `langid` (e.g. `ngerman` or `english`, cf.
       BibLaTeX documentation at https://ctan.org/pkg/biblatex)
    * `iso_code_639_1`: an ISO-639-1 code (e.g. `DE` or `EN`)
    * `iso_code_639_3`: an ISO-639-3 code (e.g. `DEU` or `ENG`)

    Example::

       convert_langcode("ngerman")
       # => 'de'
       convert_langcode("en", "iso_code_639_1", "langid")
       # => 'english'

    :param langcode: The language code to translate.
    :type langcode: string
    :param inFormat: The input format (i.e. of `langcode`).  Must be one of the
        possible in/out formats (see above).  Default = "langid"
    :type inFormat: string
    :param outFormat: The output format (i.e. of the return value). Must be one
        of the possible in/out formats (see above).  Default = "iso_code_639_3"
    :type outFormat: string
    :return: The converted langcode in the `outFormat`.
    :rtype: string
    
    """
    if inFormat == outFormat:
        print("convert_langcode: inFormat is the same as outFormat. Ignoring.")

    if inFormat == "langid":
        iso1 = langid_to_iso_639_1(langcode)
        if outFormat == "iso_code_639_3":
            return langcodes.Language.get(iso1).to_alpha3()
        elif outFormat == "iso_code_639_1":
            return iso1
        else:
            print(f"convert_langcode: Invalid outFormat '{outFormat}'.")
            return None
    elif inFormat == "iso_code_639_1":
        if outFormat == "iso_code_639_3":
            return langcodes.Language.get(langcode).to_alpha3()
        elif outFormat == "langid":
            return iso_639_1_to_langid(langcode)
        else:
            print(f"convert_langcode: Invalid outFormat '{outFormat}'.")
            return None
    elif inFormat == "iso_code_639_3":
        iso1 = langcodes.standardize_tag(langcode)
        if outFormat == "iso_code_639_1":
            return iso1
        elif outFormat == "langid":
            return iso_639_1_to_langid(iso1)
        else:
            print(f"convert_langcode: Invalid outFormat '{outFormat}'.")
            return None
        
        

################################################################################
## EOF language.py
