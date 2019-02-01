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


# Test: use_bitbucket_pipeline flag (create or not bitbucket-pipelines.yml).
@pytest.mark.parametrize('use', ['y', 'n'])
def test_use_bitbucket_pipeline(cookies, use):
    ctx = dict(use_bitbucket_pipeline=use)
    with project(cookies, extra_context=ctx) as result:
        path = result.project.join('bitbucket-pipelines.yml')
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

#
# def project_info(result):
#     """Get toplevel dir, project_slug, and project dir from baked cookies"""
#     project_path = str(result.project)
#     project_slug = os.path.split(project_path)[-1]
#     project_dir = os.path.join(project_path, project_slug)
#     return project_path, project_slug, project_dir
#
#
# def test_bake_with_defaults(cookies):
#     with project(cookies) as result:
#         assert result.project.isdir()
#         assert result.exit_code == 0
#         assert result.exception is None
#
#         found_toplevel_files = [f.basename for f in result.project.listdir()]
#         assert 'setup.py' in found_toplevel_files
#         assert 'python_boilerplate' in found_toplevel_files
#         assert 'tox.ini' in found_toplevel_files
#         assert 'tests' in found_toplevel_files
#
#
# def test_bake_and_run_tests(cookies):
#     with project(cookies) as result:
#         assert result.project.isdir()
#         run_inside_dir('python setup.py test', str(result.project)) == 0
#         print("test_bake_and_run_tests path", str(result.project))
#
#
# def test_bake_withspecialchars_and_run_tests(cookies):
#     """Ensure that a `full_name` with double quotes does not break setup.py"""
#     with project(cookies, extra_context={'full_name': 'name "quote" name'}) as result:
#         assert result.project.isdir()
#         run_inside_dir('python setup.py test', str(result.project)) == 0
#
#
# def test_bake_with_apostrophe_and_run_tests(cookies):
#     """Ensure that a `full_name` with apostrophes does not break setup.py"""
#     with project(cookies, extra_context={'full_name': "O'connor"}) as result:
#         assert result.project.isdir()
#         run_inside_dir('python setup.py test', str(result.project)) == 0
#
#
# def test_bake_without_travis_pypi_setup(cookies):
#     with project(cookies, extra_context={'use_pypi_deployment_with_travis': 'n'}) as result:
#         result_travis_config = yaml.load(result.project.join(".travis.yml").open())
#         assert "deploy" not in result_travis_config
#         assert "python" == result_travis_config["language"]
#         found_toplevel_files = [f.basename for f in result.project.listdir()]
#
#
# def test_bake_without_author_file(cookies):
#     with project(cookies, extra_context={'create_author_file': 'n'}) as result:
#         found_toplevel_files = [f.basename for f in result.project.listdir()]
#         assert 'AUTHORS.rst' not in found_toplevel_files
#         doc_files = [f.basename for f in result.project.join('docs').listdir()]
#         assert 'authors.rst' not in doc_files
#
#         # Assert there are no spaces in the toc tree
#         docs_index_path = result.project.join('docs/index.rst')
#         with open(str(docs_index_path)) as index_file:
#             assert 'contributing\n   history' in index_file.read()
#
#         # Check that
#         manifest_path = result.project.join('MANIFEST.in')
#         with open(str(manifest_path)) as manifest_file:
#             assert 'AUTHORS.rst' not in manifest_file.read()
#
#
# def test_make_help(cookies):
#     with project(cookies) as result:
#         output = check_output_inside_dir('make help', str(result.project))
#         assert b"check code coverage quickly with the default Python" in output
#
#
# def test_bake_selecting_license(cookies):
#     license_strings = {
#         'MIT license': 'MIT ',
#         'BSD license': 'Redistributions of source code must retain the above copyright notice, this',
#         'ISC license': 'ISC License',
#         'Apache Software License 2.0': 'Licensed under the Apache License, Version 2.0',
#         'GNU General Public License v3': 'GNU GENERAL PUBLIC LICENSE',
#     }
#     for license, target_string in license_strings.items():
#         with project(cookies, extra_context={'open_source_license': license}) as result:
#             assert target_string in result.project.join('LICENSE').read()
#             assert license in result.project.join('setup.py').read()
#
#
# def test_bake_not_open_source(cookies):
#     with project(cookies, extra_context={'open_source_license': 'Not open source'}) as result:
#         found_toplevel_files = [f.basename for f in result.project.listdir()]
#         assert 'setup.py' in found_toplevel_files
#         assert 'LICENSE' not in found_toplevel_files
#         assert 'License' not in result.project.join('README.rst').read()
#
#
# def test_using_pytest(cookies):
#     with project(cookies, extra_context={'use_pytest': 'y'}) as result:
#         assert result.project.isdir()
#         test_file_path = result.project.join('tests/test_python_boilerplate.py')
#         lines = test_file_path.readlines()
#         assert "import pytest" in ''.join(lines)
#         # Test the new pytest target
#         run_inside_dir('python setup.py pytest', str(result.project)) == 0
#         # Test the test alias (which invokes pytest)
#         run_inside_dir('python setup.py test', str(result.project)) == 0
#
#
# def test_not_using_pytest(cookies):
#     with project(cookies) as result:
#         assert result.project.isdir()
#         test_file_path = result.project.join('tests/test_python_boilerplate.py')
#         lines = test_file_path.readlines()
#         assert "import unittest" in ''.join(lines)
#         assert "import pytest" not in ''.join(lines)
#
#
# def test_bake_with_no_console_script(cookies):
#     context = {'command_line_interface': "No command-line interface"}
#     result = cookies.bake(extra_context=context)
#     project_path, project_slug, project_dir = project_info(result)
#     found_project_files = os.listdir(project_dir)
#     assert "cli.py" not in found_project_files
#
#     setup_path = os.path.join(project_path, 'setup.py')
#     with open(setup_path, 'r') as setup_file:
#         assert 'entry_points' not in setup_file.read()
#
#
# def test_bake_with_console_script_files(cookies):
#     context = {'command_line_interface': 'click'}
#     result = cookies.bake(extra_context=context)
#     project_path, project_slug, project_dir = project_info(result)
#     found_project_files = os.listdir(project_dir)
#     assert "cli.py" in found_project_files
#
#     setup_path = os.path.join(project_path, 'setup.py')
#     with open(setup_path, 'r') as setup_file:
#         assert 'entry_points' in setup_file.read()
#
#
# def test_bake_with_console_script_cli(cookies):
#     context = {'command_line_interface': 'click'}
#     result = cookies.bake(extra_context=context)
#     project_path, project_slug, project_dir = project_info(result)
#     module_path = os.path.join(project_dir, 'cli.py')
#     module_name = '.'.join([project_slug, 'cli'])
#     if sys.version_info >= (3, 5):
#         spec = importlib.util.spec_from_file_location(module_name, module_path)
#         cli = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(cli)
#     elif sys.version_info >= (3, 3):
#         file_loader = importlib.machinery.SourceFileLoader
#         cli = file_loader(module_name, module_path).load_module()
#     else:
#         cli = imp.load_source(module_name, module_path)
#     runner = CliRunner()
#     noarg_result = runner.invoke(cli.main)
#     assert noarg_result.exit_code == 0
#     noarg_output = ' '.join(['Replace this message by putting your code into', project_slug])
#     assert noarg_output in noarg_result.output
#     help_result = runner.invoke(cli.main, ['--help'])
#     assert help_result.exit_code == 0
#     assert 'Show this message' in help_result.output
