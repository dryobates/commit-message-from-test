import re
from subprocess import CalledProcessError, run

import click

TEST_RE = re.compile(r"^\+\s*def test(.*)\(", re.MULTILINE)
UNDERLINES_RE = re.compile("_+")


@click.command()
@click.argument("message")
def main(message):
    try:
        output = run(
            "git diff --cached",
            shell=True,
            check=True,
            capture_output=True,
            encoding="utf8",
        ).stdout
    except CalledProcessError:
        pass
    else:
        match = TEST_RE.search(output)
        if match:
            message = match.group(1)
            message = UNDERLINES_RE.sub(" ", message).strip()
    click.echo(message, nl=False)


if __name__ == "__main__":
    main()
