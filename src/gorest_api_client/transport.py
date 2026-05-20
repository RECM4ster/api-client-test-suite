from collections.abc import Mapping
from typing import Any

import httpx

from gorest_api_client.exceptions import (
    GorestAuthenticationError,
    GorestNotFoundError,
    GorestServerError,
    GorestTimeoutError,
    GorestUnexpectedError,
    GorestValidationError,
)


class HttpTransport:
    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        timeout_seconds: int = 30,
        max_retries: int = 5,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._timeout = httpx.Timeout(timeout_seconds)
        self._max_retries = max_retries

    def request(
        self,
        method: str,
        path: str,
        json: Mapping[str, Any] | None = None,
    ) -> Any:
        url = f"{self._base_url}{path}"
        headers = self._build_headers()

        last_error: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                with httpx.Client(timeout=self._timeout) as client:
                    response = client.request(
                        method=method,
                        url=url,
                        headers=headers,
                        json=json,
                    )

                if self._should_retry(response.status_code, attempt):
                    continue

                return self._handle_response(response)

            except httpx.TimeoutException as exc:
                last_error = exc
                if attempt >= self._max_retries:
                    raise GorestTimeoutError("Request timed out") from exc

            except httpx.RequestError as exc:
                last_error = exc
                if attempt >= self._max_retries:
                    raise GorestUnexpectedError("HTTP request failed") from exc

        raise GorestUnexpectedError("Request failed after retries") from last_error

    def _build_headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if self._token is not None:
            headers["Authorization"] = f"Bearer {self._token}"

        return headers

    def _should_retry(self, status_code: int, attempt: int) -> bool:
        retryable_statuses = {502, 503, 504}
        return status_code in retryable_statuses and attempt < self._max_retries

    def _handle_response(self, response: httpx.Response) -> Any:
        if 200 <= response.status_code < 300:
            if response.status_code == 204:
                return None
            return response.json()

        if response.status_code in {401, 403}:
            raise GorestAuthenticationError(response.text)

        if response.status_code == 404:
            raise GorestNotFoundError(response.text)

        if response.status_code == 422:
            raise GorestValidationError(response.text)

        if 500 <= response.status_code < 600:
            raise GorestServerError(response.text)

        raise GorestUnexpectedError(
            f"Unexpected response {response.status_code}: {response.text}"
        )