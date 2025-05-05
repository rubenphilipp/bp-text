"""This module implements the TextFragment class.

A text fragment is an item that contains (in the data slot) a token or any other
text data, combined with any other relevant data.  This is esp. a `key`, which
is most often a BibTeX citekey, and some other meta-data, most likely retreived
from the `meta` slot of a :py:class:`Pool` instance.

Created: 2025-05-06
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  01:14:41 Tue May  6 2025 CEST

"""

################################################################################

class TextFragment:
    """This class implements a TextFragment.

    A text fragment is an item that contains (in the data slot) a token or any
    other text data, combined with any other relevant data.  This is esp. a
    `key`, which is most often a BibTeX citekey, and some other meta-data, most
    likely retreived from the `meta` slot of a :py:class:`Pool` instance.

    :param key: A (unique) key. This is most likely a BibTeX citekey.
    :type key: string
    :param meta: A dict holding metadata, most likely derived from a BibTeX
       entry.
    :type meta: dict
    :param data: Any (text) data associated with this item.  This is most likely
        a `spacy.doc` or `spacy.token` object.
    :type data: any
    """
    def __init__(self,
                 key,
                 page_label = None,
                 meta = {},
                 data = None):
        self._key = key
        self._page_label = page_label
        self._meta = meta
        self._data = data

    ########################################

    @property
    def key(self):
        """Getter/setter for the key.
        """
        return self._key

    @key.setter
    def key(self, val):
        self._key = val


    @property
    def page_label(self):
        """Getter/setter for page label (str).
        """
        return self._page_label

    @page_label.setter
    def page_label(self, val):
        self._page_label = val

    @property
    def page_label(self):
        """Getter/setter for the page_label.
        """
        return self._page_label

    @page_label.setter
    def page_label(self, val):
        self._page_label = val

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
        """Getter/setter for the data.
        """
        return self._data

    @data.setter
    def data(self, val):
        self._data = val

    ########################################

################################################################################
## EOF textfragment.py
