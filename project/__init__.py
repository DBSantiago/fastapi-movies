from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from project.database import database as connection
from project.database import User, Movie, Review

from project.routers import user_router
from project.routers import review_router
from project.routers import movie_router

from .common import create_access_token

app = FastAPI(title="Movies Reviews", description="A project where we can review movies", version="1")

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(user_router)
api_v1.include_router(review_router)
api_v1.include_router(movie_router)


@api_v1.post("/auth")
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Username or password invalid.",
                            headers={"WWW-Authenticate": "Bearer"})

    return {
        "access_token": create_access_token(user),
        "token_type": "Bearer"
    }


app.include_router(api_v1)


@app.on_event("startup")
def startup():
    print("Server is starting up...")
    if connection.is_closed():
        connection.connect()

    connection.create_tables([User, Movie, Review])


@app.on_event("shutdown")
def shutdown():
    print("Server is shutting down...")
    if not connection.is_closed():
        connection.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
