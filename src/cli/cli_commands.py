import click
import traceback
import os

from src.tree.file_tree_node import FileTreeNode

# ==================================================================================

@click.group(chain=True)
@click.option("--traceback", is_flag=True, help="Show traceback on error.")
@click.pass_obj
def cli(obj: dict, traceback: bool):
    # Ensure that obj is a dictionary
    if not obj:
        obj.update({})
    obj["traceback"] = traceback


# BUILD
# ----------------------------------------------------------------------------------


@click.command()
@click.argument("source", type=click.Path(exists=True, file_okay=False))
@click.option(
    "--add-hidden",
    is_flag=True,
    default=False,
    help="Include hidden files in the file tree",
)
@click.pass_obj
def build(obj: dict, source: str, add_hidden: bool):
    """Builds the file tree from the specified directory"""
    try:
        dir_name = os.path.basename(os.path.dirname(source))
        ft: FileTreeNode = FileTreeNode(dir_name, "directory")
        ft.build_from_directory(source, add_hidden=add_hidden)
        obj["ft"] = ft  # Save the FileTreeNode object in the context
        click.echo("File tree built successfully.")
    except Exception as e:
        click.echo(f"An error occurred while building: {e}")
        click.echo("use the --traceback flag for more details.")
        if obj.get("traceback"):
            traceback.print_exc()
        raise click.Abort()

# LOAD
# ----------------------------------------------------------------------------------


@click.command()
@click.argument("input", type=click.Path(exists=True, dir_okay=False))
@click.pass_obj
def load(obj: dict, input: str):
    """Loads the file tree from the specified JSON file"""
    try:
        ft: FileTreeNode = FileTreeNode(file_path=input)
        obj["ft"] = ft  # Save the FileTreeNode object in the context
    except Exception as e:
        click.echo(f"An error occurred while loading: {e}")
        click.echo("use the --traceback flag for more details.")

        if obj.get("traceback"):
            traceback.print_exc()
        raise click.Abort()

# SAVE
# ----------------------------------------------------------------------------------


@click.command()
@click.argument(
    "output",
    type=click.Path(dir_okay=False, writable=True)
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing output file if it already exists",
)
@click.pass_obj
def save(obj: dict, output: str, overwrite: bool):
    """Saves the file tree to the specified output file as JSON"""
    try:
        ft: FileTreeNode = obj.get("ft")
        if ft is None:
            click.echo(
                "No file tree available to save. Use `build` or `load` before `save`."
            )
            raise click.Abort()

        ft.save_to_file(output, overwrite)
    except Exception as e:
        click.echo(f"An error occurred while saving: {e}")
        click.echo("use the --traceback flag for more details.")
        if obj.get("traceback"):
            traceback.print_exc()
        raise click.Abort()

# TEMPLATE
# ----------------------------------------------------------------------------------


@click.command()
@click.argument("destination", type=click.Path(), required=False)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing template if it already exists",
)
@click.pass_obj
def template(obj: dict, destination: str, overwrite: bool):
    """Creates a template copy of the file tree"""
    try:
        ft: FileTreeNode = obj.get("ft")
        if ft is None:
            click.echo(
                "No file tree exists. Use `build` or `load` command before `template`."
            )
            raise click.Abort()
        ft.create_template_copy(destination, overwrite)
        click.echo(
            f"Template copy created at {destination}"
            if destination
            else "Template copy created"
        )
    except Exception as e:
        click.echo(f"An error occurred while creating the template: {e}")
        click.echo("use the --traceback flag for more details.")
        if obj.get("traceback"):
            traceback.print_exc()
        raise click.Abort()

# PRINT
# ----------------------------------------------------------------------------------


@click.command()
@click.option(
    "--print_hidden",
    is_flag=True,
    default=False,
    help="Print also hidden files and directories.",
)
@click.pass_obj
def print_tree(obj: dict, print_hidden: bool):
    """Prints the file tree"""
    ft: FileTreeNode = obj.get("ft")
    if ft is None:
        click.echo("No file tree exists. Use `build` or `load` command before `print`.")
        raise click.Abort()
    ft.print_tree(print_hidden=print_hidden)


# ----------------------------------------------------------------------------------

cli.add_command(build)
cli.add_command(load)
cli.add_command(save)
cli.add_command(template)
cli.add_command(print_tree)