from fastapi import FastAPI, APIRouter

from project.database import database as connection
from project.database import User, Movie, Review

from project.routers import user_router
from project.routers import review_router
from project.routers import movie_router

app = FastAPI(title="Movies Reviews", description="A project where we can review movies", version="1")

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(user_router)
api_v1.include_router(review_router)
api_v1.include_router(movie_router)

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
