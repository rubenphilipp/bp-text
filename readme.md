# bp_text

This repository contains a set of tools for algorithmic text generation, being
written by Fabian Bentrup and Ruben Philipp for one of their current projects.

At its core, *bp_text* is capable of processing various text files contained
in a database (as of now in form of a BibTeX file), analyzing them (e.g. by
tokenizing the PDF-text) and generating new material from the source text(s).

This project has been initially created for the project *the prospect of its own
undoing* (working title) by Fabian Bentrup and Ruben Philipp.

For more information read the docs (at `docs/build/html/` or
https://rubenphilipp.github.io/bp-text/). 


## Installation Notes

The easiest way to install this package is by calling:

```shell
pip install bp_text
# or with an absolute path
pip install /path/to/bp-text/python/
```

### Models

This project uses [spaCy](http://spacy.io) to analyze text.  For more
information refer to the documentation (`docs/build/html/`).  


### Dependencies

All dependencies are listed in the `pyproject.toml` file. 

For OCR you might additionaly want to install *tesseract*
(https://github.com/tesseract-ocr/tesseract).  


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

## Simple example

Here is a simple example for loading a database and creating a *Pool*:

```python

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

```

# Apropos

*BP* could mean...

- Bentrup Philipp
- Binary Poem
- Bot Poet
- Boundless Prose
- Breathless Play
- Branching Plot
- Beat Poetry
- Bardic Performance
- Boolean Poetics
- Brutalist Play
- Blended Persona
- Broken Pentameter
- Bizarre Playwright
- Bespoke Poem
- Blank Page
- Borrowed Perspective
- Bifurcating Plot
- Bardic Prose
- Blueprint Play
- Boundless Performance
- Binary Perspective
- Buried Prologue
- Blended Poetry
- Bricolage Play
- Bardic Parable
- Bespoke Performance
- Borrowed Poetics
- Broken Prose
- Bifocal Perspective
- Baroque Play
- Binary Play
- Bounded Poetry
- Blueprint Prose
- Bifurcated Persona
- Blended Performance
- Bridging Plot
- Bespoke Plot
- Bardic Passage
- Binary Puppetry
- Brutalist Poetry
- Borrowed Plot
- Breached Perspective
- Baroque Prose
- Bifurcating Performance
- Broken Perspective
- Blended Plot
- Bespoke Prose
- Bardic Poetry
- Binary Passage
- Bridging Performance
- Borrowed Passage
- Breathless Prose
- Broken Play
- Blended Persona
- Bifurcating Poetics
- Boundless Poetics
- Bespoke Passage
- Bardic Puppetry
- Bridging Poetics
- Binary Performance
- Brutalist Prose
- Borrowed Play
- Bifurcated Prose
- Baroque Passage
- Breathless Poetry
- Boundless Plot
- Blended Puppetry
- Broken Poetics
- Bespoke Play
- Binary Parable
- Bridging Poem
- Bardic Blueprint
- Borrowed Blueprint
- Bespoke Perspective
- Binary Blueprint
- Brutalist Passage
- Bifurcated Blueprint
- Boundless Puppetry
- Blended Blueprint
- Broken Puppetry
- Baroque Blueprint
- Bifurcated Poetry
- Bridging Passage
- Binary Perspective
- Bespoke Puppetry
- Bardic Blueprint
- Breached Poetics
- Broken Blueprint
- Blended Play
- Bifurcating Puppetry
- Boundless Passage

...amongst others.


[^1]: On MacOS, it's recommended to use pyenv in conjunction with pyenv-venv to
    manage python versions and virtual environments.
