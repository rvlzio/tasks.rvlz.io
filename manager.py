import click
import os

from cli.commands import (
    database,
    token_store,
    misc,
)


@click.group()
def cli():
    pass


if __name__ == "__main__":
    cli.add_command(database.cli)
    cli.add_command(token_store.cli)
    cli.add_command(misc.cli)
    cli()
