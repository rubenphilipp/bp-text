"""
This module implements the (abstract) file (super-)class.

Created: 2025-05-05
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  22:12:00 Mon May  5 2025 CEST
"""

from abc import ABC, abstractmethod

import os

from . import utilities

################################################################################


class File(ABC):
    """Abstract base class for a file.

    :param file: The filepath.
    :type file: string
    :param data: The data of the file (optional). This is esp. useful when
        handling files containing text.
    :type data: any
    :param verbose: Print extra information when True.
    :type verbose: boolean
    """
    def __init__(self,
                 file: str,
                 data = None,
                 verbose = False):
        ## the filepath
        self._file = file
        ## the data
        self._data = data
        ## verbose?
        self._verbose = verbose
        ## checksum
        self._file_checksum = None
        self.update()


    ########################################

    @property
    def file(self):
        """Getter/setter for the file attribute.
        """
        return self._file

    @file.setter
    def file(self, val):
        self._file = val
        # update e.g. the checksum
        self.update()

    @property
    def data(self):
        """Getter/setter for the data.
        """
        return self._data

    @data.setter
    def data(self, val):
        self._data = val

    @property
    def verbose(self):
        """Getter/setter for verbose (bool).
        """
        return self._verbose

    @verbose.setter
    def verbose(self, val):
        self._verbose = val

    @property
    def file_checksum(self):
        """Get the file checksum (sha256). Read-only.
        """
        return self._file_checksum

    ########################################

    def update(self):
        """Updates the instance.
        """
        ## probe file
        if not os.path.exists(self.file):
            print(f"File.update(): File '{self.file}' does not exist. ")
            return False
        ## calculate file checksum
        self._file_checksum = utilities.file_checksum(self._file,
                                                      algorithm = "sha256")
        return self
        
        

################################################################################
## EOF file.py
