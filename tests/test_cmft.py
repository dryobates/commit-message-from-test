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
    file_content = """\
def testname():
    pass"""
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(file_content)

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert "name" == result.output


def test_checks_diff_between_tracked_files_in_workdir_and_head(runner):
    file_content = """\
def testname():
    pass"""
    with runner.isolated_filesystem():
        _init_repo()
        with open(TEST_FILE_NAME, "w") as test_file:
            test_file.write(file_content)

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert "name" == result.output


# - runs git diff for given directory/file when path is given as option
# - recognize different languages
# - no git repository
# - no commit in git repository


def _write_test_file_in_git_repo(content):
    _init_repo()
    with open(TEST_FILE_NAME, "w") as test_file:
        test_file.write(content)
    run(f"git add {TEST_FILE_NAME}", shell=True)


def _init_repo():
    run("git init .", shell=True)
    run(f"touch {TEST_FILE_NAME}", shell=True)
    run(f"git add {TEST_FILE_NAME}", shell=True)
    run(f"git commit -m 'init' {TEST_FILE_NAME}", shell=True)


@pytest.fixture
def runner():
    return CliRunner()
