# bp_text

This is the Python part of the *bp-text* project.

**NB:** In Python, the module is called bp_text!


## Installation Notes

The easiest way to install this package is by calling:

```shell
pip install bp_text
# or with an absolute path
pip install /path/to/bp-text/python/
```

### Dependencies

- Python 3
  - preferably in a venv[^1]
- Python libraries
  - NLP
    - https://flairnlp.github.io
      - `pip install flair` 
    - https://www.nltk.org
      - `pip install nltk`
      - make sure to also download the data (cf. https://www.nltk.org/data.html)
  - BibTeX parsing
    - https://github.com/sciunto-org/python-bibtexparser
      - install *V2* via `pip install bibtexparser --pre`
  - https://github.com/pemistahl/lingua-py
    - `pip install lingua-language-detector`
  - https://pypi.org/project/pypdf/
    - `pip install pypdf`
- PDF
  - https://pypi.org/project/PyPDF2/
    - `pip install PyPDF2`
  - https://pypi.org/project/pytesseract/
    - `pip install pytesseract`
  - https://pypi.org/project/pdf2image/
    - `pip install pdf2image`
  - additionally (for ocr in pdfs):
    - tesseract ocr
      - https://github.com/tesseract-ocr/tesseract


## Build Documentation

The documentation of this module is built using [Sphinx](http://sphinx-doc.org).
In order to rebuild the doc, it is necessary to install the related dependencies
via:

```shell
pip install "bp_text[docs]"
```

Then, in the `docs/` directory, run...

```shell
build html
```

...in order to build the HTML documentation. 

It might be necessary to re-build the complete documentation before
(re-)generating it:

```shell
make clean
make html
```

**NB:** This Sphinx documentation uses `sphinx.ext.autodoc` for the
documentation of inline commentary.



[^1]: On MacOS, it's recommended to use pyenv in conjunction with pyenv-venv to
    manage python versions and virtual environments.
