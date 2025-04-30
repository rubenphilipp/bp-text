.. -*- eval: (flyspell-mode); eval: (ispell-change-dictionary "en") -*-

Notes
=====


Some notes and remarks on several aspects of `bp_text`.


Working with BibTeX files
-------------------------

For managing BibTeX databases (`.bib` files), using `BibDesk
<http://bibdesk.sourceforge.io>` (on a Mac) is an easy way to organize the text
library.  However, there are a few things to consider, especially when it comes
to non-standard BibTeX fields. 

The crucial part with BibDesk as well as with other citation/library managers is
in the case of `bp_text` the way how files (resp. paths to them) are stored.
`BibDesk` by default uses a rather complex way to store files attached via the
regular `BibDesk` attachments in the BibTeX library.  It does so by including
serialized symlinks to `bdsk-file-n` fields.  `bp_text` does not handle these,
but expects files to be stored as (absolute or relative) paths to e.g. PDFs or
TXTs in a `file` field.  Although singular, there could be more files included
when separating the filenames with a semicolon.  Yet whether this makes sense
depends on the way the relation between BibTeX entries and the respective files
is conceived.

Keywords can also be included.  They should be placed in a `keywords` field
which should be provided by `BibDesk` by default and should also be the standard
field when exporting a library from Zotero e.g. via BetterBibTeX.  

Citation keys should, of course, be unique.

The primary language of a document is expected to be stored in the `langid`
field.  This is a BibLaTeX field and expects languages to be identified by an
idiosyncratic id which is not the same as standard ISO-639-1 language codes.
The langid for German, for example, is `ngerman` (i.e. new German spelling).
See *Table 2: Supported Languages* in the BibLaTeX documentation
(https://ctan.org/pkg/biblatex).  Although it is allowed to omit specifying a
primary language, it is highly recommended as e.g. the PdfFile class will use
the language when performing OCR.

Some notes on BibDesk
^^^^^^^^^^^^^^^^^^^^^

Some BibTeX fields used `bp_text` are not available in BibDesk by default.
Thus, it is recommended to add these to the Default Fields via `BibDesk
Preferences -> Fields -> Custom BibTeX Fields`.  These are some fields which
should be added.  Make sure to tick the "Is Default" checkbox. 

+--------+--------------+-------+
|Field   |Type          |Is     |
|        |              |Default|
+========+==============+=======+
|Keywords|Textual       |Y      |
+--------+--------------+-------+
|File    |Textual       |Y      |
|        |              |       |
+--------+--------------+-------+
|Langid  |Textual       |Y      |
+--------+--------------+-------+

Zotero and BibDesk
^^^^^^^^^^^^^^^^^^

It is quite simple to copy Zotero (https://www.zotero.org) bibliography data to
BibDesk.  In order to export Zotero data to Bib(La)TeX, first install the
`Better BibTeX` (https://retorque.re/zotero-better-bibtex/) extension in Zotero.
Then, for example, select a few entries in your Zotero database and select "copy
BibLaTeX to clipboard" in the "Better BibTeX" context menu (via right-click).
Then, you can simply paste your clipboard to your BibDesk library.

Better BibTeX automatically includes the paths to the PDFs attached to a Zotero
item in the `file` field.  Multiple files are separated by a semicolon.  As this
is also the standard way `bp_text` handles files, nothing more needs to be done.
If you want to share your BibDesk database you might want to copy the
attachments from the Zotero storage location to a directory relative to the path
of the BibDesk (.bib) file.  Then you need to adjust the `file` field in the
respective entries accordingly.  A relative path is completely sufficient here
as `bp_text` searches for files relative to the database file when no absolute
path is given (e.g. when calling `BibtexDatabase.make_pool()`).  



Languages
---------

Tokenization and tagging in this library is based on the `spaCy
<https://spacy.io>` library.  `bp_text` tries to automatically determine the
language of a text and apply the proper model to it.  For more information see
the documentation for :py:class:`Text`. 


