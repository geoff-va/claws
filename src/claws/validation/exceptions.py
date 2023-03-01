from ..exceptions import ClawsError


class ValidationError(ClawsError):
    """Raised if there is a validation error"""


class ValidationConfigError(ClawsError):
    """Raised if there is an error configuring validation"""
