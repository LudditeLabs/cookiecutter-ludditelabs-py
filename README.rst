=======================
Python project template
=======================

.. image:: https://travis-ci.org/LudditeLabs/cookiecutter-ludditelabs-py.svg?branch=master
   :target: https://travis-ci.org/LudditeLabs/cookiecutter-ludditelabs-py

Cookiecutter_ template for a python package.

Features
--------

* Python ``3.9``.
* Testing with pytest_.
* Sphinx_ documentation with ReadTheDocs_ theme.
* Bitbucket pipeline configuration support.
* Project version management with setuptools-scm_.
* Command line interface using click_.
* Application configurations using dynaconf_.

Usage
-----

Make sure Cookiecutter_ is installed::

    pip install cookiecutter

Now you can generate a project::

    cookiecutter https://github.com/LudditeLabs/cookiecutter-ludditelabs-py

It will ask you few questions and then generate project in the current directory
with name of your package name.

Fields
------

Here is the list of fields you specify before project generating.

NOTE: For ``flag`` fields you set ``y`` or ``n``, generally all non-``y`` values
are considered ``n``.

=============================== ================================================
Field                           Description
=============================== ================================================
``project_title``               Title (name) of the project.

                                Used in ``README.rst``, project docs and in
                                CLI command.

``project_short_description``   Short (one line) description of the project.

                                Used in ``setup.py``.

``project_url``                 Optional project's URL. Leave empty value to not
                                set URL.

                                Used in ``setup.py``.

``package_name``                Python package name.

``author``                      The package author.

                                Used in ``setup.py`` and ``docs/conf.py``.

``email``                       Author emails.

                                Used in ``setup.py`` and ``docs/conf.py``.

``version``                     Project version.

                                Used in ``setup.*``, ``docs/conf.py`` and CLI.

``license``                     Project license.

                                Used in ``setup.py`` and ``LICENSE``.

``use_bitbucket_pipelines``     ``flag``: setup ``bitbucket-pipelines.yml``.

``use_travis``                  ``flag``: setup ``.travis.yml``.

``use_cli``                     ``flag``: create or not CLI.

                                Used in ``setup.py``.

``use_conda``                   ``flag``: use conda environment.

``sphinx_use_apidoc``           ``flag``: configure``sphinx.ext.apidoc`` to
                                generate API docs.
=============================== ================================================

What to do next
---------------

You may want to tune some parameters after the project is generated.

* **Requirements**: Update packages versions in the ``requirements/`` directory
  and ``setup.py``.

* **Bitbucket pipeline**/**travis**: Update or change docker image and
  ``script`` steps.

* **.gitignore**: Add more entries if required. Make sure you add to correct
  place. Consider use global ``.gitignore`` for system-specific files and local
  one only for project-specific files. This article can help to figure out:
  https://gist.github.com/subfuzion/db7f57fff2fb6998a16c.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _pytest: https://docs.pytest.org/en/latest/
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.io/
.. _click: https://click.palletsprojects.com/
.. _setuptools-scm: https://github.com/pypa/setuptools_scm/
.. _dynaconf: https://www.dynaconf.com/
