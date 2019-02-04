import pytest
from contextlib import contextmanager
import datetime
import os
import shlex
import subprocess
from cookiecutter.utils import rmtree

# TODO: add tests for project_title, project_short_description, package_name,
#       author, email, version.


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
        assert run_command('py.test tests', str(result.project)) == 0


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


# Test: use_logging flag.
@pytest.mark.parametrize('use', ['y', 'n'])
def test_use_logging(cookies, use):
    ctx = dict(use_logging=use, package_name='mypkg')
    state = use == 'y'

    with project(cookies, extra_context=ctx) as result:
        path = result.project.join('src', 'mypkg', 'utils', 'logging.py')
        assert path.exists() is state


# Test: use_appconfig flag.
@pytest.mark.parametrize('use', ['y', 'n'])
def test_use_appconfig(cookies, use):
    ctx = dict(use_appconfig=use, package_name='mypkg')
    state = use == 'y'

    with project(cookies, extra_context=ctx) as result:
        path = result.project.join('setup.py')
        assert ("'config-source'" in path.read()) is state

        path = result.project.join('src', 'mypkg', 'utils', 'config.py')
        assert path.exists() is state

        path = result.project.join('requirements', 'base.txt')
        assert ('config-source=' in path.read()) is state


# Test: use_appconfig_s3 flag.
@pytest.mark.parametrize('use,use_s3', [
    ('y', 'y'),
    ('y', 'n'),
    ('n', 'n'),
    ('n', 'y')
])
def test_use_appconfig_s3(cookies, use, use_s3):
    ctx = dict(use_appconfig=use, use_appconfig_s3=use_s3, package_name='mypkg')
    state_s3 = use == 'y' and use_s3 == 'y'

    with project(cookies, extra_context=ctx) as result:
        path = result.project.join('setup.py')
        assert ("'config-source-s3'" in path.read()) is state_s3

        path = result.project.join('requirements', 'base.txt')
        assert ('config-source-s3=' in path.read()) is state_s3


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


# Test: set project URL.
@pytest.mark.parametrize('url', ['', 'http://example.com'])
def test_url(cookies, url):
    ctx = dict(project_url=url)
    state = len(url) != 0

    with project(cookies, extra_context=ctx) as result:
        path = result.project.join('setup.py')
        assert ('url=' in path.read()) is state
