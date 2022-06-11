from typing import List

from fastapi import HTTPException, APIRouter

from project.database import Movie
from project.schemas import MovieResponseModel, MovieRequestModel

router = APIRouter(prefix="/api/v1/movies")


@router.post("/", response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):
    new_movie = Movie.create(
        title=movie.title
    )

    return new_movie


@router.get("/", response_model=List[MovieResponseModel])
async def get_movies():
    movies = Movie.select()

    return list(movies)


@router.get("/{movie_id}", response_model=MovieResponseModel)
async def get_movie(movie_id: int):
    movie = Movie.select().where(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(404, "Review not found")

    return movie
