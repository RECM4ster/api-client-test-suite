from uuid import uuid4

from gorest_api_client.models import CreatePostRequest, CreateUserRequest


def create_user_request() -> CreateUserRequest:
    unique_value = uuid4().hex

    return CreateUserRequest(
        name="QA Test User",
        email=f"qa_user_{unique_value}@example.com",
        gender="male",
        status="active",
    )


def create_post_request(user_id: int) -> CreatePostRequest:
    unique_value = uuid4().hex

    return CreatePostRequest(
        user_id=user_id,
        title=f"QA Test Post {unique_value}",
        body="Integration test body",
    )