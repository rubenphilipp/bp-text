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


Languages
---------

Tokenization and tagging in this library is based on the `Flair
<https://flairnlp.github.io>` library.  This library is (as of 2025-04-23)
mainly focused on European languages, and so is this project.  When parsing
text, this should not be forgotten. 


