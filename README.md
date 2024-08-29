# File Structure Simulator

**Problem:**
Some of my scripts manipulate files or the general file structure in different kind of ways.
To get a consistent testing environment, it would be great if I could replicate a given file structure, as often as I want.

**Solution:**
This Python-based tool allows you to interactively build, load, and save file structures, based on a given directory.
It uses JSON to serialize and deserialize file trees and provides a CLI for various operations on file trees.

## Features

- Build a file tree from a specified directory.
- Load a file tree from a JSON file (The JSON file must have been created with this tool via the `save` command).
- Save the current file tree to a JSON file.
- Create a template copy of the file tree in a new location, with empty dummy files.
- Print the file tree in a console-friendly format similar to the `tree` command.

## Prerequisites

- Python 3.6+
- Click (Command Line Interface Creation Kit)

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/ThomasRasser/FileStructureSimulator.git
cd FileStructureSimulator
```
Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install the required packages:

```bash
pip install -r requirements.txt
```
## Usage

### Help

Use the `--help` command to get a description of the different commands

```bash
python3 main.py --help # General explanation
```

```bash
python3 main.py build --help # Explanation for specific commands
```

### Chaining

It is possible to chain commands together to achieve the desired output, as seen in the following examples

**Build file tree -> Save as JSON -> Print into console**

```bash
python3 main.py build '<file path>' save --output 'fileTree.json' --overwrite print-tree
```

**Load file tree -> Create template**

```bash
python3 main.py load fileTree.json template testing
```
