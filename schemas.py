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


class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# ================================
#           USER
# ================================


class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_username(cls, username):
        if not 3 <= len(username) <= 50:
            raise ValueError("Username must be between 3 and 50 characters long.")

        return username


class UserResponseModel(ResponseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# ================================
#           MOVIE
# ================================


class MovieRequestModel(BaseModel):
    title: str


class MovieResponseModel(ResponseModel):
    id: int
    title: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# ================================
#           REVIEW
# ================================
class ReviewValidator:
    @validator("score")
    def validate_score(cls, score):
        if not 1 <= score <= 5:
            raise ValueError("Score must be between 1 and 5")

        return score


class ReviewRequestModel(BaseModel, ReviewValidator):
    user_id: int
    movie_id: int
    review_text: str
    score: int


class ReviewResponseModel(ResponseModel):
    movie_id: int
    review_text: str
    score: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ReviewPutRequestModel(BaseModel, ReviewValidator):
    review_text: str
    score: int
