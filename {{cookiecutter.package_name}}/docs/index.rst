{{ '*' * (cookiecutter.project_title|length) }}
{{ cookiecutter.project_title }}
{{ '*' * (cookiecutter.project_title|length) }}

Documentation
-------------

.. toctree::
   :maxdepth: 2

   overview

{% if cookiecutter.sphinx_use_apidoc == 'y' -%}
API Reference
-------------

This section provides information about functions, classes and methods.

.. toctree::
   :maxdepth: 3

   _apidoc/modules
{%- endif %}

Miscellaneous Pages
===================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
