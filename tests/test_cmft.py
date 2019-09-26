from subprocess import run

import pytest
from click.testing import CliRunner

from cmft.cli import main

TEST_FILE_NAME = "test_example.py"


def test_outputs_no_message_when_not_in_git_repository(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(main)

        assert result.exit_code == 0
        assert "" == result.output


def test_outputs_no_message_when_no_commits(runner):
    with runner.isolated_filesystem():
        run("git init .", shell=True)
        result = runner.invoke(main)

        assert result.exit_code == 0
        assert "" == result.output


def test_outputs_message_from_staged_files(runner):
    file_content = """\
def testname():
    pass"""
    with runner.isolated_filesystem():
        _write_test_file_content_in_repo(file_content)
        run(f"git add {TEST_FILE_NAME}", shell=True)

        result = runner.invoke(main)

        assert result.exit_code == 0
        assert "name" == result.output


def test_outputs_message_from_not_staged_files(runner):
    file_content = """\
def testname():
    pass"""
    with runner.isolated_filesystem():
        _write_test_file_content_in_repo(file_content)

        result = runner.invoke(main)

        assert result.exit_code == 0
        assert "name" == result.output


def test_outputs_all_possible_messages(runner):
    first_file_name = "test_first_example.py"
    first_file_content = """\
def test_first():
    pass"""
    second_file_name = "test_second_example.py"
    second_file_content = """\
def test_second():
    pass"""
    with runner.isolated_filesystem():
        _write_test_file_content_in_repo(first_file_content, first_file_name)
        _write_test_file_content_in_repo(second_file_content, second_file_name)
        run(f"git add {first_file_name}", shell=True)
        run(f"git add {second_file_name}", shell=True)

        result = runner.invoke(main)

        assert result.exit_code == 0
        assert "first\nsecond" == result.output


# - runs git diff for given directory/file when path is given as option
# - recognize different languages


def _write_test_file_content_in_repo(file_content, file_name=TEST_FILE_NAME):
    _init_repo()
    with open(file_name, "w") as test_file:
        test_file.write(file_content)


def _init_repo():
    run("git init .", shell=True)
    run(f"touch {TEST_FILE_NAME}", shell=True)
    run(f"git add {TEST_FILE_NAME}", shell=True)
    run(f"git commit -m 'init' {TEST_FILE_NAME}", shell=True)


@pytest.fixture
def runner():
    return CliRunner()
