from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    token_type: str
    access_token: str


class FilterPage(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1)
