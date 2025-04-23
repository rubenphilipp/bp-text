"""
This module implements utility functions.

Created: 2025-03-28
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  20:45:06 Wed Apr 23 2025 CEST
"""

import hashlib
import pickle

################################################################################

def file_checksum(file_path,
                  algorithm="sha256",
                  chunk_size=8192):
    """This function creates a checksum for a file.

    :param file_path: Path to the file to be checksummed.
    :type file_path: string
    :param algorithm: The hash algorithm (e.g. "sha256", "md5", "sha1").
        Default = "sha256"
    :type algorithm: string
    :param chunk_size: The chunk size for checksum creation in Bytes.
        Default = 8192
    :type chunk_size: integer

    """
    hash_func = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            hash_func.update(chunk)

    return hash_func.hexdigest()


################################################################################

def write_pickle(obj, file_path,
                 protocol = pickle.HIGHEST_PROTOCOL):
    """This function serializes (pickles) an object and stores it in a file
    given as `file_path`.

    :param file_path: The path where to store the pickle file.  It is
       recommended to use the `.pickle` suffix. 
    :type file_path: string
    :param protocol: The pickle protocol. Default = `pickle.HIGHEST_PROTOCOL`
    :type protocol: integer
    """
    with open(file_path, "wb") as f:
        pickle.dump(obj, f, protocol)


def read_pickle(file_path):
    """Read a serialized (pickled) file and return the data it holds.

    :param file_path: The path to the serialized data.
    :type file_path: string
    """
    data = None
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data




################################################################################
## EOF utilities.py
