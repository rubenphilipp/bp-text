"""
This module implements database functionality.  Its main purpose is to read
from a BibTeX file (as database).

Created: 2025-03-23
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  00:53:34 Mon Mar 24 2025 CET
"""

import abc
import os
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
            parse_keywords = True,
            parse_files = True):
        self._data = None
        self.parse_keywords = parse_keywords  
        self.parse_files = parse_files
        if not file_path:
            raise ValueError("File path must be provided.")
        
        self.load(file_path,
                  parse_files = self.parse_files,
                  parse_keywords = self.parse_keywords)
            
    def load(self,
             file_path:str,
             parse_keywords = True,
             parse_files = True):
        """Load and parse a BibTeX file."""
        if not os.path.exists(file_path):  # Check if the file exists
            print(f"Error: The file {file_path} does not exist.")
            return
        self._data = bibtexparser.parse_file(file_path)
        for entry in self._data.entries:
            data_fl = entry.fields_dict.get('file')
            data_kw = entry.fields_dict.get('keywords')
            ## split the keywords (by ",") and files (by ";")
            if(self.parse_keywords and data_kw != None):
                entry['keywords'] = data_kw.value.split(",")
            if(self.parse_files and data_fl != None):
                entry['files'] = data_fl.value.split(";")
        return self._data

    def get_nth_entry(self, n):
        return self._data.entries[n]
        
    

################################################################################
## EOF db.py
