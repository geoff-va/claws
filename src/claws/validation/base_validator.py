from typing import Any


class BaseValidator:
    """Base Validator class"""

    def __init__(self) -> None:
        self._validate_setup()

    def _validate_setup(self) -> None:
        """Raise ImproperlyConfiguredError if there are validation setup errors"""

    def check(self, value: Any) -> None:
        """Raise ValidationError if necessary"""
