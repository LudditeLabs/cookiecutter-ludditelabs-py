=======================
Python project template
=======================

Cookiecutter_ template for a python package.

Features
--------

* Testing with pytest_ and tox_ (3.5, 3.6 and 3.7).
* Code style validation with flake8_.
* Sphinx_ documentation with ReadTheDocs_ theme.
* Bitbucket pipeline configuration support.
* Project version management with bumpversion_.
* Command line interface using click_.

Usage
-----

Make sure Cookiecutter_ is installed::

    pip install cookiecutter

Now you can generate a project::

    cookiecutter git+ssh://git@bitbucket.org/ludditelabs/cookiecutter-ludditelabs-py.git

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

``use_cli``                     ``flag``: create or not CLI.

                                Used in ``setup.py``.

``use_logging``                 ``flag``: add logging support.

                                Adds ``utils/logging.py`` with logging utils.

``use_appconfig``               ``flag``: add application configuration loading
                                with ``configsource`` package.

                                Used in ``setup.py``, ``requirements/base.txt``.

                                Adds ``utils/config.py``.

``use_appconfig_s3``            ``flag``: add ``configsource_s3`` dependency to
                                ``requirements/base.txt`` to support remote
                                configurations loading from AWS S3 buckets.

                                Used in ``setup.py``, ``requirements/base.txt``.

``sphinx_use_apidoc``           ``flag``: configure``sphinx.ext.apidoc`` to
                                generate API docs.

``use_bitbucket_pipeline``      ``flag``: create ``bitbucket-pipelines.yml``.
=============================== ================================================

What to do next
---------------

You may want to tune some parameters after the project is generated.

* **Requirements**: Update packages versions in the ``requirements/`` directory
  and ``setup.py``.

* **Bitbucket pipeline**: Update or change docker image and ``script`` steps.

* **Tox**: Update or change python versions.

* **.gitignore**: Add more entries if required. Make sure you add to correct
  place. Consider use global ``.gitignore`` for system-specific files and local
  one only for project-specific files. This article can help to figure out:
  https://gist.github.com/subfuzion/db7f57fff2fb6998a16c.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _pytest: https://docs.pytest.org/en/latest/
.. _tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.io/
.. _bumpversion: https://github.com/peritus/bumpversion
.. _click: https://click.palletsprojects.com/
.. _flake8: http://flake8.pycqa.org/en/latest/
