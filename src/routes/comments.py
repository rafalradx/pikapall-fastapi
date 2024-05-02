from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from src.schemas.users import RoleEnum, UserOut
from src.schemas.photo import CommentOut
from src.repository.comments import CommentsRepository
from src.services.auth_user import get_current_user
from dependencies import get_comments_repository

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", status_code=201)
async def create_comment(
    photo_id: int,
    user_id: int,
    content: str,
    comments_repo: CommentsRepository = Depends(get_comments_repository),
    current_user: UserOut = Depends(get_current_user),
):
    return await comments_repo.create_comment(photo_id, current_user.id, content)


@router.put("/{comment_id}", status_code=200)
async def update_comment(
    comment_id: int,
    new_content: str,
    comments_repo: CommentsRepository = Depends(get_comments_repository),
    current_user: UserOut = Depends(get_current_user),
):
    updated_comment = await comments_repo.get_comment(comment_id)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="No comment found.")

    if updated_comment.user_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to update this comment.",
        )

    return await comments_repo.update_comment(comment_id, new_content)


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: int,
    comments_repo: CommentsRepository = Depends(get_comments_repository),
    current_user: UserOut = Depends(get_current_user),
):
    comment = await comments_repo.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="No comment found.")

    if comment.user_id != current_user.id and current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete this comment.",
        )

    await comments_repo.delete_comment(comment_id)
    return None


@router.get("/{photo_id}", response_model=list[CommentOut], status_code=200)
async def get_comments_for_photo(
    photo_id: int,
    comments_repo: CommentsRepository = Depends(get_comments_repository),
    current_user: UserOut = Depends(get_current_user),
):

    comments = await comments_repo.get_comments_for_photo(photo_id)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found.")
    return comments

