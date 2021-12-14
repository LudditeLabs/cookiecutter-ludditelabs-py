import os
from pathlib import Path

root_dir = os.path.realpath(os.path.curdir)
package_dir = Path(root_dir, 'src', '{{ cookiecutter.package_name }}')


class PathsRemover:
    """Helper to remove added paths."""

    def __init__(self):
        self.paths = []

    def add_from_root(self, *args):
        """Add path relative to package root directory.

        Args:
            args: Path segments.
        """
        self.paths.append(Path(root_dir, *args))

    def add_from_package(self, *args):
        """Add path relative to package source directory.

        Args:
            args: Path segments.
        """
        self.paths.append(Path(package_dir, *args))

    def remove(self):
        """Remove added paths."""
        for path in self.paths:
            if path.is_dir():
                path.rmdir()
            else:
                path.unlink()

    def remove_empty_package(self, *args):
        pkg = Path(package_dir, *args)
        files = list(pkg.iterdir())
        init_file = Path(pkg, '__init__.py')

        if not files or files == [init_file]:
            init_file.unlink()
            pkg.rmdir()


if __name__ == '__main__':
    paths = PathsRemover()

    if '{{ cookiecutter.use_bitbucket_pipelines }}' != 'y':
        paths.add_from_root('bitbucket-pipelines.yml')

    if '{{ cookiecutter.use_travis }}' != 'y':
        paths.add_from_root('.travis.yml')

    if '{{ cookiecutter.use_cli }}' != 'y':
        paths.add_from_package('cli.py')
        paths.add_from_package('__main__.py')

    if '{{ cookiecutter.license }}' == 'No license':
        paths.add_from_root('LICENSE')

    if '{{ cookiecutter.use_conda }}' == 'y':
        paths.add_from_root('requirements', 'app.txt')
        paths.add_from_root('requirements', 'app-dev.txt')
        paths.add_from_root('requirements', 'base.txt')
        paths.add_from_root('requirements', 'dev.txt')
        paths.add_from_root('requirements', 'test.txt')
    else:
        paths.add_from_root('requirements', 'production.yml')
        paths.add_from_root('requirements', 'dev.yml')
        paths.add_from_root('requirements', 'test.yml')

    paths.remove()
