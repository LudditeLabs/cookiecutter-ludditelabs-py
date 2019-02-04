#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path as op
from setuptools import setup, find_packages


def get_version(fname='src/{{ cookiecutter.package_name }}/__init__.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def read(*parts, **kwargs):
    return open(op.join(op.dirname(__file__), *parts)).read()

{%- set license_classifiers = {
    'MIT license': 'License :: OSI Approved :: MIT License',
    'BSD license': 'License :: OSI Approved :: BSD License',
    'Apache Software License 2.0': 'License :: OSI Approved :: Apache Software License',
} %}

setup(
    name='{{ cookiecutter.package_name }}',
    version=get_version(),
    description="{{ cookiecutter.project_short_description }}",
    long_description=read('README.rst'),
    author="{{ cookiecutter.author.replace('\"', '\\\"') }}",
    author_email='{{ cookiecutter.email }}',
{%- if cookiecutter.project_url %}
    url='{{ cookiecutter.project_url }}',
{%- endif %}
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        {% if cookiecutter.use_cli == 'y' %}'click>=6.0',{% endif %}
        {%- if cookiecutter.use_appconfig == 'y' %}
        'config-source',
        {%- if cookiecutter.use_appconfig_s3 == 'y' %}
        'config-source-s3',
        {%- endif %}
        {%- endif %}
    ],
{%- if cookiecutter.use_cli == 'y' %}
    entry_points={
        'console_scripts': ['{{ cookiecutter.package_name }}={{ cookiecutter.package_name }}.__main__:cli']
    },
{%- endif %}
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
{%- if cookiecutter.license in license_classifiers %}
        '{{ license_classifiers[cookiecutter.license] }}',
{%- endif %}
        'Programming Language :: Python :: 3',
    ],
{%- if cookiecutter.license in license_classifiers %}
    license="{{ cookiecutter.license }}",
{%- endif %}
)
