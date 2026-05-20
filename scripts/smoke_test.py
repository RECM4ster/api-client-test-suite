from dotenv import load_dotenv

from gorest_api_client import (CreateUserRequest, GorestClient, load_config_from_env)

load_dotenv()

config = load_config_from_env()
client = GorestClient(config)
users = client.list_users()

print(f"Fetched users: {len(users)}")

created_user = client.create_user(
    CreateUserRequest(
        name="smoke_test_user",
        email="smoke_test_user@example.com",
        gender="male",
        status="active",
    )
)

print(created_user)

client.delete_user(created_user.id)

print(f"Cleanup completed, user {created_user.name} deleted")