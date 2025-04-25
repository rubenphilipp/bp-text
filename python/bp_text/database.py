"""
This module implements database functionality.  Its main purpose is to read
from a BibTeX file (as database).

Created: 2025-03-23
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  01:28:30 Sat Apr 26 2025 CEST
"""

import abc
import os
import re
from pathlib import Path
import bibtexparser

from . import utilities
from . import __version__
from . import txt
from . import pdf

################################################################################


class Database(abc.ABC):
    """An abstract superclass for a database. 

    """
    @abc.abstractmethod
    def load(self, file_path: str):
        """Load a database from a file.

        :param file_path: The path to the database file.
        :type file_path: string
        """
        pass


################################################################################


class BibTexDatabase(Database):
    """Implementation of a BibTeX database.  This class provides the user with
    various methods to interact with the stored data.

    NB: This class is limited to read-only use.  In order to modify the contents
    of the actual database it is recommended to use a specialized software (e.g.
    BibDesk).

    The `data` attribute contains the parsed data.

    Example::

        database = database.BibTexDatabase("db.bib")
        database.entries["adorno1960"].get("file").value

    :param file_path: The path to the .bib file.
    :type file_path: string
    :param split_keywords: When true, split all keywords in the `keywords`
        field into a list, assuming they are separated by a comma (",").
        Default = True
    :type split_keywords: boolean
    :param split_files: When true, split all files in the `file` field into a
        list, assuming they are separated by a semicolon (";").  Default = True
    :type split_files: boolean
    """
    def __init__(
            self,
            file_path: str,
            split_keywords = True,
            split_files = True):
        self._data = None
        if not file_path:
            raise ValueError("File path must be provided.")
        
        self.load(file_path,
                  split_files = split_files,
                  split_keywords = split_keywords)
        self._base_path = Path(file_path).parent

    @property
    def data(self):
        """The parsed data.  """
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @property
    def entries(self):
        """The database entries as a `dict`.
        
        Example::

           # get the value of the file field of the entry with the citation
           # key "heinlein2020"
           db.entries["heinlein2020"].fields_dict["file"].value
           # => ['heinlein2020 - katastrophen.pdf']
           
           # ...which can also be expressed in a shorter form
           db.entries["heinlein2020"].get("file").value
        """
        return self._data.entries_dict

    def load(self,
             file_path:str,
             split_keywords = True,
             split_files = True):
        """Load and parse a BibTeX file.

        :param file_path: The path to the BibTeX file.
        :type file_path: string
        :param split_keywords: When true, split all keywords in the `keywords`
            field into a list, assuming they are separated by a comma (",").
            Default = True
        :type split_keywords: boolean
        :param split_files: When true, split all files in the `file` field into
            a list, assuming they are separated by a semicolon (";").
            Default = True
        :type split_files: boolean
        """
        if not os.path.exists(file_path):  # Check if the file exists
            print(f"Error: The file {file_path} does not exist.")
            return
        self._data = bibtexparser.parse_file(file_path)
        if split_keywords:
            self.split_fields_by(field = "keywords", separator=",")
        if split_files:
            self.split_fields_by(field = "file", separator=";")
        return self._data

    def split_fields_by(self,
                        field: str,
                        separator = ";"):
        """Splits the data/value of all entries in the database (destructively)
        of the given field (e.g. "keywords") by a given separator.

        :param field: The field name (e.g. "keywords").
        :type field: string
        :param separator: The separating character. Default = ";"
        :type separator: string
        """
        ## sanity checks
        if not field:
            raise ValueError("A field must be provided.")
        if not separator:
            raise ValueError("A seperator must be provided.")
        for entry_key, entry in self.data.entries_dict.items():
            field_data = entry.fields_dict.get(field)
            if field_data:
                field_value = field_data.value
                if isinstance(field_value, str):
                    field_data.value = field_value.split(separator)
                else:
                    print(f"Field '{field}' is already a list and thus cannot "
                          + "be split. ")
        return self.data

    def get_entry_by_key(self, key):
        """Get a specific entry by citation-key in the db.

        This is an alias to `self.entries.get(key)`.

        :param key: The citation key (e.g. "@adorno1960") to look for. 
        :type key: string
        """
        return self.entries.get(key)

    def find_entries(self, field: str, search: str):
        """Find entries matching the search string in the given field.

        :param field: The field name (e.g. "keywords").
        :type field: string
        :param search: The search string.
        :type search: string
        :return: A list with items of `<class 'bibtexparser.model.Entry'>`
        :rtype: list

        """
        matches = []

        for entr in self.entries:
            entry = self.entries[entr]
            if field in entry.fields_dict:
                value = entry.get(field)

                # If the value is a list, check if search is in the list
                if isinstance(value, list):
                    if search.lower() in [str(item).lower() for item in value]:
                        matches.append(entry)
                # If the value is not a list, do a standard string comparison
                else:
                    if search.lower() in str(value).lower():
                        matches.append(entry)

        return matches
        
    def get_nth_entry(self, n):
        """Get the nth entry in the database.

        :param n: Index (zero-based) of the entry in the database.
        :type n: integer
        """
        entries = self.data.entries
        if (n < len(entries)):
            return entries[n]
        else:
            print(f"Entry '{n}' does is not within the list range.")

    def make_pool(self,
                  cache = False,
                  default_get_data_func = None,
                  pdf_auto_extract = True,
                  pdf_use_ocr = False,
                  pdf_fallback_to_ocr = True,
                  pdf_ocr_dpi = 300,
                  pdf_ocr_default_lang = 'eng',
                  verbose = True):
        """Create a :py:class:`Pool` with :py:class:`PoolItem` objects derived
        from the `BibTexDatabase` entries and the documents linked in the `file`
        fields.

        While creating the `Pool`, this methods also instantiates text holding
        objects for the data linked in `file`.  This could be
        :py:class:`PdfFile` (for PDFs) or :py:class:`TxtFile` (for TXTs)
        objects.  When a cache directory is given, this method will try to
        search for pickled objects in the respective directory and tries to load
        them in order to avoid recomputing expensive NLP analyses
        (cf. :py:class:`Text`).  The search pattern for cache files is
        `[citekey]-[file_checksum]-[bp_text.__version__].pickle`.  Besides
        searching for existing cached files, new cache files will automatically
        be created items not found in the cache directory.

        The paths in `file` are either relative or absolute.  When relative,
        they are converted to absolute paths relative to the location of the
        database file (cf. `self._base_path). 

        :param cache: When `False` caching is disabled. If a directory string
           is given, use this for caching (see above).
        :type cache: False or string
        :param default_get_data_func: This sets the default function to get data
           from a :py:class:`PoolItem` object (cf. respective doc in this
           class).
        :type default_get_data_func: A function which must be a function taking
           the `PoolItem` as its argument and must return an index to the
           element of `data` which should be retrieved. Set to `None` to use the
           default.
        :param pdf_auto_extract: Automatically extract the text from all pages
           in the file when instantiating the object? This also automatically
           creates :py:class:`PdfPage` objects for each page. Default = True
        :type pdf_auto_extract: boolean
        
        :param pdf_use_ocr: Use OCR by default for text extraction? Default =
           False
        :type pdf_ose_ocr: boolean
        :param pdf_fallback_to_ocr: If text extraction without OCR yields little
           text, fallback to OCR? Default = True
        :type pdf_fallback_to_ocr: boolean
        :param pdf_ocr_dpi: The DPI amount for OCR. Default = 300
        :type pdf_ocr_dpi: integer
        :param pdf_ocr_default_lang: The default language for OCR. Default =
           "eng"
        :type pdf_ocr_default_lang: string
        :param verbose: Print additional information during performance when
           True.  Default = True
        :type verbose: boolean

        """
        ## test if cache is given and directory exists
        if cache and not os.path.isdir(cache):
            # create cache directory
            Path(cache).mkdir(parents=True, exist_ok=True)

        if cache:
            ## trailing slash
            cache = Path(cache)
        
        for key, val in self.entries.items():
            files = val.get("file")
            ## skip when no files are given
            if not files:
                continue

            ## since there are files, get the actual paths
            files = files.value

            ## process file by file
            files_ob = []
            for fl in files:
                fl_path = Path(convert_latex_umlauts(fl))

                ## if path is relative, convert it to an absolute path
                ## relative to the base dir of the database
                if not fl_path.is_absolute():
                    fl_path = self._base_path / fl_path
                
                ## test if file exists
                if not (fl_path.exists() and fl_path.is_file()):
                    if verbose:
                        print(f"make_pool: File '{fl_path}' does not exist. "
                              + "Skipping.")
                    continue

                ## get file type
                fl_suffix = fl_path.suffix.lower()
                if not (fl_suffix == ".pdf" or fl_suffix == ".txt"):
                    if verbose:
                        print(f"make_pool: File '{fl_path}' is neither a PDF "
                              + "nor a TXT. Skipping. ")
                    continue
                
                ## get cache-path
                if cache:
                    fl_checksum = utilities.file_checksum(fl_path,
                                                          algorithm="sha256")
                    cachefile = cache / (key + "-" + fl_checksum + "-"
                                         + __version__ + ".pickle")
                    
                ## load from cache if exists
                if cache and (cachefile.exists() and cachefile.is_file()):
                    if verbose:
                        print(f"make_pool: Found cache for '{fl_path}'. "
                              + "Loading...")
                    files_ob.append(utilities.read_pickle(cachefile))
                else:
                    if fl_suffix == ".txt":
                        if verbose:
                            print(f"make_pool: Processing '{fl_path}'...")
                        fl_ob = txt.TxtFile(file=fl_path)
                    elif fl_suffix == ".pdf":
                        if verbose:
                            print(f"make_pool: Processing '{fl_path}'...")
                        fl_ob = pdf.PdfFile(
                            file=fl_path,
                            auto_extract = pdf_auto_extract,
                            use_ocr = pdf_use_ocr,
                            fallback_to_ocr = pdf_fallback_to_ocr,
                            ocr_dpi = pdf_ocr_dpi,
                            ocr_default_lang = pdf_ocr_default_lang,
                            verbose = verbose)
                    else:
                        if verbose:
                            print("make_pool: File obj could not be created "
                                  + f" for '{fl_path}'. Skipping.")
                        continue
                    ## append to files
                    files_ob.append(fl_ob)
                    ## cache when desired
                    if cache:
                        if verbose:
                            print(f"make_pool: Caching '{cachefile}'...")
                        utilities.write_pickle(fl_ob, cachefile)
                    

        

################################################################################

################################################################################
## convert latex umlauts (esp. in file) to ascii umlauts
def convert_latex_umlauts(text):
    """Convert LaTeX umlauts to ASCII umlauts.

    :param text: Text to convert.
    :type text: string
    """
    # Dictionary mapping LaTeX umlaut sequences to Unicode characters
    umlaut_map = {
        '{\\"a}': 'ä', '{\\"A}': 'Ä',
        '{\\"o}': 'ö', '{\\"O}': 'Ö',
        '{\\"u}': 'ü', '{\\"U}': 'Ü',
        '{\\"e}': 'ë', '{\\"E}': 'Ë',
        '{\\"i}': 'ï', '{\\"I}': 'Ï',
        '{\\ss}': 'ß'
    }
    
    # Replace each LaTeX sequence with its Unicode equivalent
    for latex_seq, unicode_char in umlaut_map.items():
        text = text.replace(latex_seq, unicode_char)
    
    # Also handle alternate forms like \"a
    alt_pattern = r'\\"([aoueiAOUEI])'
    text = re.sub(alt_pattern,
                  lambda m: umlaut_map.get('{\\"' + m.group(1) + '}',
                                           m.group(0)), text)
    return text

################################################################################
## EOF db.py
