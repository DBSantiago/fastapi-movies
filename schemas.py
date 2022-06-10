from peewee import ModelSelect
from pydantic import BaseModel
from pydantic import validator
from pydantic.utils import GetterDict
from typing import Any


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)

        if isinstance(res, ModelSelect):
            return list(res)

        return res


class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_username(cls, username):
        if not 3 <= len(username) <= 50:
            raise ValueError("Username must be between 3 and 50 characters long.")

        return username


class UserResponseModel(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
