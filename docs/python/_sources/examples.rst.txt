.. -*- eval: (flyspell-mode); eval: (ispell-change-dictionary "en") -*-

==========
 Examples
==========

First of all, load the library:

.. code-block:: python

   import bp_text

   
Database
--------

This examples shows how to load a BibTeX file and access the keywords of an
entry by a given citation key:

.. code-block:: python

   # load the database
   db = bp_text.database.BibTexDatabase("sources.bib")
   
   # get keywords if the field is not empty
   entry = db.entries.get("chion2018")
   if entry.get("keywords"):
       print(entry.get("keywords").value)

   # => ['Aesthetics', 'Motion pictures', 'Sound effects', 'Sound motion
   #     pictures']


   
Pool
----


The :py:class:`bp_text.pool.Pool` class is the heart of `bp_text`.  This class
is a collection of annotated/tokenized, text-holding objects (e.g.  PdfFiles,
TxtFiles) and can be generated from a BibTexDatabase object.  Its main purpose
is to facilitate interacting with a corpus of texts and the metadata provided by
the BibTex entries.

The most straightforward way to create a pool is to first load a BibTeX database
and then derive a `Pool` from the `BibTexDatabase` object.

**Note:** It is crucial to include paths to the source files (either PDF or TXT)
in the BibTeX file (cf. `notes`).  The paths can either be absolute or relative
(to the BibTeX file).

Here is an example for creating a database and a derived `Pool`:

.. code-block:: python

   import bp_text
   db = bp_text.database.BibTexDatabase("/users/bp/sources.bib")
   pool = db.make_pool(cache="/tmp/pool_cache")


Using a cache (via `cache`, which is a directory where to store cache files)
improves the performance of `bp_text`. 
