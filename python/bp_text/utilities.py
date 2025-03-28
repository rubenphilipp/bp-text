"""
This module implements utility functions.

Created: 2025-03-28
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  15:16:42 Fri Mar 28 2025 CET
"""

import hashlib
import pickle

################################################################################

def file_checksum(file_path,
                  algorithm="sha256",
                  chunk_size=8192):
    """
    This file creates a checksum for a file.

    - chunk_size: the chunk size in Bytes.
    - file_path: the path to the file.
    - algorithm: the hash algorihm e.g. sha256, md5, sha1 etc.)
    """
    hash_func = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            hash_func.update(chunk)

    return hash_func.hexdigest()


################################################################################

def write_pickle(obj, file_path,
                 protocol = pickle.HIGHEST_PROTOCOL):
    """Serializes/pickles an object to the given file path"""
    with open(file_path, "wb") as f:
        pickle.dump(obj, f, protocol)


def read_pickle(file_path):
    """Reads a pickle file and returns the data it holds."""
    data = None
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data




################################################################################
## EOF utilities.py
