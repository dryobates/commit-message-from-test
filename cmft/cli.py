from subprocess import CalledProcessError, run

import click


@click.command()
@click.argument("message")
def main(message):
    try:
        run("git diff", shell=True, check=True)
    except CalledProcessError:
        click.echo(message)


if __name__ == "__main__":
    main()
