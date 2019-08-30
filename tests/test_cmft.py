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


def test_outputs_default_message_when_could_not_run_git_diff(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert DEFAULT_MESSAGE == result.output


def test_output_message_based_on_test_found_in_git_diff(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """\
def testname():
    pass"""
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert "name" == result.output


# - file tracked and not staged
# - runs git diff for given directory/file when path is given as option
# - recognize different languages


def _write_test_file_in_git_repo(content):
    run("git init .", shell=True)
    with open(TEST_FILE_NAME, "w") as test_file:
        test_file.write(content)
    run(f"git add {TEST_FILE_NAME}", shell=True)


@pytest.fixture
def runner():
    return CliRunner()
