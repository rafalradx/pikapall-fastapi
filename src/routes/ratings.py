from fastapi import APIRouter, HTTPException, Depends
from src.repository.ratings import RatingRepository
from dependencies import get_rating_repository
from src.schemas.ratings import Rating
from src.services.auth_user import get_current_user
from src.schemas.users import UserOut, RoleEnum

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.get("/{photo_id}/average", response_model=float)
async def get_average_rating(
        photo_id: int,
        rating_repo: RatingRepository = Depends(get_rating_repository)):
    """
    Get the average rating for a photo.
    """
    average_rating = await rating_repo.calculate_average_rating(photo_id)
    if average_rating is None:
        raise HTTPException(
            status_code=404, detail="No ratings found for the photo")
    return average_rating


@router.post("/", response_model=Rating)
async def create_rating(
        photo_id: int,
        rating: int,
        rating_repo: RatingRepository = Depends(get_rating_repository),
        current_user: UserOut = Depends(get_current_user)):
    """
    Create a new rating for a photo.
    """
    existing_rating = await rating_repo.get_user_rating_for_photo(photo_id, current_user.id)
    if existing_rating:
        raise HTTPException(
            status_code=400, detail="You have already rated this photo")

    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=400, detail="Rating must be between 1 and 5")
    return await rating_repo.create_rating(photo_id, current_user.id, rating)


@router.put("/{rating_id}", response_model=Rating)
async def update_rating(
        rating_id: int,
        new_rating: int,
        rating_repo: RatingRepository = Depends(get_rating_repository),
        current_user: UserOut = Depends(get_current_user)):
    """
    Update an existing rating.
    """
    existing_rating = await rating_repo.get_rating_by_id(rating_id)
    if not existing_rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    if existing_rating.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not allowed to update this rating")

    if new_rating < 1 or new_rating > 5:
        raise HTTPException(
            status_code=400, detail="Rating must be between 1 and 5")

    updated_rating = await rating_repo.update_rating(rating_id, new_rating, current_user.id)
    if not updated_rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    return updated_rating


@router.delete("/{rating_id}", response_model=Rating)
async def delete_rating(
        rating_id: int,
        rating_repo: RatingRepository = Depends(get_rating_repository),
        current_user: UserOut = Depends(get_current_user)):
    """
    Delete a rating.
    """
    existing_rating = await rating_repo.get_rating_by_id(rating_id)
    if not existing_rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    if existing_rating.user_id != current_user.id and current_user.role not in [RoleEnum.admin, RoleEnum.mod]:
        raise HTTPException(
            status_code=403, detail="You are not allowed to delete this rating")

    deleted = await rating_repo.delete_rating(rating_id, current_user.role, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Rating not found")

    return existing_rating
