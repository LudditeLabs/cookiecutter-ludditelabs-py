#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from setuptools import setup, find_packages

root = Path(__file__).parent


def get_base_version():
    filename = root / "src" / "{{ cookiecutter.package_name }}" / "__init__.py"
    with filename.open() as f:
        for line in f:
            if line.startswith("__base_version__"):
                return eval(line.split("=")[-1])


def read(*parts):
    return root.joinpath(*parts).read_text()


base_version = get_base_version()


setup(
    name="{{ cookiecutter.package_name }}",
    description="{{ cookiecutter.project_short_description }}",
    long_description=read("README.rst"),
    author="{{ cookiecutter.author.replace('\"', '\\\"') }}",
    author_email="{{ cookiecutter.email }}",
{%- if cookiecutter.project_url %}
    url="{{ cookiecutter.project_url }}",
{%- endif %}
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        {%- if cookiecutter.use_cli == 'y' %}
        "click",
        {%- endif %}
    ],
    setup_requires=["setuptools>=45", "wheel", "setuptools-scm>=6.2"],
    use_scm_version={
        "write_to": "./src/{{ cookiecutter.package_name }}/_version.py",
        "version_scheme": lambda x: base_version,
        "fallback_version": base_version,
    },
{%- if cookiecutter.use_cli == 'y' %}
    entry_points={
        "console_scripts": ["{{ cookiecutter.package_name }}={{ cookiecutter.package_name }}.__main__:cli"]
    },
{%- endif %}
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        {% if cookiecutter.license == 'MIT license' -%}
        "License :: OSI Approved :: MIT License",
        {% elif cookiecutter.license == 'BSD license' -%}
        "License :: OSI Approved :: BSD License",
        {% elif cookiecutter.license == 'Apache Software License 2.0' -%}
        "License :: OSI Approved :: Apache Software License",
        {% endif %}
    ],
)
