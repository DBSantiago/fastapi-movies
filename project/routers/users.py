from fastapi import HTTPException, APIRouter, Response
from fastapi.security import HTTPBasicCredentials

from project.database import User
from project.schemas import UserResponseModel, UserRequestModel

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, "Username already exists.")

    hashed_password = User.create_password(user.password)

    user = User.create(
        username=user.username,
        password=hashed_password
    )
    return user


@router.post("/login", response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        return HTTPException(404, "User not found")

    if user.password != User.create_password(credentials.password):
        return HTTPException(404, "Password error")

    response.set_cookie(key="user_id", value=user.id)

    return user
