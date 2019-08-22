import click


@click.command()
@click.argument("message")
def main(message):
    pass


if __name__ == "__main__":
    main()
