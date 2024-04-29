from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from src.schemas.photo import PhotoCreate, PhotoIn, PhotoOut, TransformationInput
from dependencies import get_image_provider, get_tags_repository, get_photos_repository, PhotoRepository
from src.schemas.users import UserOut
from src.services.auth_user import get_current_user
from src.services.cloudinary_tr import CloudinaryImageProvider
from src.services.abstract import AbstractImageProvider
from src.repository.tags import TagRepository


router = APIRouter(prefix="/photos", tags=["photos"])


@router.post(
    "/", response_model=PhotoOut, status_code=201, summary="Create a new photo"
)
async def create_photo(
    photo_data: PhotoIn,
    file: UploadFile = File(),
    current_user: UserOut = Depends(get_current_user),
    photos_repository: PhotoRepository = Depends(get_photos_repository),
    image_provider: CloudinaryImageProvider = Depends(get_image_provider),
    tags_repository: TagRepository = Depends(get_tags_repository),
):
    """
    Create a new photo.

    :param photo_data: Data of the photo to create.
    :param current_user: The current authenticated user.
    :param db: Database session.
    :return: Created photo.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized.")
    photo_tags = []

    for tag_name in photo_data.tags:
        tag = await tags_repository.get_tag_by_name(tag_name)
        if tag is None:
            tag = await tags_repository.create_tag(tag_name)
        photo_tags.append(tag.id)
    photo_url = image_provider.upload(file, current_user)
    data = PhotoCreate(
        description=photo_data.description, tags=photo_tags, image_url=photo_url
    )
    photo_data.tags = photo_tags
    new_photo = await photos_repository.create_photo(data, current_user.id)
    return new_photo


@router.get("/", response_model=list[PhotoOut], summary="Get all photos")
async def get_all_photos(
    photos_repository: PhotoRepository = Depends(get_photos_repository),
):
    """
    Get all photos.

    :param db: Database session.
    :return: List of all photos.
    """
    photos = await photos_repository.get_all_photos()
    if not photos:
        raise HTTPException(status_code=404, detail="No photos found.")
    return photos


@router.get("/{photo_id}", response_model=PhotoOut, summary="Get a photo by ID")
async def get_photo_by_id(
    photo_id: int, photos_repository: PhotoRepository = Depends(get_photos_repository)
):
    """
    Get a photo by ID.

    :param photo_id: ID of the photo to retrieve.
    :param db: Database session.
    :return: Retrieved photo.
    """
    photo = await photos_repository.get_photo_by_id(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found.")
    return photo


@router.put("/{photo_id}", response_model=PhotoOut, summary="Update a photo by ID")
async def update_photo(
    photo_id: int,
    photo_data: PhotoIn,
    current_user: UserOut = Depends(get_current_user),
    photos_repository: PhotoRepository = Depends(get_photos_repository),
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

    updated_photo = await photos_repository.update_photo(
        photo_id, photo_data, current_user.id
    )
    if not updated_photo:
        raise HTTPException(status_code=404, detail="Photo not found.")
    return updated_photo


@router.delete("/{photo_id}", response_model=PhotoOut, summary="Delete a photo by ID")
async def delete_photo(
    photo_id: int,
    current_user: UserOut = Depends(get_current_user),
    photos_repository: PhotoRepository = Depends(get_photos_repository),
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

    deleted_photo = await photos_repository.delete_photo(photo_id, current_user.id)
    if not deleted_photo:
        raise HTTPException(status_code=404, detail="Photo not found.")
    return deleted_photo


@router.get("/search/", response_model=list[PhotoOut], summary="Search photos by tag")
async def search_photos_by_tag(
    tag: str = Query(..., description="Tag to search for"),
    photos_repository: PhotoRepository = Depends(get_photos_repository),
):
    """
    Search photos by tag.

    :param tag: The tag to search for.
    :param db: Database session.
    :return: List of photos matching the tag.
    """
    photos = await photos_repository.search_photos_by_tag(tag)
    return photos


@router.get(
    "/filter/", response_model=list[PhotoOut], summary="Filter photos by criteria"
)
async def filter_photos(
    tag: str = None,
    start_date: str = None,
    end_date: str = None,
    min_rating: str = None,
    photos_repository: PhotoRepository = Depends(get_photos_repository),
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
    photos = await photos_repository.filter_photos(
        tag, min_rating, start_date, end_date
    )
    return photos


@router.post(
    "/{photo_id}/transform",
    response_model=PhotoOut,
    summary="Apply transformation to a photo by ID",
)
async def transform_photo(
    id: int,
    trans_body: TransformationInput,
    photos_repository: PhotoRepository = Depends(get_photos_repository),
    image_provider: AbstractImageProvider = Depends(get_image_provider),
):
    """
    Apply transformation to a photo by ID.
    """
    photo = photos_repository.get_photo_by_id(photo_id=id)
    transformed_url = image_provider.transform(
        url=photo.image_url, transform=trans_body
    )
    if transformed_url:
        return {
            "message": "Photo after applying the transformation:",
            "transformed_url": transformed_url,
        }
    else:
        raise HTTPException(status_code=404, detail="No photo found.")
