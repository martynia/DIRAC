#
# DiracDocs documentation build configuration file, created by
# sphinx-quickstart on Sun Apr 25 17:34:37 2010.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# pylint: disable=invalid-name
import logging
import datetime
import os
import sys

sys.path.insert(0, ".")

import recommonmark
from recommonmark.transform import AutoStructify

import diracdoctools
import diracdoctools.cmd
from diracdoctools import fakeEnvironment, environmentSetup, DIRAC_DOC_MOCK_LIST
from diracdoctools.Utilities import setUpReadTheDocsEnvironment, registerValidatingExitHandler

logging.basicConfig(level=logging.INFO, format="%(name)25s: %(levelname)8s: %(message)s")
LOG = logging.getLogger("conf.py")

LOG.info("Current location %r", os.getcwd())
LOG.info("DiracDocTools location %r", diracdoctools.__file__)
LOG.info("DiracDocTools location %r", diracdoctools.Utilities.__file__)
LOG.info("DiracDocTools location %r", diracdoctools.cmd.__file__)

# configuration

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# AUTO SETUP START
if os.environ.get("READTHEDOCS") == "True":
    setUpReadTheDocsEnvironment(moduleName="DIRAC", location="../../src")

    # re-create the RST files for the command references
    LOG.info("Building command reference")
    from diracdoctools.cmd.commandReference import run as buildCommandReference

    buildCommandReference(configFile="../docs.conf")

    # singlehtml build needs too much memory, so we need to create less code documentation
    buildType = "limited" if any("singlehtml" in arg for arg in sys.argv) else "full"
    LOG.info("Chosing build type: %r", buildType)
    from diracdoctools.cmd.codeReference import run as buildCodeDoc

    buildCodeDoc(configFile="../docs.conf", buildType=buildType)

    # Update dirac.cfg
    LOG.info("Concatenating dirac.cfg")
    from diracdoctools.cmd.concatcfg import run as updateCompleteDiracCFG

    updateCompleteDiracCFG(configFile="../docs.conf")

# AUTO SETUP END

else:
    # If not READTHEDOCS just prepare dirac.cfg for docs
    from diracdoctools.cmd.concatcfg import ConcatCFG

    ConcatCFG(configFile="../docs.conf").prepareDiracCFG()

# get the dirac version
try:
    from DIRAC import version

    LOG.info("Found dirac version %r", version)
except ImportError as e:
    LOG.info("Failed to import DIRAC.version: %s", e)
    version = "integration"
diracRelease = version
# on rtd we use (parts of) the branch, unless "branch" is latest
if os.environ.get("READTHEDOCS") == "True":
    diracRelease = os.path.basename(os.path.abspath("../../"))
    if diracRelease.startswith("rel-"):
        # basically version without patch number
        diracRelease = diracRelease[4:]
    elif diracRelease == "latest":
        diracRelease = version

LOG.info("DIRACVERSION is %r", diracRelease)

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.graphviz",
    "recommonmark",
    "sphinx_rtd_theme",
    "sphinx_panels",
]


def setup(app):
    app.add_config_value(
        "recommonmark_config",
        {
            "enable_eval_rst": True,
            "auto_toc_tree_section": "Contents",
        },
        True,
    )
    app.add_transform(AutoStructify)


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "ma",
    ".md": "markdown",
}


# The encoding of source files.
# source_encoding = 'utf-8'

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "DIRAC"
copyright = "%s, DIRAC Project" % datetime.datetime.utcnow().year

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ""
# The full version, including alpha/beta/rc tags.
release = diracRelease

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = "%H:%M %d/%m/%Y %Z"

# List of documents that shouldn't be included in the build.
# unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
# ADRI: Ignore old stuff that is not included in the compilation
exclude_trees = ["AdministratorGuide/Configuration/ConfigurationReference"]

# The reST default role (used for this markup: `text`) to use for all documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = dict(
    # sidebarbgcolor='#D5E2F2',
    logo_only=True
)

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "DIRAC Documentation"

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = '_static/DIRAC-logo.png'
html_logo = "_static/DIRAC-logo3.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_static/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%d/%m/%Y"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_use_modindex = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = "DiracDocsdoc"


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
# latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
# latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    ("index", "DiracDocs.tex", "DIRAC Documentation", "DIRAC Project.", "manual"),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# Additional stuff for the LaTeX preamble.
# latex_preamble = ''

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_use_modindex = True

# packages that cannot be installed in RTD
autodoc_mock_imports = DIRAC_DOC_MOCK_LIST


# link with the python standard library docs
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "matplotlib": ("https://matplotlib.org/", None),
}

# check for :param / :return in html, points to faulty syntax, missing empty lines, etc.
registerValidatingExitHandler()
