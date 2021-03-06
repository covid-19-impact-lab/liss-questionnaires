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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'CoViD-19 Impact Lab Questionnaire Documentation'
copyright = '2020, CoViD-19 Impact Lab Team'
author = 'CoViD-19 Impact Lab Team'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
master_doc = 'index'

extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme_path = ["_themes", ]
html_theme = "yummy_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


html_theme_options = {
    'navs': {
        'GitHub': 'https://github.com/covid-19-impact-lab',
	'Data Explorer': 'https://covid-19-impact-lab.iza.org/app',
	'About': "https://covid-19-impact-lab.readthedocs.io/en/latest/"
    },
    'service': 'GitHub',
    'user': 'covid-19-impact-lab',
    'repo': 'liss-questionnaires',
    'twitter_url': 'https://twitter.com/CovidImpactLab',
}

html_logo = '_static/images/impactlab_logo_simple.png'
