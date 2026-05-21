from unittest.mock import Mock

from gorest_api_client import CreatePostRequest, GorestClient, GorestConfig
from gorest_api_client.models import Post, User


def test_client_maps_user_response_to_user_model() -> None:
    client = GorestClient(GorestConfig())
    client._transport = Mock()
    client._transport.request.return_value = {
        "id": 123,
        "name": "Gorest Test User",
        "email": "gorest_user@example.com",
        "gender": "male",
        "status": "active",
    }

    user = client.get_user(123)

    assert user == User(
        id=123,
        name="Gorest Test User",
        email="gorest_user@example.com",
        gender="male",
        status="active",
    )


def test_client_sends_create_post_payload_and_maps_response_to_post_model() -> None:
    client = GorestClient(GorestConfig())
    client._transport = Mock()
    client._transport.request.return_value = {
        "id": 456,
        "user_id": 123,
        "title": "Gorest API Test Post",
        "body": "This post was created to verify client payload mapping.",
    }

    post_request = CreatePostRequest(
        user_id=123,
        title="Gorest API Test Post",
        body="This post was created to verify client payload mapping.",
    )

    post = client.create_post(post_request)

    client._transport.request.assert_called_once_with(
        "POST",
        "/posts",
        json=post_request.model_dump(),
    )
    assert post == Post(
        id=456,
        user_id=123,
        title="Gorest API Test Post",
        body="This post was created to verify client payload mapping.",
    )