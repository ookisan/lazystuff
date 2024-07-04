project = 'lazystuff'
copyright = '2024, David Byers'
author = 'David Byers'
release = '0.1'

master_doc = "index"

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = []

pygments_style = None
html_theme = 'sphinx_rtd_theme'
html_theme_options = {}
html_static_path = ['_static']

add_module_names = False
