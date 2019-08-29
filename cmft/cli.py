import re
from subprocess import CalledProcessError, run

import click

TEST_RE = re.compile(r"^\+\s*def test(.*)\(", re.MULTILINE)
UNDERLINES_RE = re.compile("_+")
FIRST_CAP_RE = re.compile(r"(.)([A-Z][a-z]+)")
ALL_CAP_RE = re.compile("([a-z0-9])([A-Z])")


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
            message = camel_to_snake(match.group(1))
            message = UNDERLINES_RE.sub(" ", message).strip()
    click.echo(message, nl=False)


def camel_to_snake(message):
    message = FIRST_CAP_RE.sub(r"\1_\2", message)
    return ALL_CAP_RE.sub(r"\1_\2", message).lower()


def snake_to_words(message):
    return UNDERLINES_RE.sub(" ", message).strip()


if __name__ == "__main__":
    main()
