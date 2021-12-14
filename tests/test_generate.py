import pytest
import datetime
import os
import re
import shlex
import subprocess
from contextlib import contextmanager
from cookiecutter.utils import rmtree

# TODO: add tests for project_title, project_short_description, package_name,
#       author, email, version.

# TODO: test CLI running.

# -- Utils --------------------------------------------------------------------

@contextmanager
def cwd(path):
    """Temporary change current working directory.

    Args:
        path: Working directory path.
    """
    old_path = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def project(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def run_command(command, path):
    """Run a command from inside a given directory.

    Args:
        command: Command to run.
        path: Working directory.

    Returns:
        Exit status of the command.
    """
    with cwd(path):
        return subprocess.check_call(shlex.split(command))


# -- Tests --------------------------------------------------------------------

# Test: check if package dir exists.
def test_package_dir(cookies):
    with project(cookies) as result:
        path = result.project.join('src', result.project.basename)
        assert path.exists()


# Test: check if generated test is correct.
def test_run_tests(cookies):
    with project(cookies) as result:
        assert run_command('pytest tests', str(result.project)) == 0


# Test: check if docs can be generated.
def test_run_docs(cookies):
    with project(cookies) as result:
        assert run_command('make html', str(result.project.join('docs'))) == 0


# Test: use_bitbucket_pipelines flag (create or not bitbucket-pipelines.yml).
@pytest.mark.parametrize('use', ['y', 'n'])
def test_use_bitbucket_pipelines(cookies, use):
    ctx = dict(use_bitbucket_pipelines=use)
    with project(cookies, extra_context=ctx) as result:
        path = result.project.join('bitbucket-pipelines.yml')
        assert path.exists() is (use == 'y')


# Test: use_travis flag (create or not .travis.yml).
@pytest.mark.parametrize('use', ['y', 'n'])
def test_use_travis(cookies, use):
    ctx = dict(use_travis=use)
    with project(cookies, extra_context=ctx) as result:
        path = result.project.join('.travis.yml')
        assert path.exists() is (use == 'y')


# Test: sphinx_use_apidoc flag, configure or not apidoc.
@pytest.mark.parametrize('use', ['y', 'n'])
def test_sphinx_use_apidoc(cookies, use):
    ctx = dict(sphinx_use_apidoc=use)
    state = use == 'y'

    with project(cookies, extra_context=ctx) as result:
        path = result.project.join('docs', 'conf.py')
        assert (("app.connect('builder-inited', run_apidoc)" in path.read())
                is state)

        path = result.project.join('docs', 'index.rst')
        assert ("_apidoc/modules" in path.read()) is state


# Test: use_cli flag, setup CLI support.
@pytest.mark.parametrize('use', ['y', 'n'])
def test_use_cli(cookies, use):
    ctx = dict(use_cli=use, package_name='mypkg')
    state = use == 'y'

    with project(cookies, extra_context=ctx) as result:
        path = result.project.join('setup.py')
        assert ('entry_points' in path.read()) is state

        path = result.project.join('src', 'mypkg', '__main__.py')
        assert path.exists() is state

        path = result.project.join('src', 'mypkg', 'cli.py')
        assert path.exists() is state


# Test: use_cli flag, setup CLI support.
@pytest.mark.parametrize(
    'use,paths',
    (
        (
            'y',
            [
                'production.yml',
                'dev.yml',
                'test.yml',
            ],
        ),
        (
            'n',
            [
                'app.txt',
                'app-dev.txt',
                'base.txt',
                'dev.txt',
                'test.txt',
            ]
        ),
    )
)
def test_use_conda(cookies, use, paths):
    ctx = dict(use_conda=use, package_name='mypkg')

    with project(cookies, extra_context=ctx) as result:
        actual = sorted(str(x) for x in os.listdir(result.project.join('requirements')))
        assert sorted(paths) == actual


# Test: LICENSE file generating.
class TestLicense:
    # Test: is file exists after generating.
    @pytest.mark.parametrize('license, state', [
        ('No license', False),
        ('Apache Software License 2.0', True),
        ('MIT license', True),
        ('BSD license', True)
    ])
    def test_generated(self, cookies, license, state):
        ctx = dict(license=license)
        with project(cookies, extra_context=ctx) as result:
            path = result.project.join('LICENSE')
            assert path.exists() is state

    # Test: check year in the license file.
    @pytest.mark.parametrize('license', [
        'Apache Software License 2.0',
        'MIT license',
        'BSD license'
    ])
    def test_year(self, cookies, license):
        with project(cookies, extra_context=dict(license=license)) as result:
            path = result.project.join('LICENSE')
            now = datetime.datetime.now()
            assert 'Copyright (c) %d' % now.year in path.read()

    # Test: is file exists after generating.
    @pytest.mark.parametrize('license, text', [
        ('No license', ''),
        (
            'Apache Software License 2.0',
            '"License :: OSI Approved :: Apache Software License",'
        ),
        ('MIT license', '"License :: OSI Approved :: MIT License",'),
        ('BSD license', '"License :: OSI Approved :: BSD License",')
    ])
    def test_setup(self, cookies, license, text):
        pattern = f'"Programming Language :: Python :: 3",\n\s+{text}\n\s+]'
        ctx = dict(license=license)
        with project(cookies, extra_context=ctx) as result:
            path = result.project.join('setup.py')
            content = path.read()
            m = re.search(pattern, content)
            assert m is not None


# Test: set project URL.
@pytest.mark.parametrize('url', ['', 'http://example.com'])
def test_url(cookies, url):
    ctx = dict(project_url=url)
    state = len(url) != 0

    with project(cookies, extra_context=ctx) as result:
        path = result.project.join('setup.py')
        assert ('url=' in path.read()) is state
