import re
from typing import Any

from .base_validator import BaseValidator
from .exceptions import ValidationConfigError, ValidationError


class StringValidator(BaseValidator):
    """String validation based on their length"""

    def __init__(self, min_length: int = None, max_length: int | None = None):
        self._min_length = min_length if min_length is not None else 0
        self._max_length = max_length

    def _validate_setup(self) -> None:
        if self._min_length < 0:
            raise ValidationConfigError(
                f"min_length must be >= 0, got {self._min_length}"
            )

        if self._max_length is not None and self._max_lenth < 1:
            raise ValidationConfigError(
                f"max_length must be > 0, got {self._max_length}"
            )

    def check(self, value: str) -> None:
        str_len = len(value)

        if self._max_length:
            if not (self._min_length < str_len < self._max_length):
                raise ValidationError(
                    f"String length must be > {self._min_length} and < "
                    f"{self._max_length}, got {str_len}"
                )

        if str_len < self._min_length:
            raise ValidationError(f"String length must be > {self._min_length}")


class RegexStringValidator(BaseValidator):
    """Validation or regex patterns"""

    def __init__(self, regex: str, err_msg: str = "") -> None:
        self._regex = re.compile(regex)
        self._err_msg = err_msg
        self._default_msg = f"Must match regex pattern: {regex}"

    def check(self, value: str) -> None:
        if not self._regex.match(value):
            msg = self._err_msg if self._err_msg else self._default_msg
            raise ValidationError(msg)


class IntegerValidator(BaseValidator):
    """Integer validation within an optional range"""

    def __init__(self, min: int | None = None, max: int | None = None) -> None:
        self._min = min
        self._max = max

    def check(self, value: str) -> None:
        converted = self._convert_type(value)

        if self._min is not None and self._max is not None:
            if not (self._min < converted < self._max):
                raise ValidationError(
                    f"Must be between {self._min} and {self._max}, got {converted}"
                )

        elif self._min is not None:
            if converted < self._min:
                raise ValidationError(f"Must be > {self._min}, got {converted}")

        elif self._max is not None:
            if converted > self._min:
                raise ValidationError(f"Must be < {self._max}, got {converted}")

    def _convert_type(self, value: Any) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValidationError("Not an int")


class FloatValidator(IntegerValidator):
    def _convert_type(self, value: Any) -> int:
        try:
            return float(value)
        except ValueError:
            raise ValidationError("Not a float")


VALIDATOR_MAP = {
    "string": StringValidator,
    "regex": RegexStringValidator,
    "integer": IntegerValidator,
    "float": FloatValidator,
}
