To developers:
The documentation sources use Markdown with MyST extensions and are built with Sphinx.
Python docstrings use Markdown and are parsed by sphinx-autodoc2, which replaces `sphinx.ext.autodoc` and analyzes source statically.
Install the documentation dependencies with:

    pip install -r docs/requirements.txt

Then run the build script from the docs directory.
The old Sphinx 0.6 patch applies to the former reStructuredText sources and is no longer needed for the Markdown documentation.
The API reference pages are generated under `source/apidocs` during the build and are ignored by Git.
- Christian S. Perone
