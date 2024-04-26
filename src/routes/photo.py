from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.schemas.photo import PhotoCreate, PhotoOut
from src.services.photo_service import PhotoService
from src.services.auth_user import get_current_user
from src.database.db import get_db

router = APIRouter(prefix="/photos", tags=["Photos"])


@router.post(
    "/", response_model=PhotoOut, status_code=201, summary="Create a new photo"
)
async def create_photo(
    photo_data: PhotoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new photo.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    photo_service = PhotoService(db)
    new_photo = await photo_service.create_photo(photo_data, current_user["user_id"])
    return new_photo


@router.get("/", response_model=list[PhotoOut], summary="Get all photos")
async def get_all_photos(db: Session = Depends(get_db)):
    """
    Get all photos.
    """
    photo_service = PhotoService(db)
    photos = await photo_service.get_all_photos()
    return photos


@router.get("/{photo_id}", response_model=PhotoOut, summary="Get a photo by ID")
async def get_photo_by_id(photo_id: int, db: Session = Depends(get_db)):
    """
    Get a photo by ID.
    """
    photo_service = PhotoService(db)
    photo = await photo_service.get_photo_by_id(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


@router.put("/{photo_id}", response_model=PhotoOut, summary="Update a photo by ID")
async def update_photo(
    photo_id: int,
    photo_data: PhotoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a photo by ID.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    photo_service = PhotoService(db)
    updated_photo = await photo_service.update_photo(
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
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    photo_service = PhotoService(db)
    deleted_photo = await photo_service.delete_photo(photo_id, current_user["user_id"])
    if not deleted_photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return deleted_photo
