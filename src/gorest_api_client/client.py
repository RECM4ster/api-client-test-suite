from gorest_api_client.config import GorestConfig
from gorest_api_client.models import CreatePostRequest, CreateUserRequest, Post, User
from gorest_api_client.transport import HttpTransport


class GorestClient:
    def __init__(self, config: GorestConfig) -> None:
        self._transport = HttpTransport(
            base_url=config.base_url,
            token=config.token,
            timeout_seconds=config.timeout_seconds,
            max_retries=config.max_retries,
        )

    def list_users(self) -> list[User]:
        response = self._transport.request("GET", "/users")
        return [User.model_validate(item) for item in response]

    def get_user(self, user_id: int) -> User:
        response = self._transport.request("GET", f"/users/{user_id}")
        return User.model_validate(response)

    def create_user(self, payload: CreateUserRequest) -> User:
        response = self._transport.request(
            "POST",
            "/users",
            json=payload.model_dump(),
        )
        return User.model_validate(response)

    def delete_user(self, user_id: int) -> None:
        self._transport.request("DELETE", f"/users/{user_id}")

    def list_posts(self) -> list[Post]:
        response = self._transport.request("GET", "/posts")
        return [Post.model_validate(item) for item in response]

    def get_post(self, post_id: int) -> Post:
        response = self._transport.request("GET", f"/posts/{post_id}")
        return Post.model_validate(response)

    def create_post(self, payload: CreatePostRequest) -> Post:
        response = self._transport.request(
            "POST",
            "/posts",
            json=payload.model_dump(),
        )
        return Post.model_validate(response)

    def delete_post(self, post_id: int) -> None:
        self._transport.request("DELETE", f"/posts/{post_id}")