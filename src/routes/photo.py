from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from src.schemas.photo import PhotoIn, PhotoOut
from src.database.db import get_db
from src.repository.photo import PhotoRepository
from src.services.auth_user import get_current_user
from src.services.cloudinary_tr import apply_transformation_endpoint

router = APIRouter(prefix="/photos", tags=["photos"])


@router.post(
    "/", response_model=PhotoOut, status_code=201, summary="Create a new photo"
)
async def create_photo(
    photo_data: PhotoIn,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new photo.

    :param photo_data: Data of the photo to create.
    :param current_user: The current authenticated user.
    :param db: Database session.
    :return: Created photo.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    photo_repo = PhotoRepository(db)
    new_photo = await photo_repo.create_photo(photo_data, current_user["user_id"])
    return new_photo


@router.get("/", response_model=List[PhotoOut], summary="Get all photos")
async def get_all_photos(db: Session = Depends(get_db)):
    """
    Get all photos.

    :param db: Database session.
    :return: List of all photos.
    """
    photo_repo = PhotoRepository(db)
    photos = await photo_repo.get_all_photos()
    return photos


@router.get("/{photo_id}", response_model=PhotoOut, summary="Get a photo by ID")
async def get_photo_by_id(photo_id: int, db: Session = Depends(get_db)):
    """
    Get a photo by ID.

    :param photo_id: ID of the photo to retrieve.
    :param db: Database session.
    :return: Retrieved photo.
    """
    photo_repo = PhotoRepository(db)
    photo = await photo_repo.get_photo_by_id(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


@router.put("/{photo_id}", response_model=PhotoOut, summary="Update a photo by ID")
async def update_photo(
    photo_id: int,
    photo_data: PhotoIn,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a photo by ID.

    :param photo_id: ID of the photo to update.
    :param photo_data: Updated data for the photo.
    :param current_user: The current authenticated user.
    :param db: Database session.
    :return: Updated photo.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    photo_repo = PhotoRepository(db)
    updated_photo = await photo_repo.update_photo(
        photo_id, photo_data, current_user["user_id"]
    )
    if not updated_photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return updated_photo


@router.delete("/{photo_id}", response_model=PhotoOut, summary="Delete a photo by ID")
async def delete_photo(
    photo_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a photo by ID.

    :param photo_id: ID of the photo to delete.
    :param current_user: The current authenticated user.
    :param db: Database session.
    :return: Deleted photo.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    photo_repo = PhotoRepository(db)
    deleted_photo = await photo_repo.delete_photo(photo_id, current_user["user_id"])
    if not deleted_photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return deleted_photo


@router.get("/search/", response_model=List[PhotoOut], summary="Search photos by tag")
async def search_photos_by_tag(
    tag: str = Query(..., description="Tag to search for"),
    db: Session = Depends(get_db),
):
    """
    Search photos by tag.

    :param tag: The tag to search for.
    :param db: Database session.
    :return: List of photos matching the tag.
    """
    photo_repo = PhotoRepository(db)
    photos = await photo_repo.search_photos_by_tag(tag)
    return photos


@router.get(
    "/filter/", response_model=List[PhotoOut], summary="Filter photos by criteria"
)
async def filter_photos(
    tag: str = None,
    start_date: str = None,
    end_date: str = None,
    min_rating: str = None,
    db: Session = Depends(get_db),
):
    """
    Filter photos by specified criteria.

    :param tag: Tag to filter by.
    :param min_rating: Minimum rating to filter by.
    :param start_date: Start date to filter by.
    :param end_date: End date to filter by.
    :param db: Database session.
    :return: List of filtered photos.
    """
    photo_repo = PhotoRepository(db)
    photos = await photo_repo.filter_photos(tag, min_rating, start_date, end_date)
    return photos


@router.post(
    "/{photo_id}/transform",
    response_model=PhotoOut,
    summary="Apply transformation to a photo by ID",
)
async def transform_photo(
    photo_id: int,
    db: Session = Depends(get_db),
):
    """
    Apply transformation to a photo by ID.
    """
    transformed_url = apply_transformation_endpoint(photo_id)
    if transformed_url:
        return {
            "message": "Zdjęcie po zastosowaniu transformacji:",
            "transformed_url": transformed_url,
        }
    else:
        raise HTTPException(
            status_code=404, detail="Nie znaleziono zdjęcia o podanym ID."
        )
