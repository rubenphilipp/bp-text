"""This module implements the TextFragment class.

A text fragment is an item that contains (in the data slot) a token or any other
text data, combined with any other relevant data.  This is esp. a `key`, which
is most often a BibTeX citekey, and some other meta-data, most likely retreived
from the `meta` slot of a :py:class:`Pool` instance.

Created: 2025-05-06
Author: Ruben Philipp <me@rubenphilipp.com>

$$ Last modified:  16:34:18 Wed May  7 2025 CEST

"""

from spacy.tokens import Token, Span, Doc

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

    def format_org(self,
                   cite = True,
                   force_cite = False):
        """This returns a formatted string with the text contained in `data` in
        org-mode syntax.

        :param cite: When True, an org-cite citation will be appended to the
            generated string. Default = True
        :type cite: boolean
        :param force_cite: When True (and `cite`=True), also for a citation for
            text elements that normally don't "require" a citation (e.g. PUNCT).
            Default = False
        :type force_cite: boolean

        :returns: A string with the content of `text` formatted in org-mode
            syntax. 
        """
        res = ""
        res_pos = None

        if isinstance(self.data, str):
            res = self.data
        elif isinstance(self.data, Token):
            res = self.data.text
            res_pos = self.data.pos_
        elif isinstance(self.data, Span):
            res = self.data.text
        else:
            print("TextFragment.format_org: The data does not contain valid "
                  + "text.")
            return None

        if (cite and self.key
            and ((res_pos != "PUNCT" and res_pos != "SPACE")
                 or force_cite)):
            if self.page_label:
                res += "[cite:@" + self.key + " " + self.page_label + "]"
            else:
                res += "[cite:@" + self.key + "]"

        return res


################################################################################

def textfragments_to_org(fragment_list,
                         cite = True,
                         force_cite = False):
    """This function takes a `list` of :py:class:`TextFragment` objects and
    returns a `string` formatted in org-mode syntax, (optionally) including
    org-cite references.

    :param fragment_list: The :py:class:`TextFragment` objects. 
    :type fragment_list: A list with :py:class:`TextFragment` objects.
    :param cite: When True, an org-cite citation will be appended to the
        generated string. Default = True
    :type cite: boolean
    :param force_cite: When True (and `cite`=True), also for a citation for
            text elements that normally don't "require" a citation (e.g. PUNC).
            Default = False
    :type force_cite: boolean
    """
    if not (isinstance(fragment_list, list)
            and all(isinstance(ele, TextFragment) for ele in fragment_list)):
        raise ValueError("textfragments_to_org: fragment_list must be a list "
                         + "of TextFragment objects.")

    res_string = ""
    for i, frag in enumerate(fragment_list):
        res_string += frag.format_org(cite = cite,
                                      force_cite = force_cite)
        ## add a space if this is not the last fragment and the next fragment's
        ## token is not punctuation
        ## always adds a space if the data contains something else than a
        ## spacy.Token 
        if i < len(fragment_list) - 1:
            next_frag = fragment_list[i + 1]
            if (isinstance(next_frag.data, Token)
                and isinstance(frag.data, Token)):
                if not next_frag.data.is_punct and not frag.data.is_space:
                    res_string += " "
            else:
                res_string += " "

    return res_string
        

################################################################################
## EOF textfragment.py
