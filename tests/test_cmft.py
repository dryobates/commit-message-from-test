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
        run("git init .", shell=True)
        with open(TEST_FILE_NAME, "w") as test_file:
            test_file.write("#")
        run(f"git add {TEST_FILE_NAME}", shell=True)

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert DEFAULT_MESSAGE == result.output


def test_outputs_message_based_on_test_name_when_one_test_found(runner):
    with runner.isolated_filesystem():
        run("git init .", shell=True)
        with open(TEST_FILE_NAME, "w") as test_file:
            test_file.write("def test_name")
        run(f"git add {TEST_FILE_NAME}", shell=True)

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert "name" == result.output


def test_outputs_message_based_on_first_found_test_name_when_many_tests_found(runner):
    with runner.isolated_filesystem():
        run("git init .", shell=True)
        with open(TEST_FILE_NAME, "w") as test_file:
            test_file.write("def test_first\n")
            test_file.write("def test_second\n")
        run(f"git add {TEST_FILE_NAME}", shell=True)

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert "first" == result.output


def test_test_is_method(runner):
    with runner.isolated_filesystem():
        run("git init .", shell=True)
        with open(TEST_FILE_NAME, "w") as test_file:
            test_file.write(
                """
    class TestExample(TestCase):
        def test_name(self):
            pass
                """
            )
        run(f"git add {TEST_FILE_NAME}", shell=True)

        result = runner.invoke(main, [DEFAULT_MESSAGE])

        assert result.exit_code == 0
        assert "name" == result.output


# - runs git diff for given directory/file when path is given as option
# - test has arguments
# - test is commented
# - test contains "test" in name
# - test contains "def" in name
# - snake case function name
# - camel case function name
# - file tracked and not staged


@pytest.fixture
def runner():
    return CliRunner()
