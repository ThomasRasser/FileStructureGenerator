from typing import Optional, List

import os
import json

# ==================================================================================

class FileTreeNode:

    def __init__(
        self,
        name: str = "",
        type_str: str = "",
        children: Optional[List["FileTreeNode"]] = None,
        file_path: Optional[str] = None,
    ):

        # If a filepath is given, try to load the root directory from it
        if file_path:
            if not os.path.exists(file_path):
                raise ValueError(f"File '{file_path}' does not exist.")
            if not os.path.isfile(file_path) or not file_path.lower().endswith(".json"):
                raise ValueError(f"'{file_path}' does not point to a JSON file.")

            deserialized_tree = self.__load_from_file(file_path)
            self.name = deserialized_tree.name
            self.type = deserialized_tree.type
            self.children = deserialized_tree.children
            return

        # Otherwise, generate a new node with the given values
        self.name = name

        if type_str not in ["file", "directory"]:
            raise ValueError("Type must be 'file' or 'directory'")
        self.type = type_str

        if type_str == "file" and children is not None:
            raise ValueError("Files must not contain children")

        self.children = children if children is not None else []

    # ------------------------------------------------------------------------------

    def build_from_directory(self, dir_path: str, add_hidden: bool = False) -> None:

        if not os.path.isdir(dir_path):
            raise ValueError(f"Path '{dir_path}' does not point to a directory.")

        items = os.listdir(dir_path)

        if not add_hidden:
            items = [item for item in items if not item.startswith(".")]

        dirs = [item for item in items if os.path.isdir(os.path.join(dir_path, item))]
        for dir in dirs:
            self.children.append(FileTreeNode(dir, "directory"))

        for child in self.children:
            child.build_from_directory(os.path.join(dir_path, child.name))

        files = [item for item in items if os.path.isfile(os.path.join(dir_path, item))]
        for file in files:
            self.children.append(FileTreeNode(file, "file"))

    # ------------------------------------------------------------------------------

    def __serialize(self) -> str:
        def node_to_dict(node: FileTreeNode) -> dict:
            return {
                "name": node.name,
                "type": node.type,
                "children": (
                    [node_to_dict(child) for child in node.children]
                    if node.children
                    else None
                ),
            }

        return json.dumps(
            node_to_dict(self), ensure_ascii=False, indent=4, sort_keys=True
        )

    def __deserialize(self, data: dict) -> "FileTreeNode":
        def dict_to_node(node_dict: dict) -> FileTreeNode:
            name = node_dict["name"]
            type_str = node_dict["type"]
            children = (
                [dict_to_node(child) for child in node_dict["children"]]
                if node_dict["children"]
                else None
            )
            return FileTreeNode(name, type_str, children)

        return dict_to_node(data)

    # ------------------------------------------------------------------------------

    def save_to_file(self, file_path: str, overwrite: bool = False):
        if os.path.exists(file_path) and os.path.isfile(file_path) and not overwrite:
            print(
                f"File '{file_path}' already exists. Use --overwrite to overwrite it."
            )
            return

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.__serialize())

        print(f"File tree saved to {file_path}")

    def __load_from_file(self, file_path: str) -> "FileTreeNode":
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return self.__deserialize(data)

    # ------------------------------------------------------------------------------

    def create_template_copy(
        self, destination_path: str = None, overwrite: bool = False
    ):
        # Use current working directory if no destination is provided
        if destination_path is None:
            destination_path = os.getcwd()

        # Define the root path for this node
        root_path = os.path.join(destination_path, self.name)

        # Check if the path already exists
        if os.path.exists(root_path) and not overwrite:
            print(f"Path '{root_path}' already exists. Skipping creation.")
            return

        # Create files or directories and sub-directories recursively
        if self.type == "directory":
            os.makedirs(root_path)
            for child in self.children:
                child.create_template_copy(root_path)
        elif self.type == "file":
            with open(root_path, "w") as file:
                file.write("This is an empty template file")
        else:
            raise ValueError(
                f"Unknown type '{self.type}' for node '{self.name}'. Expected 'file' or 'directory'."
            )

    # ------------------------------------------------------------------------------

    def print_tree(
        self, indent=0, print_hidden=False, is_last_child=True, prefix=""
    ) -> None:
        if not print_hidden and self.name.startswith("."):
            return

        # Set up the tree branch prefixes
        connector = "  └─" if is_last_child else "  ├─"

        # Print the current file or directory
        if self.type == "file":
            print(f"{prefix + connector}📄 {self.name}")
        elif self.type == "directory":
            print(f"{prefix + connector}📁 {self.name}")

            # Update the prefix for children
            new_prefix = prefix + ("   " if is_last_child else "  │")

            # Sort children: directories first, then files, each alphabetically
            sorted_children = sorted(
                self.children, key=lambda x: (x.type != "directory", x.name.lower())
            )

            # Recursively print children with updated prefix and indentation
            for i, child in enumerate(sorted_children):
                is_last_child = i == len(sorted_children) - 1
                child.print_tree(
                    indent=indent + 1,
                    print_hidden=print_hidden,
                    is_last_child=is_last_child,
                    prefix=new_prefix,
                )