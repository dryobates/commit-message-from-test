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
            message = camel_to_snake(match.group(1))
            message = UNDERLINES_RE.sub(" ", message).strip()
    click.echo(message, nl=False)


first_cap_re = re.compile(r'(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def camel_to_snake(s):
    subbed = first_cap_re.sub(r'\1_\2', s)
    return all_cap_re.sub(r'\1_\2', subbed).lower()


if __name__ == "__main__":
    main()
