from typing import List

from fastapi import FastAPI, HTTPException
from database import database as connection
from database import User, Movie, Review
from schemas import *

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


@app.post("/users", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, "Username already exists.")

    hashed_password = User.create_password(user.password)

    user = User.create(
        username=user.username,
        password=hashed_password
    )
    return user


@app.post("/movies", response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):
    new_movie = Movie.create(
        title=movie.title
    )

    return new_movie


@app.get("/movies", response_model=List[MovieResponseModel])
async def get_movies():
    movies = Movie.select()

    return list(movies)


@app.get("/movies/{movie_id}", response_model=MovieResponseModel)
async def get_movie(movie_id: int):
    movie = Movie.select().where(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(404, "Review not found")

    return movie


@app.post("/reviews", response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not found")

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    review = Review.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review_text=user_review.review_text,
        score=user_review.score
    )

    return review


@app.get("/reviews", response_model=List[ReviewResponseModel])
async def get_reviews():
    reviews = Review.select()

    return list(reviews)


@app.get("/reviews/{review_id}", response_model=ReviewResponseModel)
async def get_review(review_id: int):
    review = Review.select().where(Review.id == review_id).first()

    if review is None:
        raise HTTPException(404, "Review not found")

    return review
