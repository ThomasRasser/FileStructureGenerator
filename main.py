from src.cli import cli
from src.logging import setup_logger

if __name__ == "__main__":
    # Initialize logger
    # logger = setup_logger(__name__, "file_tree_node.log")

    # The cli function is called to start the command-line interface.
    # The obj parameter is used to pass a dictionary that can hold context data.
    cli(obj={})