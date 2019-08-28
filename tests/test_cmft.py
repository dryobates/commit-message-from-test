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
def testname():
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
def testfirst():
    pass

def testsecond():
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert "first" == result.output


def test_test_is_method(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """
class TestExample(TestCase):
    def testname(self):
        pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert "name" == result.output


def test_does_not_include_function_arguments_in_message(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """
def testname(self, args1):
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert "name" == result.output


def test_does_not_output_commented_tests(runner):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            """
# def testfirst():
#    pass

def testsecond():
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert "second" == result.output


@pytest.mark.parametrize("word", ["def", "test"])
def test_contains_test_definition_words_in_name(runner, word):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            f"""
def test{word}():
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert word == result.output


@pytest.mark.parametrize(
    "test_name", ["snake_case", "snake__case", "_snake_case", "snake_case_"]
)
def test_changes_underlines_to_spaces_in_message(runner, test_name):
    with runner.isolated_filesystem():
        _write_test_file_in_git_repo(
            f"""
def test{test_name}():
    pass
        """
        )

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert "snake case" == result.output


# - runs git diff for given directory/file when path is given as option
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
