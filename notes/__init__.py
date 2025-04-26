import click
from .crud import create, read


@click.group()
def cli() -> None:
    """Command line interface for the Notes application."""
    pass


cli.add_command(create)
cli.add_command(read)
