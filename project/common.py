from datetime import datetime, timedelta

import jwt

from decouple import config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from project.database import User

SECRET_KEY = config("SECRET_KEY")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth")


def create_access_token(user, days: int = 7):
    data = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(days=days),
    }

    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception as error:
        return None


def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    data = decode_access_token(token)

    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Access Token is not valid.",
                            headers={"WWW-Authenticate": "Bearer"})

    return User.select().where(User.id == data["user_id"]).first()
