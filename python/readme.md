# bp_text

This is the Python part of the *bp-text* project.

**NB:** In Python, the module is called bp_text!


## Installation Notes

### Dependencies

- Python 3
  - preferably in a venv[^1]
- Python libraries
  - NLP
    - https://flairnlp.github.io
    - https://www.nltk.org
  - BibTeX parsing
    - https://github.com/sciunto-org/python-bibtexparser
      - install *V2* via `pip install bibtexparser --pre`
  - https://github.com/pemistahl/lingua-py
  - https://pypi.org/project/pypdf/
- PDF
  - https://pypi.org/project/PyPDF2/
  - https://pypi.org/project/pytesseract/
  - https://pypi.org/project/pdf2image/
  - additionally (for ocr in pdfs):
    - tesseract ocr
      - https://github.com/tesseract-ocr/tesseract


[^1]: On MacOS, it's recommended to use pyenv in conjunction with pyenv-venv to
    manage python versions and virtual environments.
