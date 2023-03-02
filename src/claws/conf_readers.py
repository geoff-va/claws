"""Functions for reading configuration files. They should return a dict-like object"""
import json
from pathlib import Path
from typing import Callable

import tomlkit as tk
from dotenv import dotenv_values

from .exceptions import UnsupportedFileTypeError


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


_CONF_READER_MAP = {
    ".env": read_env,
    ".json": read_json,
    ".toml": read_toml,
}


def conf_reader_factory(file_ext: str) -> Callable[[Path], dict]:
    """Return a function to read the specified file_ext"""
    try:
        return _CONF_READER_MAP[file_ext]
    except KeyError:
        raise UnsupportedFileTypeError(f"Unsupported config file type: {file_ext}")
