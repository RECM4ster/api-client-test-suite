import pytest

from gorest_api_client import GorestClient, GorestConfig, User
from gorest_api_client.exceptions import GorestAuthenticationError, GorestNotFoundError
from tests.factories import create_user_request

pytestmark = pytest.mark.integration


def test_list_users_can_be_called_without_authentication() -> None:
    unauthenticated_client = GorestClient(GorestConfig(token=None))

    users = unauthenticated_client.list_users()

    assert users
    assert all(isinstance(user, User) for user in users)
    assert all(user.id > 0 for user in users)


def test_create_user_requires_authentication() -> None:
    unauthenticated_client = GorestClient(GorestConfig(token=None))

    with pytest.raises(GorestAuthenticationError):
        unauthenticated_client.create_user(create_user_request())


def test_authenticated_client_can_create_and_read_user(
        client,
) -> None:
    user_request = create_user_request()
    created_user = client.create_user(user_request)

    try:
        fetched_user = client.get_user(created_user.id)

        assert created_user.id > 0
        assert fetched_user.id == created_user.id
        assert fetched_user.name == user_request.name
        assert fetched_user.email == user_request.email
        assert fetched_user.gender == user_request.gender
        assert fetched_user.status == user_request.status

    finally:
        client.delete_user(created_user.id)


def test_deleted_user_is_no_longer_available(
        client,
) -> None:
    created_user = client.create_user(create_user_request())

    client.delete_user(created_user.id)

    with pytest.raises(GorestNotFoundError):
        client.get_user(created_user.id)
