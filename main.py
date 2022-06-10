from fastapi import FastAPI, HTTPException
from database import database as connection
from database import User, Movie, Review
from schemas import UserBaseModel

app = FastAPI(title="Movies Reviews", description="A project where we can review movies", version="1")


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


@app.post("/users")
async def create_user(user: UserBaseModel):
    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, "Username already exists.")

    hashed_password = User.create_password(user.password)

    user = User.create(
        username=user.username,
        password=hashed_password
    )
    return user.id
