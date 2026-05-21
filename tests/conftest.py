import os
from collections.abc import Generator

import pytest
from dotenv import load_dotenv

from gorest_api_client import GorestClient, GorestConfig, User
from tests.factories import create_user_request


load_dotenv()


@pytest.fixture(scope="session")
def config() -> GorestConfig:
    return GorestConfig(
        base_url=os.getenv("GOREST_BASE_URL", "https://gorest.co.in/public/v2"),
        token=os.getenv("GOREST_TOKEN"),
    )


@pytest.fixture
def client(config: GorestConfig) -> GorestClient:
    return GorestClient(config)


@pytest.fixture
def created_user(client: GorestClient) -> Generator[User, None, None]:
    user = client.create_user(create_user_request())

    yield user

    client.delete_user(user.id)