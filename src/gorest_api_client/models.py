from pydantic import BaseModel, ConfigDict


class CreateUserRequest(BaseModel):
    name: str
    email: str
    gender: str
    status: str


class User(BaseModel):
    id: int
    name: str
    email: str
    gender: str
    status: str


class CreatePostRequest(BaseModel):
    user_id: int
    title: str
    body: str


class Post(BaseModel):
    id: int
    user_id: int
    title: str
    body: str

    model_config = ConfigDict(populate_by_name=True)