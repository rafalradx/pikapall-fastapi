from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from src.repository import comments
from src.database.db import get_db
from src.schemas.users import RoleEnum, UserOut
from src.schemas.photo import CommentOut
from src.services.auth_user import get_current_user

router = APIRouter()


@router.post("/comments/", status_code=201)
async def create_comment(
    photo_id: int,
    user_id: int,
    content: str,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    if current_user.role == RoleEnum.user:
        raise HTTPException(status_code=403, detail="Only admins and mods can create comments")
    return await comments.create_comment(db, photo_id, user_id, content)


@router.put("/comments/{comment_id}/", status_code=200)
async def update_comment(
    comment_id: int,
    user_id: int,
    new_content: str,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    if current_user.role == RoleEnum.user:
        raise HTTPException(status_code=403, detail="komentarze usuwa tylko admin lub moderator")
    updated_comment = await comments.update_comment(db, comment_id, user_id, new_content)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="nie znaleziono komentarza")
    return updated_comment


@router.delete("/comments/{comment_id}/", status_code=204)
async def delete_comment(
    comment_id: int,
    user_role: RoleEnum,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user not in [RoleEnum.admin, RoleEnum.mod]:
        raise HTTPException(status_code=403, detail="Komentarze usuwa tylko admin lub moderator")
    if not await comments.delete_comment(db, comment_id, user_role):
        raise HTTPException(status_code=404, detail="Nie znaleziono komentarza")


@router.get("/comments/{photo_id}/", response_model=list[CommentOut], status_code=200)
async def get_comments_for_photo(
    photo_id: int,
    db: Session = Depends(get_db)
):
    return await comments.get_comments_for_photo(db, photo_id)
