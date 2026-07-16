import asyncio
import logging
from collections.abc import Mapping
from typing import Any

import httpx

from app.core.config import get_settings
from app.integrations.api_football.exceptions import (
    ApiFootballConfigurationError,
    ApiFootballResponseError,
)

logger = logging.getLogger(__name__)


class ApiFootballClient:
    """Small async client for API-Football v3."""

    def __init__(self) -> None:
        self.settings = get_settings()

        if not self.settings.api_football_is_configured:
            raise ApiFootballConfigurationError(
                "API_FOOTBALL_KEY is missing. Add it to the local .env file."
            )

        self.headers = {
            "x-apisports-key": self.settings.api_football_key,
        }

    async def get(
        self,
        endpoint: str,
        params: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.settings.api_football_base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        attempts = max(1, self.settings.api_football_max_retries)

        async with httpx.AsyncClient(
            timeout=self.settings.api_football_timeout_seconds,
            headers=self.headers,
        ) as client:
            for attempt in range(1, attempts + 1):
                try:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    payload = response.json()
                    self._validate_payload(payload)
                    return payload
                except (
                    httpx.TimeoutException,
                    httpx.NetworkError,
                    httpx.HTTPStatusError,
                ) as exc:
                    retryable = self._is_retryable(exc)
                    logger.warning(
                        "API-Football request failed endpoint=%s attempt=%s/%s retryable=%s error=%s",
                        endpoint,
                        attempt,
                        attempts,
                        retryable,
                        exc,
                    )

                    if not retryable or attempt == attempts:
                        raise ApiFootballResponseError(
                            f"API-Football request failed for '{endpoint}'."
                        ) from exc

                    await asyncio.sleep(min(2 ** (attempt - 1), 8))

        raise ApiFootballResponseError(
            f"API-Football request failed for '{endpoint}'."
        )

    @staticmethod
    def _is_retryable(exc: Exception) -> bool:
        if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
            return True
        if isinstance(exc, httpx.HTTPStatusError):
            return exc.response.status_code in {429, 500, 502, 503, 504}
        return False

    @staticmethod
    def _validate_payload(payload: Any) -> None:
        if not isinstance(payload, dict):
            raise ApiFootballResponseError(
                "API-Football returned an unexpected response format."
            )

        errors = payload.get("errors")
        if errors:
            raise ApiFootballResponseError(
                f"API-Football reported an error: {errors}"
            )

        if "response" not in payload:
            raise ApiFootballResponseError(
                "API-Football response is missing the 'response' field."
            )
