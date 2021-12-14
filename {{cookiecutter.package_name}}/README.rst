{{ '*' * (cookiecutter.project_title|length) }}
{{ cookiecutter.project_title }}
{{ '*' * (cookiecutter.project_title|length) }}

.. _overview:

Overview
========

This section provides an overview on main parts of the project.

Project layout
--------------

*{{ cookiecutter.project_title }}* uses so called "*src layout*", advantages are
described in this blog post:
https://blog.ionelmc.ro/2014/05/25/python-packaging/.

{%- set name_sz = cookiecutter.package_name|length + 3 %}
{% set sz = 2 + [name_sz, 13] | max %}
::

    docs/{{ ' ' * (sz - 5) }}- Project documentation.
    requirements/{{ ' ' * (sz - 13) }}- Project requirements.
    src/
      {{ cookiecutter.package_name }}/{{ ' ' * (sz - name_sz) }}- Project sources.
    tests/{{ ' ' * (sz - 6) }}- Project tests.

Installation
------------

{% if cookiecutter %}
Create conda environment and install ``{{ cookiecutter.package_name }}`` there. You can use production and
development environments::

    # Create development environment.
    $ conda env create -n {{ cookiecutter.package_name }} --file requirements/development.yml

    # Or create production environment.
    $ conda env create -n {{ cookiecutter.package_name }} --file requirements/production.yml

    $ conda activate {{ cookiecutter.package_name }}
    $ pip install -e src/{{ cookiecutter.package_name }}

{% else %}
Project installation is performing with requirements files::

    $ pip install -r requirements/<name>.txt

Requirement file contains list of dependencies to install and allows to setup
runtime environment for the project. There are multiple environments, install
one of it depending on your needs.

Requirements layout::

    requirements/
        base.txt    - {{ cookiecutter.package_name }} dependencies.
        app.txt     - Production environment.
        app-dev.txt - Production environment, but {{ cookiecutter.package_name }} is installed in
                      development mode.
        dev.txt     - Development environment.
        test.txt    - Testing environment, used to run tests.

For example, to prepare environment for users you need to run::

    $ pip install -r requirements/app.txt

If you are developer then run::

    $ pip install -r requirements/dev.txt

Also common recommendation is to setup separate python environment for
applications and then install the application and its dependencies to this
environment::

    $ python3 -m venv /path/to/venv
    $ source /path/to/venv/bin/activate
    $ pip install -r requirements/app.txt
{% endif %}

{% if cookiecutter.use_cli == 'y' -%}
After installation you can run commands with::

    $ {{ cookiecutter.package_name }} <commands> ...
    $ {{ cookiecutter.package_name }} --help

{% endif -%}
Uninstall ``{{ cookiecutter.package_name }}`` with::

    $ pip uninstall {{ cookiecutter.package_name }}

Documentation
-------------

Project documentation is located in the ``docs/`` directory.

`Sphinx <http://sphinx-doc.org>`_ is used to generate HTML documentation::

    $ cd docs
    $ make html

Above command generates HTML documentation in the ``docs/_build/html``
directory.

Code Style
----------

This project is developing using `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_
style with help of `black <https://github.com/psf/black>`_ and
`isort <https://github.com/PyCQA/isort>`_.

Use the following command to check source code before committing changes::

    $ isort src tests
    $ black src tests

Git commit messages follows these guidelines:
https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53.

Tests
-----

Tests are located in the ``tests/`` directory and implemented with
`PyTests <pytest.org>`_ framework.

You could run specific tests with ``pytest`` or all tests in different
enviroments with ``tox``::

    # Run all tests.
    $ pytest tests

    # Run single test case.
    $ pytest tests/test_<name>.py

    # Run tests with coverage report.
    $ pytest --cov={{ cookiecutter.package_name }} ...

    # Run all tests with tox.
    $ tox
