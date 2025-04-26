import click
import os
from pathlib import Path
from .crud import create, read
from config import load_config, DEFAULT_NOTES_DIR


@click.group()
def cli(ctx: click.Context):
    """Command line interface for the Notes application."""
    # Load configuration
    config = load_config()

    notes_dir = config.get("notes_dir", str(DEFAULT_NOTES_DIR))
    # Create notes directory if it doesn't exist
    if not notes_dir.exists():
        os.makedirs(notes_dir)
    ctx.obj = {"notes_dir": Path(notes_dir), "config": config}


cli.add_command(create)
cli.add_command(read)
