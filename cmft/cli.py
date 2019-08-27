import re
from subprocess import CalledProcessError, run

import click

TEST_RE = re.compile(r"^\+def test_*(.*)$", re.MULTILINE)


@click.command()
@click.argument("message")
def main(message):
    try:
        output = run("git diff --cached", shell=True, check=True, capture_output=True, encoding="utf8").stdout
    except CalledProcessError:
        click.echo(message, nl=False)
    else:
        match = TEST_RE.search(output)
        if match:
            click.echo(match.group(1), nl=False)
        else:
            click.echo(message, nl=False)


if __name__ == "__main__":
    main()
