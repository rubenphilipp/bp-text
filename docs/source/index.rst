.. bp_text documentation master file, created by
   sphinx-quickstart on Wed Apr 23 13:34:55 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

bp_text documentation
=====================

This is the documentation of ``bp_text``, which is a Python library containing
tools for algorithmic text generation.

At its core, ``bp_text`` is capable of processing various text files contained
in a database (as of now in form of a BibTeX file), analyzing them (e.g. by
tokenizing the PDF-text) and generating new material from the source text(s).

This project has been initially created for the project *the prospect of its own
undoing* (working title) by Fabian Bentrup and Ruben Philipp.

This project uses spaCy (http://spacy.io) to analyze text.  For more information
see esp. the doc for the `text` module.


.. note::

   This project is still under active development.  Thus, the API is likely to
   change.  Additionally, not all functionality described in parts of this
   documentation is implemented. 



   
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   api
   notes
   examples
   
