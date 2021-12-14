import os.path as op

__base_version__ = "{{ cookiecutter.version }}"


def app_version():
    """Get ``{{ cookiecutter.package_name }}`` version."""
    root = op.abspath(op.join(op.dirname(__file__), "../../"))
    if op.exists(op.join(root, ".git")):
        from setuptools_scm import get_version

        return get_version(root=root, version_scheme=lambda x: __base_version__)
    else:
        try:
            from {{ cookiecutter.package_name }}._version import version

            return version
        except ImportError:
            return __base_version__


__version__ = app_version()
del op
del app_version
