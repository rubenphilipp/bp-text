"""
This module implements database functionality.  Its main purpose is to read
from a BibTeX file (as database).

Created: 2025-03-23
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  13:37:42 Thu Mar 27 2025 CET
"""

import abc
import os
import re
from pathlib import Path
import bibtexparser


class Database(abc.ABC):
    @abc.abstractmethod
    def load(self, file_path: str):
        """Load a database from a file."""
        pass


class BibTexDatabase(Database):
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

    @property
    def data(self):
        """Getter for data"""
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @property
    def entries(self):
        """Getter for db entries"""
        return self._data.entries_dict

    def load(self,
             file_path:str,
             split_keywords = True,
             split_files = True):
        """Load and parse a BibTeX file."""
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
        """
        Splits the data/value of all entries in the database (destructively)
        of the given field (e.g. "keywords") by a given separator.
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
        """
        Getter for a specific entry by citation key in the db.
        """
        return self.entries.get(key)

    def find_entries(self, field: str, search: str):
        """
        Find entries matching the search string in the given field.

        Return: A list with items of <class 'bibtexparser.model.Entry'>
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
        entries = self.data.entries
        if (n < len(entries)):
            return entries[n]
        else:
            print(f"Entry '{n}' does is not within the list range.")
        

################################################################################

################################################################################
## convert latex umlauts (esp. in file) to ascii umlauts
def convert_latex_umlauts(text):
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
