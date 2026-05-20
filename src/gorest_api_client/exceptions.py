class GorestClientError(Exception):
    """Base exception for all client errors."""


class GorestTimeoutError(GorestClientError):
    """Raised when the API request times out."""


class GorestAuthenticationError(GorestClientError):
    """Raised when authentication fails."""


class GorestNotFoundError(GorestClientError):
    """Raised when a requested resource does not exist."""


class GorestValidationError(GorestClientError):
    """Raised when the API rejects request data."""


class GorestServerError(GorestClientError):
    """Raised when the API returns a server-side error."""


class GorestUnexpectedError(GorestClientError):
    """Raised for unexpected API/client errors."""