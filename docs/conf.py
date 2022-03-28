"""Sphinx configuration."""
from datetime import datetime

# pylint: disable=C0103,W0622


project = "Okapi"
author = "Romain Brault"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
]
autodoc_typehints = "description"
html_theme = "furo"
