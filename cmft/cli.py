from subprocess import CalledProcessError, run

import click

from cmft.extract_message import extract_message_from_python_file_diff


@click.command()
@click.argument("message")
def main(message):
    output = _get_diff_output()
    message = extract_message_from_python_file_diff(output, message)
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
