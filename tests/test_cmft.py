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


def test_outputs_default_message_when_no_tests_found(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo("#")

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert DEFAULT_MESSAGE == result.output


def test_outputs_message_based_on_test_name_when_one_test_found(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """
def test_name():
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert "name" == result.output


def test_outputs_message_based_on_first_found_test_name_when_many_tests_found(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """
def test_first():
    pass

def test_second():
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert "first" == result.output


def test_test_is_method(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """
class TestExample(TestCase):
    def test_name(self):
        pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert "name" == result.output


def test_does_not_include_function_arguments_in_message(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """
def test_name(self, args1):
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert "name" == result.output


def test_does_not_output_commented_tests(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """
# def test_first():
#    pass

def test_second():
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert "second" == result.output


def test_contains_test_in_name(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """
def test_test():
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert "test" == result.output


def test_contains_def_in_name(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """
def test_def():
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert "def" == result.output


def test_changes_underlines_to_spaces_in_message(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """
def test_snake_case():
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert "snake case" == result.output


# - runs git diff for given directory/file when path is given as option
# - snake case function name
# - camel case function name
# - file tracked and not staged


def _write_test_file_in_git_repo(content):
    run("git init .", shell=True)
    with open(TEST_FILE_NAME, "w") as test_file:
        test_file.write(content)
    run(f"git add {TEST_FILE_NAME}", shell=True)


@pytest.fixture
def runner():
    return CliRunner()
