import pytest

from gorest_api_client import Post
from gorest_api_client.exceptions import GorestNotFoundError
from tests.factories import create_post_request

pytestmark = pytest.mark.integration


def test_authenticated_client_can_create_post_for_existing_user(
        client,
        created_user,
) -> None:
    post_request = create_post_request(created_user.id)
    created_post = client.create_post(post_request)

    try:
        assert isinstance(created_post, Post)
        assert created_post.id > 0
        assert created_post.user_id == created_user.id
        assert created_post.title == post_request.title
        assert created_post.body == post_request.body

    finally:
        client.delete_post(created_post.id)


def test_deleted_post_is_no_longer_available(
        client,
        created_user,
) -> None:
    created_post = client.create_post(create_post_request(created_user.id))

    client.delete_post(created_post.id)

    with pytest.raises(GorestNotFoundError):
        client.get_post(created_post.id)
