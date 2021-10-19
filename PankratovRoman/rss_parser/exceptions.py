"""The module that implements errors."""


class ResolveError(Exception):
    """Raised when the resolver was unable to process a value."""


class FindResolverError(Exception):
    """Raised when a right resolver cannot be found"""
