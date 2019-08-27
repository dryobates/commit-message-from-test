from click.testing import CliRunner

from cmft.cli import main


def test_shows_usage_when_no_default_message_provided():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code != 0
    assert result.output.startswith("Usage:")


def test_prints_on_stdout_default_message_when_not_in_git_repo():
    default_message = "some message"
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, [default_message])
        assert result.exit_code == 0
        assert "f{default_message}\n" == result.output


# - prints on stderr error when could not run git diff
# - prints on stdout default message when no test found in git diff
# - prints on stdout message based on test name when one test found in git diff
# - prints on stdout message based on first found test name when many tests found in git diff
# - runs git diff for given directory/file when path is given as option
# - test is method
# - test has arguments
# - test is commented
# - test contains "test" in name
# - test contains "def" in name
