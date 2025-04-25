"""This module implements functionality for a (text) pool.

A text pool is a collection of annotated/tokenized, text-holding objects (e.g.
PdfFiles, TxtFiles) and can be generated from a BibTexDatabase object.  Its main
purpose is to facilitate interacting with a corpus of texts and the metadata
provided by the BibTex entries.

Created: 2025-04-25
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  01:56:37 Sat Apr 26 2025 CEST

"""

from random import randrange

from .pdf import PdfFile
from .txt import TxtFile

################################################################################

def random_data(ob):
    """This data getter function returns a random data item index.  See
    :py:func:`PoolItem.get_data` for details.

    """
    return randrange(0, len(ob.data))


def cycle_data(ob):
    """This data getter function returns the next data item index and also sets
    the next item index to return.  See :py:func:`PoolItem.get_data` for
    details.

    """
    this_next = ob.next_data
    # set new next index
    ob.next_data = (this_next + 1) % len(ob.data)
    # return index
    return this_next
    

class PoolItem:
    """This class implements a PoolItem.

    PoolItems are containers for metadata (e.g. retrieved from a BibTeX entry in
    a BibTexDatabase) and text holding objects (in the `data` attr),
    e.g. :py:class:`PdfFile` objects.

    They are meant to be placed into a :py:class:`Pool`.

    :param key: A (unique) key. This is most likely a BibTeX citekey.
    :type key: string
    :param meta: A dict holding metadata, most likely derived from a BibTeX
       entry.
    :type meta: dict
    :param data: A list holding one or more text holding objects (e.g. a
       :py:class:`PdfFile`).
    :type data: list
    :param default_get_data_func: The default function to retrieve a data object
       via :py:func:`get_data` (cf. :py:func:`get_data`).
       Default = None, which falls back to the default which causes `get_data`
       to always return the first element of the `data`.
    :type default_get_data_func: A function which must be a function taking the
       `PoolItem` as its argument and must return an index to the element of
       `data` which should be retrieved. Set to `None` to use the default. 

    """
    def __init__(self,
                 key,
                 meta = {},
                 data = [],
                 default_get_data_func = None):
        self.key = key
        self.meta = meta
        self.data = data
        ## the index of the next data object
        self._next_data = 0
        self.default_get_data_func = default_get_data_func

    ########################################

    @property
    def key(self):
        """Getter/setter for the key. 
        """
        return self._key
    
    @key.setter
    def key(self, val):
        if not isinstance(val, str):
            print(f"PoolItem: ERROR '{val}' is not a valid key (must be "
                  + "a string.")
            return False
        self._key = val
    
    @property
    def next_data(self):
        """Getter/setter for the next_data id.  This is an index (zero-based)
        to the next element that should be retrieved from the data list when
        using :py:func:`get_data`.  (int)
        """
        return self._next_data

    @next_data.setter
    def next_data(self, val):
        self._next_data = val % len(self._data)

    @property
    def meta(self):
        """Getter/setter for the meta dict.
        """
        return self._meta

    @meta.setter
    def meta(self, val):
        if isinstance(val, dict):
            self._meta = val
        else:
            raise ValueError("PoolItem.meta expects a dict.")

    @property
    def data(self):
        """Getter/setter for the data list.
        """
        return self._data

    @data.setter
    def data(self, val):
        if (
            isinstance(val, list)
            and all(isinstance(x, PdfFile) or isinstance(x, TxtFile)
                    for x in val)
        ):
            self._data = val
        else:
            raise ValueError("PoolItem.data must be a list of PdfFile or "
                             + "TxtFile objects. ")

    @property
    def default_get_data_func(self):
        return self._default_get_data_func

    @default_get_data_func.setter
    def default_get_data_func(self, val):
        if callable(val):
            self._default_get_data_func = val
        elif val == None:
            self._default_get_data_func = (lambda ignore: 0)
        else:
            raise ValueError("PoolItem.default_get_data_func must be None or "
                             + "a function. ")
        

    def get_data(self, func = None):
        """This function returns a single data object from the data list instead
        of the data list itself.  The `func` argument -- which must be a
        function taking the `PoolItem` as its argument and must return an index
        to the element of `data` which should be retrieved -- specifies which
        element should be returned.  By default, it always returns the first
        item of the `data` list.  There are two more functions specified, which
        could also be used: :py:func:`random_data` and :py:func:`cycle_data`.

        Example::

           # this cycles through the data by using the `cycle_data` function
           pitm.get_data(cycle_data)
        

        :param func: A function which must be a function taking the `PoolItem`
            as its argument and must return an index to the element of `data`
            which should be retrieved.  Default = None which falls back to the
            `self._default_get_data_func`. 
        :type func: function

        """
        if func is None:
            func = self._default_get_data_func
            
        next_index = func(self) % len(self.data)
        return self.data[next_index]
            
        
        
        
    
################################################################################

class Pool:
    """Implementation of the Pool class.

    A (text) Pool is a collection of annotated/tokenized, text-holding objects
    (e.g.  PdfFiles, TxtFiles) and can be generated from a BibTexDatabase
    object.  Its main purpose is to facilitate interacting with a corpus of
    texts and the metadata provided by the BibTex entries.

    The `data` of the pool is a `dict` of :py:class:`PoolItem` objects.  The
    keys of the `dict` are typically (e.g. when the `Pool` is created from a
    :py:class:`BibTexDatabase`) citation keys.

    :param data: A `dict` with an initial set of :py:class:`PoolItem` objects.
    :type data: dict

    """
    def __init__(self,
                 data = {}):
        self.data = data


    @property
    def data(self):
        """Getter/setter for the data of the `Pool`.

        This is a `dict` with :py:class:`PoolItem` objects.  Keys are usually
        citekeys. 
        """
        return self._data

    @data.setter
    def data(self, val):
        if not (
            isinstance(val, dict)
            and all(x, PoolItem) for x in val.values()
        ):
            raise ValueError("Pool: data must be a dict. all values need "
                             + "to be PoolItem instances.")

        self._data = val


    def get(self, key):
        """Get a py:class:`PoolItem` from the pool by its key. 
        """
        return self.data.get(key)

    
            

################################################################################
### EOF pool.py
