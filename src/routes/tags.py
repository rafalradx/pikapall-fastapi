from fastapi import APIRouter, HTTPException, Depends, status
from src.schemas.users import UserOut
from src.schemas.photo import TagOut, TagIn
from src.services.auth_user import get_current_user
from src.repository.tags import TagRepository
from dependencies import get_tags_repository

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=list[TagOut])
async def read_all_tags(
    skip: int = 0,
    limit: int = 100,
    tags_repository: TagRepository = Depends(get_tags_repository),
    current_user: UserOut = Depends(get_current_user),
):
    tags = await tags_repository.get_all_tags(skip, limit)
    return tags


@router.get("/{tag_id}", response_model=TagOut)
async def read_tag_by_id(
    tag_id: int,
    tags_repository: TagRepository = Depends(get_tags_repository),
    current_user: UserOut = Depends(get_current_user),
):
    tag = await tags_repository.get_tag_by_id(tag_id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found."
        )
    return tag


@router.get("/{tag_name}", response_model=TagOut)
async def read_tag_by_name(
    tag_name: str,
    tags_repository: TagRepository = Depends(get_tags_repository),
    current_user: UserOut = Depends(get_current_user),
):
    tag = await tags_repository.get_tag_by_name(tag_name)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found."
        )
    return tag


@router.post("/", response_model=TagOut, status_code=status.HTTP_201_CREATED)
async def create_tag(
    body: TagIn,
    tags_repository: TagRepository = Depends(get_tags_repository),
    current_user: UserOut = Depends(get_current_user),
):
    tag = await tags_repository.create_tag(body.name)
    return tag


@router.put("/{tag_id}", response_model=TagOut)
async def update_tag(
    tag_id: int,
    body: str,
    tags_repository: TagRepository = Depends(get_tags_repository),
    current_user: UserOut = Depends(get_current_user),
):
    tag = await tags_repository.update_tag(tag_id, body)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found."
        )
    return tag


@router.delete("/{tag_id}", response_model=TagOut)
async def remove_tag(
    tag_id: int,
    tags_repository: TagRepository = Depends(get_tags_repository),
    current_user: UserOut = Depends(get_current_user),
):
    if tag_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found."
        )
    tag = await tags_repository.delete_tag(tag_id)
    return tag
