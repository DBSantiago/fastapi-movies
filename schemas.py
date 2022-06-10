from pydantic import BaseModel
from pydantic import validator


class UserBaseModel(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_username(cls, username):
        if not 3 <= len(username) <= 50:
            raise ValueError("Username must be between 3 and 50 characters long.")

        return username
