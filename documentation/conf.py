# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# pylint: disable=invalid-name, missing-module-docstring
from __future__ import annotations

import sys
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Literal, TypeAlias

sys.path.insert(0, str(Path('..', 'src').resolve()))
sys.path.insert(0, str(Path('.').resolve()))


if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.ext.autodoc import Options

import simplebench._meta as metadata  # pylint: disable=wrong-import-position  # noqa: E402

# -- Project information -----------------------------------------------------

project: str = metadata.__project__
copyright: str = metadata.__copyright__  # pylint: disable=redefined-builtin
author: str = metadata.__author__

# The short X.Y version
version: str = metadata.__version__
# The full version, including alpha/beta/rc tags
release: str = metadata.__release__


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # 'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.apidoc',
    'sphinx.ext.autodoc',
    # 'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    # 'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
    'sphinx.ext.viewcode',
    'sphinx_copybutton',
    'sphinx_design',
]


simplebench_src_path = Path('..', 'src', 'simplebench')

# -- Custom file exclusions for apidoc --------------------------------------------


def catalog_files(dir_path: Path) -> list[Path]:
    """Catalog all files in a directory and subdirectories.
    :param dir_path Path: The directory path to catalog.
    :return list[Path]: A list of file paths in the directory.
    """
    # Use rglob to recursively find all python files and make them relative
    return [p.relative_to(dir_path) for p in dir_path.rglob('*') if p.is_file() and p.suffix == '.py']


def exclude_files(dir_path: Path) -> list[str]:
    """Generate a list of file patterns to exclude from apidoc generation.

    It excludes files where the file name stem matches its parent directory name,
    e.g., metric/metric.py.

    :param dir_path Path: The directory path to generate exclusions for.
    :return list[str]: A list of file patterns to exclude.
    """
    files = catalog_files(dir_path)
    exclusions: list[str] = []
    for item in files:
        if item.suffix == '.py' and item.parent != Path('.'):
            if item.stem == item.parent.name:
                # Create a posix-style path relative to the conf.py directory
                rel_path_parts = list(dir_path.parts)
                rel_path_parts.append(item.as_posix())
                item_path = Path(*rel_path_parts).as_posix()
                exclusions.append(item_path)
    return exclusions


# apidoc options
apidoc_modules = [
    {
        'path': simplebench_src_path.as_posix(),
        'destination': 'source/',
        'exclude_patterns': exclude_files(simplebench_src_path),
        'max_depth': 4,
        'follow_links': False,
        'separate_modules': False,
        'include_private': False,
        'no_headings': False,
        'module_first': False,
        'implicit_namespaces': False,
        'automodule_options': {
            'members', 'show-inheritance', 'undoc-members'
        },
    },
]

# print(f"apidoc_modules: {apidoc_modules}")

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'rich': ('https://rich.readthedocs.io/en/latest/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'seaborn': ('https://seaborn.pydata.org/', None),
    'psutil': ('https://psutil.readthedocs.io/en/latest/', None),
    'pytest': ('https://docs.pytest.org/en/latest/', None),
    'jsonschema': ('https://python-jsonschema.readthedocs.io/en/stable/', None),
}
intersphinx_disabled_domains = ['std']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'tests',
    'conf.py'
    'coverage',
    '.venv',
    '.venv-3.10',
    '.venv-3.11',
    '.venv-3.12',
    '.venv-3.13',
    '.venv-3.14',
    ]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "github-dark"


# -- Options for HTML output -------------------------------------------------

# Maximum line length for signatures in the HTML docs.
maximum_signature_line_length: int = 50

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'sphinxawesome_theme'
html_theme: str = 'furo'
html_logo = '_static/images/simplebench-logo.svg'


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom CSS files.
html_css_files = [
    'custom.css',
]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# Icon to use for the permalink to the current page.
html_permalinks_icon = '🔗'

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'simplebenchdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {  # type: ignore [var-annotated]
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'simplebench.tex', 'simplebench Documentation',
     'Jerilyn Franz', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual metric).
man_pages = [
    (master_doc, 'simplebench', 'simplebench Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'simplebench', 'simplebench Documentation',
     author, 'simplebench', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
# epub_title = simplebench

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

epub_show_urls = 'footnote'

# -- Extension configuration -------------------------------------------------

# By default, highlight as Python 3.
highlight_language = 'python3'

# This pattern will automatically exclude prompts from shell blocks
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True


# -- Options for autodoc extension -------------------------------------------

# This value determines whether module names are prepended to all
# documented members. If true, the module name is prepended.
# autodoc_canonical_imports = True

# This value controls how to represent the signature of a class.
# 'class' shows the class name, 'init' shows the __init__ signature.
autodoc_class_signature = 'mixed'

# This value selects what content will be inserted into the main body of an
# autoclass directive. The possible values are:
# "class", "init", "both"
autoclass_content = 'both'


# -- Options for doctest -------------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html#configuration

# This code block will be executed before each doctest.
# We use it to inject our custom assertion helper into the test's global namespace.
doctest_global_setup = """
from _helpers.doctest_utils import run_script_and_get_raw_output, assert_benchmark_output
"""


# -- Custom skip member function for autodoc --------------------------------


What: TypeAlias = Literal['module', 'class', 'exception', 'function', 'method', 'attribute']


def custom_skip_member(app: Sphinx, what: What, name: str, obj: object, skip: bool, options: Options) -> bool | None:  # pylint: disable=unused-argument
    """Custom skip member function for autodoc.

    :param app Sphinx: The Sphinx application object.
    :param what What: The type of the object which the member belongs to.
    :param name str: The name of the member.
    :param obj object: The member object itself.
    :param skip bool: A boolean indicating if Sphinx intends to skip this member.
    :param options Options: The autodoc options given to the directive.
    :return bool | None: True to skip the member, False to include it, or None to use default behavior.
    """
    print(f"custom_skip_member called: app={type(app)}, what={what}, name={name}, obj={repr(obj)}, skip={skip}, options={type(options)}")
    if what != 'module' or not isinstance(obj, ModuleType):
        return None

    fqn = obj.__name__
    print(f"Fully qualified name of the module: {fqn}")
    path_elements = fqn.split('.')
    if len(path_elements) < 2:
        return None
    module_name = path_elements[-2]
    member_name = path_elements[-1]
    # Don't skip if we don't have a pattern like metric.metric
    if module_name != member_name:
        return None

    # This is a module that matches a pattern like metric.metric
    # We consider these "private" implementation modules and skip them
    print(f"************Skipping private implementation module: {fqn}")
    return True  # Skip "private" implementation modules


# def setup(app):
#     """Register the custom skip function with Sphinx."""
#     app.connect('autodoc-skip-member', custom_skip_member)
