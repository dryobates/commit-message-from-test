from subprocess import CalledProcessError, run

import click

from cmft.split_diff_into_files import extract_messages_from_diff


@click.command()
@click.argument("message")
def main(message):
    diff = _get_diff_output()
    messages = extract_messages_from_diff(diff)
    if messages:
        message = messages[0]
    click.echo(message, nl=False)


def _get_diff_output():
    try:
        return run(
            "git diff HEAD",
            shell=True,
            check=True,
            capture_output=True,
            encoding="utf8",
        ).stdout
    except CalledProcessError:
        return ""


if __name__ == "__main__":
    main()
