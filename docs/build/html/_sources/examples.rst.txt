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
be used as a noun in the context of the respective text.

The :py:class:`bp_text.textfragment.TextFragment` can be, in this case,
conceived as a "container" for the search results.  It holds the token of the
search result as well as the citekey, the page_label and some meta-data (taken
from the resp. item's meta-data which is most likely retrieved from the BibTeX
file).  In general, `TextFragment` objects help to unify the results of data
extraction e.g. from a pool. 

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


org-mode
--------

The easiest way to compile a text with material generated by `bp_text` is to use
embedded python code in Emacs's `org-mode` [#f1]_.  The following example shows
a simple way to work with `bp_text` in this way.

.. code-block:: org-mode

   #+title: Testdocument
   #+author: Ruben Philipp
   #+date: 2025-05-13
   #+LANGUAGE: de
   #+startup: overview
   #+LATEX_COMPILER: xelatex
   #+LATEX_CLASS: article
   #+LATEX_CLASS_OPTIONS: [a4paper,10pt,oneside]
   #+LATEX_HEADER: \usepackage{multicol} 
   #+LATEX_HEADER: \usepackage{geometry}
   #+LATEX_HEADER: \geometry{left=15mm,right=15mm,top=15mm,bottom=15mm}
   #+LATEX_HEADER: \usepackage[hang,flushmargin]{footmisc} 
   #+LATEX_HEADER: \usepackage{pdflscape}
   #+LATEX_HEADER: \usepackage{lmodern}
   # #+LATEX_HEADER: \usepackage{ebgaramond}
   #+LATEX_HEADER: \usepackage{fontspec}
   #+LATEX_HEADER: \setmainfont{Adobe Garamond Pro}
   #+LATEX_HEADER: \usepackage{fancyhdr}
   #+LATEX_HEADER: \usepackage{epigraph}
   #+LATEX_HEADER: \usepackage[utf8]{inputenc}
   #+LATEX_HEADER: \usepackage[ngerman]{babel}
   # % caption styling
   #+LATEX_HEADER: \usepackage[font=small,labelfont=bf]{caption}
   
   #+cite_export: csl chicago-note-bibliography.csl
   
   #+options: toc:nil num:nil ':t
   #+bibliography: /path/to/sources.bib
   #+LaTeX_HEADER: \hypersetup{hidelinks}
   #+LATEX_HEADER: \usepackage{setspace}
   #+EXPORT_FILE_NAME: /tmp/test
   # % code listings with mono font
   #+LATEX_HEADER: \lstset{basicstyle=\footnotesize\ttfamily,breaklines=true}
   #+LATEX_HEADER: \lstset{keepspaces=true}
   # % hyphenation in mono/texttt blocks
   #+LATEX_HEADER: \usepackage[htt]{hyphenat}
   
   
   #+begin_src python :session bp_text :results none :exports none
   
   ## These are some global definitions and declarations
   
   import bp_text
   import os
   import random
   
   DATA_ROOT = os.path.abspath("data")
   SOURCES_BIB = DATA_ROOT + "/sources.bib"
   
   # Just instantiate DB and POOL once as this might take a while
   try:
       DB and POOL
   except NameError:
       # not defined, instantiate
       DB = bp_text.database.BibTexDatabase(SOURCES_BIB)
       POOL = DB.make_pool(cache=DATA_ROOT + "/_pool-cache")
   
   
   # Set this if citations for items retrieved from a pool should be included in
   # the generated text.
   CITE = False
   
   #+end_src
      
   
   * Text From a "Model"
   
   #+begin_comment
   This example uses an input text as a model and "replaces" the words in the
   text with words with the same POS from randomly chosen pages from a text in the
   pool. 
   #+end_comment
   
   #+begin_src python :session bp_text :results value raw :exports results
   
   # This is the pool item and its associated doc
   thePitm = POOL.get("arendt2006")
   theDoc = thePitm.get_data()
   
   # number of pages in doc
   num_pages = len(theDoc.data)
   
   # this is the input text
   # source:
   # https://www.soziopolis.de/zur-diagnostischen-gefuehlskultur-der-gegenwart.html
   input_sentence = """
   Trauma, toxisch, triggern – Wörter wie diese sind
   inzwischen fester Bestandteil des Begriffsinventars, mit dem viele Menschen,
   online wie offline, über Lebenskrisen und zwischenmenschliche Konflikte
   sprechen. In Digitale Diagnosen. Psychische Gesundheit als Social-Media-Trend
   analysiert die Soziologin Laura Wiesböck ebenjene gegenwärtige Melange aus
   therapeutischen Diskursfragmenten auf Social Media. Die Autorin, Jahrgang 1987,
   hat an der Universität Wien promoviert und ist auf die Themen soziale
   Ungleichheit, Gendergerechtigkeit und digitale Arbeitswelt spezialisiert. Seit
   2018 ihr erstes Buch In besserer Gesellschaft. Der selbstgerechte Blick auf die
   Anderen erschienen ist, zählt sie zu den medial präsentesten Gesichtern einer –
   jungen und weiblichen – soziologischen Wissenschaftskommunikation. Das
   vorliegende Sachbuch adressiert eine breite Öffentlichkeit jenseits der
   fachwissenschaftlichen Community. Das verhandelte Phänomen ist eine so markante
   Signatur unserer Gegenwart, dass Wiesböcks Buch eine gewinnbringende Lektüre für
   unterschiedliche Leserschaften – vor allem mit sozialwissenschaftlichem und
   psychologischem Fachhintergrund – ist.
   """
   
   # initialize a NLP model
   nlp = bp_text.text.get_nlp("de_core_news_sm")
   
   # analyze the input text
   input_doc = nlp(input_sentence)
   
   # reset random seed
   random.seed(123)
   
   result = []
   for word in input_doc:
       pg_i = random.randrange(num_pages)
       pg = theDoc.get_page(pg_i)
       for token in pg.text.doc:
           if token.pos_ == word.pos_:
               result.append(bp_text.textfragment.TextFragment(thePitm.key,
                                                               pg.page_label,
                                                               thePitm.meta,
                                                               token))
               break
   
   # output the results as org text
   bp_text.textfragment.textfragments_to_org(result,
                                             cite = CITE,
                                             force_cite = False)
   
   
   #+end_src
   
   * Literature
   
   #+print_bibliography: 









.. rubric:: Footnotes

.. [#f1] Cf. https://orgmode.org and
         https://orgmode.org/worg/org-contrib/babel/languages/ob-doc-python.html
         for more details on working with Python in `org-mode`.  
