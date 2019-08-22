from click.testing import CliRunner

from cmft.cli import main


def test_shows_usage_when_no_default_message_provided():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code != 0
    assert result.output.startswith('Usage:')

# - prints on stdout default message when no test found in git diff
# - prints on stdout message based on test name when one test found in git diff
# - prints on stdout message based on first found test name when many tests found in git diff
# - runs git diff for given directory/file when path is given as option
