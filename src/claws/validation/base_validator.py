import re
from typing import Any


class BaseValidator:
    """Base Validator class"""

    def _validate_setup(self) -> None:
        """Raise ImproperlyConfiguredError if there are validation setup errors"""

    def check(self, value: Any) -> None:
        self._validate_setup()
