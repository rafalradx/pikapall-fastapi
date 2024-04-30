from fastapi import APIRouter, HTTPException, Depends
from src.repository.ratings import RatingRepository
from dependencies import get_rating_repository
from src.schemas.photo import RatingOut
from src.services.auth_user import get_current_user
from src.schemas.users import UserOut, RoleEnum

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.post("/", response_model=RatingOut)
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
    created_rating = await rating_repo.create_rating(photo_id, current_user.id, rating)
    return created_rating


@router.delete("/{rating_id}", response_model=RatingOut)
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
