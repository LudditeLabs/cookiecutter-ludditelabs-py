import pytest
import datetime
import os
import re
import shlex
import subprocess
from contextlib import contextmanager
from cookiecutter.utils import rmtree


# TODO: add tests for project_title, project_short_description, project_slug,
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
    if result.exception is not None:
        raise result.exception
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
        return subprocess.check_call(shlex.split(command), shell=True)


# -- Tests --------------------------------------------------------------------


# Test: check if package dir exists.
def test_package_dir(cookies):
    with project(cookies) as result:
        path = result.project.join("src", result.project.basename)
        assert path.exists()


# Test: check if generated test is correct.
def test_run_tests(cookies):
    with project(cookies) as result:
        env = os.environ.copy()
        env["POETRY_VIRTUALENVS_IN_PROJECT"] = "1"
        res = subprocess.run(
            ["poetry", "install", "--with", "test"],
            env=env,
            cwd=result.project,
            capture_output=True,
        )
        assert res.returncode == 0, res.stderr

        res = subprocess.run(
            ["poetry", "run", "pytest", "tests"],
            env=env,
            cwd=result.project,
            capture_output=True,
        )
        assert res.returncode == 0, res.stderr


# Test: check if docs can be generated.
def test_run_docs(cookies):
    with project(cookies) as result:
        env = os.environ.copy()
        env["POETRY_VIRTUALENVS_IN_PROJECT"] = "1"
        res = subprocess.run(
            ["poetry", "install", "--with", "doc"],
            env=env,
            cwd=result.project,
            capture_output=True,
        )
        assert res.returncode == 0, res.stderr

        res = subprocess.run(
            ["poetry", "run", "make", "html"],
            env=env,
            cwd=result.project / "docs",
            capture_output=True,
        )
        assert res.returncode == 0, res.stderr


# Test: with_bitbucket_pipelines flag (create or not bitbucket-pipelines.yml).
@pytest.mark.parametrize("use", [True, False])
def test_with_bitbucket_pipelines(cookies, use):
    ctx = dict(with_bitbucket_pipelines=use)
    with project(cookies, extra_context=ctx) as result:
        path = result.project / "bitbucket-pipelines.yml"
        assert path.exists() is use


# Test: with_cli flag, setup CLI support.
@pytest.mark.parametrize("use", [True, False])
def test_with_cli(cookies, use):
    ctx = dict(with_cli=use, project_slug="my_pkg")

    with project(cookies, extra_context=ctx) as result:
        filename = result.project / "pyproject.toml"
        content = filename.read()

        assert ("my-pkg = 'my_pkg.__main__:run'" in content) is use
        assert ('click = "^8.1.3"' in content) is use

        filename = result.project / "src" / "my_pkg" / "__main__.py"
        assert filename.exists() is use

        filename = result.project / "src" / "my_pkg" / "cli.py"
        assert filename.exists() is use


# Test: LICENSE file generating.
class TestLicense:
    # Test: is file exists after generating.
    @pytest.mark.parametrize(
        "license, state",
        [
            ("No license", False),
            ("Apache Software License 2.0", True),
            ("MIT license", True),
            ("BSD license", True),
        ],
    )
    def test_generated(self, cookies, license, state):
        ctx = dict(license=license)
        with project(cookies, extra_context=ctx) as result:
            path = result.project / "LICENSE"
            assert path.exists() is state

    # Test: check year in the license file.
    @pytest.mark.parametrize(
        "license", ["Apache Software License 2.0", "MIT license", "BSD license"]
    )
    def test_year(self, cookies, license):
        with project(cookies, extra_context=dict(license=license)) as result:
            content = (result.project / "LICENSE").read()
            now = datetime.datetime.now()
            assert "Copyright (c) %d" % now.year in content

    # Test: License in classifiers.
    @pytest.mark.parametrize(
        "license, text",
        [
            ("No license", ""),
            (
                "Apache Software License 2.0",
                "License :: OSI Approved :: Apache Software License",
            ),
            ("MIT license", "License :: OSI Approved :: MIT License"),
            ("BSD license", "License :: OSI Approved :: BSD License"),
        ],
    )
    def test_classifiers(self, cookies, license, text):
        postfix = "Programming Language :: Python :: 3"

        if text:
            pattern = rf'classifiers=\[\n\s+"{text}",\n\s+"{postfix}"'
        else:
            pattern = rf'classifiers=\[\n\s+"{postfix}"'

        ctx = dict(license=license)
        with project(cookies, extra_context=ctx) as result:
            content = (result.project / "pyproject.toml").read()
            m = re.search(pattern, content)
            assert m is not None


# Test: set project URL.
@pytest.mark.parametrize("url", ["", "http://example.com"])
def test_url(cookies, url):
    ctx = dict(project_url=url)
    state = len(url) != 0

    with project(cookies, extra_context=ctx) as result:
        content = (result.project / "pyproject.toml").read()
        assert ("homepage =" in content) is state
