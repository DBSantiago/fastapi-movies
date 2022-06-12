from datetime import datetime, timedelta

import jwt

from decouple import config

SECRET_KEY = config("SECRET_KEY")


def create_access_token(user, days: int = 7):
    data = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(days=days),
    }

    return jwt.encode(data, SECRET_KEY, algorithm="HS256")
