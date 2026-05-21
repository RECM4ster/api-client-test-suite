import httpx
import pytest
import respx

from gorest_api_client.exceptions import (
    GorestAuthenticationError,
    GorestTimeoutError,
    GorestUnexpectedError,
)
from gorest_api_client.transport import HttpTransport


BASE_URL = "https://gorest.co.in/public/v2"


@respx.mock
def test_authenticated_request_sends_bearer_token() -> None:
    transport = HttpTransport(base_url=BASE_URL, token="test-token")

    route = respx.get(f"{BASE_URL}/users").mock(
        return_value=httpx.Response(status_code=200, json=[])
    )

    transport.request("GET", "/users")

    sent_request = route.calls[0].request

    assert sent_request.headers["Authorization"] == "Bearer test-token"


@respx.mock
def test_unauthorized_response_is_mapped_to_authentication_error() -> None:
    transport = HttpTransport(base_url=BASE_URL, token=None)

    respx.post(f"{BASE_URL}/users").mock(
        return_value=httpx.Response(status_code=401, text="Authentication failed")
    )

    with pytest.raises(GorestAuthenticationError):
        transport.request("POST", "/users", json={"name": "QA Test User"})


@respx.mock
def test_timeout_is_mapped_to_timeout_error() -> None:
    transport = HttpTransport(base_url=BASE_URL, max_retries=0)

    respx.get(f"{BASE_URL}/users").mock(
        side_effect=httpx.TimeoutException("Request timed out")
    )

    with pytest.raises(GorestTimeoutError):
        transport.request("GET", "/users")


@respx.mock
def test_request_retries_temporary_server_error_and_returns_success() -> None:
    transport = HttpTransport(base_url=BASE_URL, max_retries=1)

    route = respx.get(f"{BASE_URL}/users").mock(
        side_effect=[
            httpx.Response(status_code=503, text="Service unavailable"),
            httpx.Response(status_code=200, json=[]),
        ]
    )

    response = transport.request("GET", "/users")

    assert response == []
    assert route.call_count == 2


@respx.mock
def test_request_does_not_retry_validation_error() -> None:
    transport = HttpTransport(base_url=BASE_URL, max_retries=2)

    route = respx.post(f"{BASE_URL}/users").mock(
        return_value=httpx.Response(status_code=400, text="Bad request")
    )

    with pytest.raises(GorestUnexpectedError):
        transport.request("POST", "/users", json={"invalid": "payload"})

    assert route.call_count == 1