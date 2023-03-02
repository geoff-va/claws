class ClawsError(Exception):
    """Base library exception"""


class UnsupportedFileTypeError(ClawsError):
    """Raised when a file type is unsupported"""
