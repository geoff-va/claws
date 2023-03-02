import logging
from pathlib import Path
from typing import Any, Callable

import tomlkit as tk
from tomlkit import items

log = logging.getLogger(__name__)

CONF_TABLE_NAME = "conf-options"
FIELDS_TABLE_NAME = "fields"


class TomlConf:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._doc = self._load_file(path)

    def _load_file(self, path: Path) -> tk.TOMLDocument:
        # TODO: Should we ever load an existing one?
        # if path.exists():
        #     log.info("Loading existing path: %s", path)
        #     with path.open("rb") as fin:
        #         return tk.load(fin)
        # log.info("Path %s does not exist, creating new toml document", path)
        return tk.document()

    def add_conf_table(self) -> None:
        pass

    def add_structure(self) -> None:
        pass

    def dump(self) -> None:
        """Write current doc to file"""
        with self._path.open("w") as fout:
            tk.dump(self._doc, fout)
            log.info("Wrote: %s", self._path)

    def create(
        self,
        conf_data: dict,
        field_builder: Callable[[dict], items.Table] | None = None,
    ) -> None:
        """Create a new .toml conf file from data_in

        NOTE: Currently only works with .env style data

        Args:
            conf_data (dict): dict of the incoming configuration data
            field_builder (Callable): used to build a field
        """
        if field_builder is None:
            field_builder = build_field

        # TODO: Find leaves, build up dotted location as name
        fields_table = tk.table(True)
        for name, v in conf_data.data.items():
            if name not in fields_table:
                field_table = field_builder(name, v)
                fields_table.add(name, field_table)

        self._doc.add(FIELDS_TABLE_NAME, fields_table)
        self.dump()


def build_field(name: str, value: Any) -> items.Table:
    """Return"""
    table = tk.table()
    # TODO: Do I need a name field?
    table["name"] = name
    table["type"] = _guess_field_type(value)
    table["default"] = value
    return table


def _guess_field_type(value: Any) -> str:
    """Try to return a field type based on value"""
    if isinstance(value, int):
        return "integer"

    if isinstance(value, float):
        return "float"

    if isinstance(value, str):
        if value.lower().strip() in ("true", "false"):
            return bool

        if "." in value:
            try:
                float(value)
                return "float"
            except ValueError:
                return "string"

        try:
            int(value)
            return "integer"
        except ValueError:
            return "string"
