# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

src = os.path.abspath('../ssaw')
sys.path.insert(0, src)



about = {}
with open(os.path.join(src, '__about__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

# -- Project information -----------------------------------------------------

project = about['__title__']
author = about['__author__']
version = about['__version__']
release = about['__version__']


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html',
    ]
}

html_theme_options = {
    'logo': 'logo.png',
    'touch_icon': 'logo-small.png',
    'github_user': 'vavalomi',
    'github_repo': 'ssaw',
    'github_button': True,
    'fixed_sidebar': True,
    'extra_nav_links': {'Survey Solutions Documentation': 'https://support.mysurvey.solutions'}
}

html_static_path = ['_static']

napoleon_use_rtype = False
autodoc_member_order = 'bysource'