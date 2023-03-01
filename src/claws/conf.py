import logging
from pathlib import Path

import tomlkit as tk

log = logging.getLogger(__name__)

CONF_TABLE_NAME = "conf-options"


class TomlConf:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._doc = self._load_file(path)

    def _load_file(self, path: Path) -> tk.TOMLDocument:
        if path.exists():
            log.info("Loading existing path: %s", path)
            with path.open("rb") as fin:
                return tk.load(fin)
        log.info("Path %s does not exist, creating new toml document", path)
        return tk.document()

    def add_conf_table(self) -> None:
        pass

    def add_structure(self) -> None:
        pass

    def add_field(
        self,
        name: str,
        type: str,
        location: str,
        display_name: str = "",
        default: str = "",
        help: str = "",
        remove_if_empty: bool = False,
    ) -> None:
        root = tk.table(True) if not "fields" in self._doc else self._doc["fields"]
        table = tk.table()
        table["name"] = name
        table["type"] = type
        table["display_name"] = display_name
        table["default"] = default
        table["help"] = help
        table["remove_if_empty"] = remove_if_empty
        root.append(location, table)
        if "fields" not in self._doc:
            self._doc.append("fields", root)

    def dump(self) -> None:
        """Write current doc to file"""
        with self._path.open("w") as fout:
            tk.dump(self._doc, fout)
            log.info("Wrote: %s", self._path)
