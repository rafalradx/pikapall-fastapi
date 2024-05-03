from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from src.schemas.photo import (
    PhotoCreate,
    PhotoIn,
    PhotoOut,
    PhotoUpdateIn,
    PhotoUpdateOut,
    TransformationInput,
)
from dependencies import (
    get_image_provider,
    get_tags_repository,
    get_photos_repository,
    PhotoRepository,
)
from src.schemas.users import UserOut, RoleEnum
from src.services.auth_user import get_current_user
from src.services.image_provider import (
    AbstractImageProvider,
    CloudinaryImageProvider,
)
from src.repository.tags import TagRepository
import io
import qrcode
from fastapi.responses import StreamingResponse

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
    (photo_url, public_id) = image_provider.upload(file, current_user)
    data = PhotoCreate(
        description=photo_data.description,
        tags=photo_tags,
        image_url=photo_url,
        cloudinary_public_id=public_id,
    )
    new_photo = await photos_repository.create_photo(data, current_user.id)
    return new_photo


@router.get("/{photo_id}", response_model=PhotoOut, summary="Get a photo by ID")
async def get_photo_by_id(
    photo_id: int,
    qr_code: bool = False,
    photos_repository: PhotoRepository = Depends(get_photos_repository),
    current_user: UserOut = Depends(get_current_user),
):
    """
    Get a photo by ID.

    :param photo_id: ID of the photo to retrieve.

    :return: Retrieved photo.
    """

    photo = await photos_repository.get_photo_by_id(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found.")

    if qr_code:
        url = photo.image_url
        if photo.image_url_transform:
            url = photo.image_url_transform
        img = qrcode.make(url)
        buf = io.BytesIO()
        img.save(buf)
        buf.seek(0)  # important here!
        return StreamingResponse(buf, media_type="image/jpeg")

    return photo


@router.put("/{photo_id}", response_model=PhotoOut, summary="Update a photo by ID")
async def update_photo(
    photo_id: int,
    photo_data: PhotoUpdateIn,
    current_user: UserOut = Depends(get_current_user),
    photos_repository: PhotoRepository = Depends(get_photos_repository),
    tags_repository: TagRepository = Depends(get_tags_repository),
):
    """
    Update a photo by ID.

    :param photo_id: ID of the photo to update.

    :param photo_data: Updated data for the photo.

    :param current_user: The current authenticated user.

    :return: Updated photo.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    photo_tags = []
    for tag_name in photo_data.tags:
        tag = await tags_repository.get_tag_by_name(tag_name)
        if tag is None:
            tag = await tags_repository.create_tag(tag_name)
        photo_tags.append(tag.id)
    data = PhotoUpdateOut(
        description=photo_data.description,
        tags=photo_tags,
    )
    updated_photo = await photos_repository.update_photo(
        photo_id, data, current_user.id
    )
    if not updated_photo:
        raise HTTPException(status_code=404, detail="Photo not found.")
    return updated_photo


@router.delete("/{photo_id}", response_model=PhotoOut, summary="Delete a photo by ID")
async def delete_photo(
    photo_id: int,
    current_user: UserOut = Depends(get_current_user),
    photos_repository: PhotoRepository = Depends(get_photos_repository),
    image_provider: AbstractImageProvider = Depends(get_image_provider),
):
    """
    Delete a photo by ID.

    :param photo_id: ID of the photo to delete.

    :param current_user: The current authenticated user.

    :return: Deleted photo.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    photo = await photos_repository.get_photo_by_id(photo_id)
    if photo.user_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="You can't delete another user's photo if you're not an administrator.")

    deleted_photo = await photos_repository.delete_photo(photo_id, current_user.id)

    if not deleted_photo:
        raise HTTPException(status_code=404, detail="Photo not found.")
    image_provider.delete(deleted_photo.cloudinary_public_id)
    return deleted_photo


@router.get(
    "/", response_model=list[PhotoOut], summary="Display and/or search and/or filter photos by criteria."
)
async def get_photos(
    keyword: str = None,
    created_after: str = None,
    created_before: str = None,
    avg_rating_above: str = None,
    avg_rating_below: str = None,
    user_id: int = None,
    current_user: UserOut = Depends(get_current_user),
    photos_repository: PhotoRepository = Depends(get_photos_repository),
):
    """
    Display and/or search and/or filter photos by criteria.

    :param keyword: The parameter allows you to search for photos by keyword in fields such as Tag and Description.

    :param created_after: The parameter allows you to search for photos created after the specified date.

    :param created_before: The parameter allows you to search for photos created before the specified date.

    :param avg_rating_above: The parameter allows you to search for photos above the indicated average rating.

    :param avg_rating_below: The parameter allows you to search for photos below the indicated average rating.

    :param user_id: The parameter allows you to search for photos of a specific user.

    :param current_user: The current authenticated user.

    :return: List of filtered photos.
    """
    if current_user.role not in [RoleEnum.admin, RoleEnum.mod] and user_id != None:
        raise HTTPException(status_code=403, detail="Only administrators and moderators can search for photos by user_id.")

    photos = await photos_repository.get_photos(
        keyword, created_after, created_before, avg_rating_above, avg_rating_below, user_id
    )

    if not photos:
        raise HTTPException(status_code=404, detail="No photos found.")
    
    return photos


@router.post(
    "/{photo_id}/transform",
    response_model=PhotoOut,
    summary="Apply transformation to a photo by ID",
)
async def transform_photo(
    photo_id: int,
    trans_body: TransformationInput,
    photos_repository: PhotoRepository = Depends(get_photos_repository),
    image_provider: AbstractImageProvider = Depends(get_image_provider),
    current_user: UserOut = Depends(get_current_user),
) -> PhotoOut:
    """
    Apply transformation to a photo by ID.

    angle: rotate image clockwise by angle in degrees

    effect: "sepia", "cartoonify",

    crop: "crop", "fill", "thumb"

    height: pixel or fraction

    width: pixel or fraction

    gravity: "face"; automatic face detection

    radius: pixel or max; radius for corner rounding
    """
    photo = await photos_repository.get_photo_by_id(photo_id=photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="No photo found!")

    if not photo.user_id == current_user.id:
        raise HTTPException(
            status_code=401, detail="You shall not change someone else's photo!"
        )

    transformed_url = image_provider.transform(
        public_id=photo.cloudinary_public_id, transform=trans_body
    )

    trans_photo = await photos_repository.update_photo_trans_url(
        photo_id=photo_id, url=transformed_url
    )
    return trans_photo
