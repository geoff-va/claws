import json
from pathlib import Path

import tomlkit as tk
from dotenv import dotenv_values


def read_env(path: Path) -> dict:
    """Return a dict from reading a .env formatted file"""
    return dotenv_values(path)


def read_json(path: Path) -> dict:
    """Return a dict from reading a .json formatted file"""
    with path.open("r") as fin:
        return json.load(fin)


def read_toml(path: Path) -> tk.TOMLDocument:
    """Return a dict-like object from reading a .toml formatted file"""
    with path.open("rb") as fin:
        return tk.load(fin)
