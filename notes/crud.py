import click
from datetime import datetime
import json
import os
from pathlib import Path


@click.command()
@click.argument("title")
@click.option("--content", default="", help="Content of the note")
@click.option("--tags", default="", help="Tags for the note, separated by commas.")
@click.pass_context
def create(ctx: click.Context, title: str, content: str, tags: str):
    """Create a new note."""
    notes_dir = ctx.obj["notes_dir"]
    note_name = f"{title}.txt"
    note_path = notes_dir / note_name

    if note_path.exists():
        click.secho(
            f"Note {note_name} already exists. Please choose a different title.",
            fg="red",
        )
        exit(1)

    note_data = {
        "title": title,
        "content": content,
        "tags": tags.split(",") if tags else [],
        "created_at": datetime.now().isoformat(),
    }

    with open(note_path, "w") as f:
        json.dump(note_data, f, indent=4)

    click.secho(f"Note {note_name} created successfully.", fg="green")


@click.command()
@click.option("--tag", default="", help="Filter notes by tag.")
@click.option("--sort", default="created_at", help="Sort notes by field.")
def read(tag: str, sort: str):
    """Read notes."""
    notes_dir = Path(".notes")

    # check if notes directory exists
    if not notes_dir.exists() or not any(notes_dir.iterdir()):
        click.secho("No notes found.", fg="yellow")
        return

    # check if tag is valid
    if tag and not isinstance(tag, str):
        click.secho("Invalid tag. Please provide a string.", fg="red")
        return

    # check if sort is valid
    valid_sort_options = ["created_at", "title"]
    if sort not in valid_sort_options:
        click.secho("Invalid sort option. Use 'created_at' or 'title'.", fg="red")
        return

    # check if tag exists in notes
    if tag and not any(
        tag in json.load(open(note_file, "r"))["tags"]
        for note_file in notes_dir.iterdir()
    ):
        click.secho(f"No notes found with tag '{tag}'.", fg="yellow")
        return

    notes = []
    # Read all notes
    for note_file in notes_dir.iterdir():
        if note_file.suffix == ".txt":
            with open(note_file, "r") as f:
                note_data = json.load(f)
                if tag and tag not in note_data["tags"]:
                    continue
                notes.append(note_data)

    if sort == "created_at":
        notes.sort(key=lambda x: x["created_at"])
    elif sort == "title":
        notes.sort(key=lambda x: x["title"])

    for note in notes:
        click.echo(f"Title: {note['title']}")
        click.echo(f"Content: {note['content']}")
        click.echo(f"Tags: {', '.join(note['tags'])}")
        click.echo(f"Created at: {note['created_at']}")
        click.echo("-" * 40)
