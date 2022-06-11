from typing import List

from fastapi import HTTPException, APIRouter

from project.schemas import ReviewResponseModel, ReviewRequestModel, ReviewPutRequestModel
from project.database import User, Movie, Review

router = APIRouter(prefix="/reviews")


@router.post("/", response_model=ReviewResponseModel)
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


@router.get("/", response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    reviews = Review.select().paginate(page, limit)

    return list(reviews)


@router.get("/{review_id}", response_model=ReviewResponseModel)
async def get_review(review_id: int):
    review = Review.select().where(Review.id == review_id).first()

    if review is None:
        raise HTTPException(404, "Review not found")

    return review


@router.put("/{review_id}", response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewPutRequestModel):
    review = Review.select().where(Review.id == review_id).first()

    if review is None:
        raise HTTPException(404, "Review not found")

    review.review_text = review_request.review_text
    review.score = review_request.score

    review.save()

    return review


@router.delete("/{review_id}", response_model=ReviewResponseModel)
async def delete_review(review_id: int):
    review = Review.select().where(Review.id == review_id).first()

    if review is None:
        raise HTTPException(404, "Review not found")

    review.delete_instance()

    return review
