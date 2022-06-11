from fastapi import FastAPI

from project.database import database as connection
from project.database import User, Movie, Review

from project.routers import user_router
from project.routers import review_router
from project.routers import movie_router

app = FastAPI(title="Movies Reviews", description="A project where we can review movies", version="1")

app.include_router(user_router)
app.include_router(review_router)
app.include_router(movie_router)


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
