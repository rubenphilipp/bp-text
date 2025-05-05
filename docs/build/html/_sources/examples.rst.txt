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

   # this returns the data according to the given default_get_data_func
   pool.get("chion2018").get_data()
   # => <bp_text.pdf.PdfFile object at 0x453d80ef0>
   
   # you can also use a different method to get the data
   pool.get("chion2018").get_data(bp_text.pool.random_data)
   # => <bp_text.pdf.PdfFile object at 0x453d80ef0>
   
   # this entry ("chion2018") is a PDF, so it contains multiple pages
   pool.get("chion2018").get_data().get_page(20).text()
   # => 'XX FOREWORD\n(the disembodied voice seems to come from (...)
   


Using a cache (via `cache`, which is a directory where to store cache files)
improves the performance of `bp_text`. 


Trivial Noun Search
^^^^^^^^^^^^^^^^^^^

The following lines show how to search a pool for a `search_word` which should
be used as a noun in the context of the respective text:

.. code-block:: python

   # these need to be imported in order to make the typecasting work (via
   # isinstance())...
   from bp_text.pdf import PdfFile
   from bp_text.txt import TxtFile
   
   # this word is the word to find in the pool...
   search_word = "sprache"
   # as we, in this example (see below), use normalized words, let's apply
   # lowercase...
   search_word = search_word.lower()
   
   # this is an empty list for the results (which will be a dict)...
   results = {}
   
   # now, loop through all available pool items...
   for key, pitm in pool.data.items():
       # get a data object (either a TxtFile or a PdfFile)...
       data = pitm.get_data()

       # these will be the matches...
       matches = []

       # just proceed if the PoolItem contains either a PdfFile or a TxtFile
       # object)...
       if isinstance(data, PdfFile) or isinstance(data, TxtFile):
           # loop throuth all pages while preserving the pagenum (which is the
           # page
           # index here)...
           for pagenum, page in enumerate(data.data):
               # this is the spacy.doc
               doc = page.text.doc
               # this is the page_label (cf. :py:module:`bp_text.pdf`)
               page_label = page.page_label
               # if the page does not contain any text, the doc might be empty.
               # this handles this case...
               if doc == None:
                   continue
               # now, search the spacy.doc for nouns matching the pattern
               for token in doc:
                   if (token.text.lower() == search_word
                       and token.pos_ == "NOUN"):
                       # make a TextFragment object for this search result
                       frag = bp_text.textfragment.TextFragment(key,
                                                                page_label,
                                                                pitm.meta,
                                                                token)
                       matches.append(frag)
                       
       else:
           continue

       # add the matches to the results...
       if matches:
           results[key] = matches

   # this loop goes through the items in the results variable and prints the
   # token and the page_label (if applicable)...
   for key, val in results.items():
       print("-------")
       for itm in val:
           print(f"data: '{itm.data}'")
           print(f"page_label: '{itm.page_label}'")

   # get tokens around the tokens
   selected_token = results["nietzsche2"][7].data
   print(f"This is the token: '{selected_token}'")
   print("This is the next token: " +
         f"'{selected_token.doc[selected_token.i + 1]}'")
   print("This is the prev token: '"
         + f"{selected_token.doc[selected_token.i - 1]}'")
   print("This is the sentence:")
   print(f"'{selected_token.sent.text}'")
