from subprocess import run

import pytest
from click.testing import CliRunner

from cmft.cli import main

DEFAULT_MESSAGE = "some message"
TEST_FILE_NAME = "test_example.py"


def test_shows_usage_when_no_default_message_provided(runner):
    result = runner.invoke(main, [])

    assert result.exit_code != 0
    assert result.output.startswith("Usage:")


def test_outputs_default_message_when_not_in_git_repository(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert DEFAULT_MESSAGE == result.output


def test_outputs_default_message_when_no_commits(runner):
    with runner.isolated_filesystem():
        run("git init .", shell=True)
        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert DEFAULT_MESSAGE == result.output


def test_outputs_message_from_staged_files(runner):
    file_content = """\
def testname():
    pass"""
    with runner.isolated_filesystem():
        _write_test_file_content(file_content)
        run(f"git add {TEST_FILE_NAME}", shell=True)

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert "name" == result.output


def test_outputs_message_from_not_staged_files(runner):
    file_content = """\
def testname():
    pass"""
    with runner.isolated_filesystem():
        _write_test_file_content(file_content)

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert "name" == result.output


# - runs git diff for given directory/file when path is given as option
# - recognize different languages


def _write_test_file_content(file_content):
    _init_repo()
    with open(TEST_FILE_NAME, "w") as test_file:
        test_file.write(file_content)


def _init_repo():
    run("git init .", shell=True)
    run(f"touch {TEST_FILE_NAME}", shell=True)
    run(f"git add {TEST_FILE_NAME}", shell=True)
    run(f"git commit -m 'init' {TEST_FILE_NAME}", shell=True)


@pytest.fixture
def runner():
    return CliRunner()
