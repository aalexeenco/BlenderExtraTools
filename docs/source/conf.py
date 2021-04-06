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
sys.path.insert(0, os.path.abspath("../../"))


# -- Project information -----------------------------------------------------

project = "Blender Extra Tools Add-on"
copyright = "2021, Andrei Alexeenco"
author = "aalexeenco"

# The full version, including alpha/beta/rc tags
# use command line arguments -D version=1.2 -D release=1.2.3
release = "x.y.z"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build"]


# -- Options for HTML output -------------------------------------------------
html_short_title = "Add-on Manual"
html_show_sourcelink = False

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_material"

html_theme_options = {
    "base_url": "http://aalexeenco.github.io/BlenderExtraTools/",
    "repo_url": "https://github.com/aalexeenco/BlenderExtraTools/",
    "repo_name": "BlenderExtraTools",
    "logo_icon": "&#x1f6e0",
    "globaltoc_depth": 2,
    "nav_title": "Blender Extra Tools",
    "heroes": {
        "index": "Blender<small><sup>®</sup></small> Add-on with extra tools and features."  # noqa E501
    },
    "version_dropdown": True,
    "version_json": "../versions.json",
}

# MaterialTheme config
html_sidebars = {
    "**": [
        "logo-text.html",
        "globaltoc.html",
        "localtoc.html",
        "searchbox.html",
    ]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


def config_inited_handler(app, config):
    config.html_theme_options["nav_title"] += " " + config.release


def setup(app):
    app.connect("config-inited", config_inited_handler)
