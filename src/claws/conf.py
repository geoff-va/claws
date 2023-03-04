import logging
from pathlib import Path
from typing import Any, Callable, Iterable

import tomlkit as tk
from tomlkit import items

from .validation import (
    BaseValidator,
    ValidationConfigError,
    ValidationError,
    ValidatorNotFoundError,
    validation_factory,
)

log = logging.getLogger(__name__)

CONF_TABLE_NAME = "conf-options"
FIELDS_TABLE_NAME = "fields"


class TomlConf:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._doc = self._load_file(path)
        self._fields_table = self._doc.get(FIELDS_TABLE_NAME, tk.table(True))
        if FIELDS_TABLE_NAME not in self._doc:
            self._doc.add(FIELDS_TABLE_NAME, self._fields_table)

    def _load_file(self, path: Path) -> tk.TOMLDocument:
        if path.exists():
            log.info("Loading existing path: %s", path)
            with path.open("rb") as fin:
                return tk.load(fin)
        log.info("Path %s does not exist, creating new toml document", path)
        return tk.document()

    def validate(self, data: dict) -> None:
        for field, field_data in self._fields_table.items():
            try:
                validator_class = validation_factory(field_data["type"])
            except ValidatorNotFoundError:
                log.warning("No validation class found for %s", field_data["type"])
                continue

            if field not in data:
                log.warning("Field %s doesn't exist in loaded configuration", field)
                continue

            value = data[field]
            try:
                validator: BaseValidator = validator_class(
                    **field_data.get("validation", {})
                )

                validator.check(value)
            except ValidationError as e:
                print(f"{field}: {value}")
                print(f"  {e}")
            except ValidationConfigError as e:
                print(f"{field}: Validation Configuration Error")
                print(f"  {e}")

    def dump(self) -> None:
        """Write current doc to file"""
        with self._path.open("w") as fout:
            tk.dump(self._doc, fout)
            log.info("Wrote: %s", self._path)

    def sync(
        self, conf_data: dict, field_builder: Callable[[dict], items.Table] = None
    ) -> None:
        """Adds/Removes fields from current toml doc based on fields in conf_data"""
        if field_builder is None:
            field_builder = build_field

        conf_fields = flatten_dict(conf_data)
        current_fields = squash(flatten_dict(self._doc.get("fields", {})))

        to_add = conf_fields.keys() - current_fields.keys()
        to_remove = current_fields.keys() - conf_fields.keys()
        breakpoint()

        # Add fields
        self._add_fields()

        # Remove Fields

    def _add_fields(self, fields: dict[str, Any], conf_data: dict) -> None:
        """Remove keys from fields table"""
        for location, default in fields.items():
            field = build_field(default)
            self._fields_table.add(field)
            log.debug("Added Field: %s", location)

    def _remove_fields(self, field_locations: Iterable[str]) -> None:
        """Remove fields from fields table"""
        for location in field_locations:
            self._fields_table.pop(location)
            log.debug("Removed Field: %s", location)


def squash(flattened: dict) -> dict:
    result = {}
    for k, v in flattened.items():
        parts = k.split(".")
        path, attr = parts[:-1], parts[-1]
        if attr == "default":
            result[".".join(path)] = v
    return result


def build_field(value: Any) -> items.Table:
    """Return default field table"""
    table = tk.table()
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


def flatten_dict(dic: dict) -> dict:
    data = {}
    _flatten_dict(dic, [], data)
    return data


def _flatten_dict(node: dict, location: list[str], flattened: dict) -> None:
    for k, v in node.items():
        location += [k]
        if _is_leaf(v):
            flattened[".".join(location)] = v
        else:
            _flatten_dict(v, location, flattened)
        location.pop(-1)


def _is_leaf(value: Any) -> bool:
    """Return True if the current value is a leaf"""
    return False if isinstance(value, dict) else True
