from ..exceptions import ClawsError


class ValidationError(ClawsError):
    """Raised if there is a validation error"""


class ValidationConfigError(ClawsError):
    """Raised if there is an error configuring validation"""


class ValidatorNotFoundError(ClawsError):
    """Raised when trying to access a validator that doesn't exist"""
