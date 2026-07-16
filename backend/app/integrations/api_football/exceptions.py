class ApiFootballError(Exception):
    """Base exception for API-Football integration failures."""


class ApiFootballConfigurationError(ApiFootballError):
    """Raised when API-Football credentials are missing or invalid locally."""


class ApiFootballResponseError(ApiFootballError):
    """Raised when API-Football returns an error or unexpected response."""
