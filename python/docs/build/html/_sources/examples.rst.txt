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
   db = bp_text.database.BibTexDatabase("/sources.bib")
   
   # get keywords if the field is not empty
   entry = db.entries.get("chion2018")
   if entry.get("keywords"):
       print(entry.get("keywords").value)

   # => ['Aesthetics', 'Motion pictures', 'Sound effects', 'Sound motion
   #     pictures']


   
