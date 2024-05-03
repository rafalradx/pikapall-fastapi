from fastapi import APIRouter, HTTPException, Depends
from src.repository.ratings import RatingRepository
from dependencies import get_rating_repository, get_photos_repository, PhotoRepository
from src.schemas.ratings import RatingOut
from src.services.auth_user import get_current_user
from src.schemas.users import UserOut, RoleEnum

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.get("/", response_model=list[RatingOut])
async def get_ratings(
    rating_repo: RatingRepository = Depends(get_rating_repository),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Display all ratings.
    """
    if current_user.role in [RoleEnum.admin, RoleEnum.mod]:
        existing_ratings = await rating_repo.get_ratings()
    else:
        existing_ratings = await rating_repo.get_user_ratings(current_user.id)

    if not existing_ratings:
        raise HTTPException(status_code=404, detail="Ratings not found.")

    return existing_ratings


@router.get("/rating_id={rating_id}", response_model=RatingOut)
async def get_rating_by_id(
    rating_id: int,
    rating_repo: RatingRepository = Depends(get_rating_repository),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Display rating by ID.
    """
    if current_user.role in [RoleEnum.admin, RoleEnum.mod]:
        existing_ratings = await rating_repo.get_rating_by_id(rating_id)
    else:
        existing_ratings = await rating_repo.get_user_rating_by_id(
            rating_id, current_user.id
        )

    if not existing_ratings:
        raise HTTPException(status_code=404, detail="Rating not found.")
    return existing_ratings


@router.get("/photo_id={photo_id}", response_model=list[RatingOut])
async def get_ratings_for_photo(
    photo_id: int,
    rating_repo: RatingRepository = Depends(get_rating_repository),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Display ratings for photo.
    """
    if current_user.role in [RoleEnum.admin, RoleEnum.mod]:
        existing_ratings = await rating_repo.get_ratings_for_photo(photo_id)
    else:
        existing_ratings = await rating_repo.get_user_rating_for_photo(
            photo_id, current_user.id
        )

    if not existing_ratings:
        raise HTTPException(status_code=404, detail="Ratings not found.")
    return existing_ratings


@router.get("/user_id={user_id}", response_model=list[RatingOut])
async def get_user_ratings(
    user_id: int,
    rating_repo: RatingRepository = Depends(get_rating_repository),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Display all user's ratings.
    """
    if current_user.role in [RoleEnum.admin, RoleEnum.mod]:
        existing_ratings = await rating_repo.get_user_ratings(user_id)
    else:
        if current_user.id == user_id:
            existing_ratings = await rating_repo.get_user_ratings(user_id)
        else:
            raise HTTPException(
                status_code=404,
                detail="Ratings not found or you have not permission to display these ratings.",
            )

    if not existing_ratings:
        raise HTTPException(status_code=404, detail="Ratings not found.")
    return existing_ratings


@router.post("/", response_model=RatingOut)
async def create_rating(
    photo_id: int,
    rating: int,
    photos_repository: PhotoRepository = Depends(get_photos_repository),
    rating_repo: RatingRepository = Depends(get_rating_repository),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Create a new rating for a photo.
    """
    if not await photos_repository.get_photo_by_id(photo_id):
        raise HTTPException(status_code=400, detail="No photo found with the given ID.")

    photo = await photos_repository.get_photo_by_id(photo_id)
    if photo.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You can't rate your own photos.")

    existing_rating = await rating_repo.get_user_rating_for_photo(
        photo_id, current_user.id
    )
    if existing_rating:
        raise HTTPException(
            status_code=400, detail="You have already rated this photo."
        )

    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
    created_rating = await rating_repo.create_rating(photo_id, current_user.id, rating)
    return created_rating


@router.delete("/{rating_id}", response_model=RatingOut)
async def delete_rating(
    rating_id: int,
    rating_repo: RatingRepository = Depends(get_rating_repository),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Delete a rating.
    """
    existing_rating = await rating_repo.get_rating_by_id(rating_id)
    if not existing_rating:
        raise HTTPException(status_code=404, detail="Rating not found.")

    if existing_rating.user_id != current_user.id and current_user.role not in [
        RoleEnum.admin,
        RoleEnum.mod,
    ]:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this rating. Only Administrators and Moderators can delete all ratings.",
        )

    deleted = await rating_repo.delete_rating(
        rating_id, current_user.role, current_user.id
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Rating not found.")

    return existing_rating
