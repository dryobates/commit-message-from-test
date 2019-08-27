from subprocess import run

import pytest
from click.testing import CliRunner

from cmft.cli import main


def test_shows_usage_when_no_default_message_provided(runner):
    result = runner.invoke(main, [])

    assert result.exit_code != 0
    assert result.output.startswith("Usage:")


def test_prints_on_stdout_default_message_when_could_not_run_git_diff(runner):
    default_message = "some message"
    with runner.isolated_filesystem():

        result = runner.invoke(main, [default_message])

        assert result.exit_code == 0
        assert f"{default_message}\n" == result.output


def test_prints_on_stdout_default_message_when_no_tests_found_in_git_diff(runner):
    default_message = "some message"
    with runner.isolated_filesystem():
        run("git init .", shell=True)
        run("touch test_example.py", shell=True)
        run("git add test_example.py", shell=True)

        result = runner.invoke(main, [default_message])

        assert result.exit_code == 0
        assert f"{default_message}\n" == result.output


def test_prints_on_stdout_message_based_on_test_name_when_one_test_found_in_git_diff(runner):
    default_message = "some message"
    with runner.isolated_filesystem():
        run("git init .", shell=True)
        with open("test_example.py", "w") as test_file:
            test_file.write("def test_name")
        run("git add test_example.py", shell=True)

        result = runner.invoke(main, [default_message])

        assert result.exit_code == 0
        assert "name" == result.output

# - prints on stdout message based on first found test name when many tests found in git diff
# - runs git diff for given directory/file when path is given as option
# - test is method
# - test has arguments
# - test is commented
# - test contains "test" in name
# - test contains "def" in name


@pytest.fixture
def runner():
    return CliRunner()
