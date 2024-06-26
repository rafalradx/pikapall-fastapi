from fastapi import APIRouter, Depends, HTTPException
from src.schemas.users import RoleEnum, UserOut
from src.schemas.comments import CommentIn, CommentOut, CommentUpdate
from src.repository.comments import CommentsRepository
from src.services.auth_user import get_current_user
from dependencies import get_comments_repository

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("", status_code=200)
async def get_comments_for_photo(
    photo_id: int = None,
    comments_repo: CommentsRepository = Depends(get_comments_repository),
    current_user: UserOut = Depends(get_current_user),
) -> list[CommentOut]:

    comments = await comments_repo.get_comments_for_photo(photo_id)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found.")
    return comments


@router.post("", status_code=201)
async def create_comment(
    new_comment: CommentIn,
    comments_repo: CommentsRepository = Depends(get_comments_repository),
    current_user: UserOut = Depends(get_current_user),
) -> CommentOut:
    return await comments_repo.create_comment(new_comment, current_user.id)


@router.put("/{comment_id}", status_code=200)
async def update_comment(
    comment_id: int,
    new_content: CommentUpdate,
    comments_repo: CommentsRepository = Depends(get_comments_repository),
    current_user: UserOut = Depends(get_current_user),
):

    existing_comment = await comments_repo.get_comment_by_id(comment_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="No comment found.")

    if existing_comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to edit other users' comments.",
        )

    updated_comment = await comments_repo.update_comment(comment_id, new_content)

    return updated_comment


@router.delete("/{comment_id}", status_code=200)
async def delete_comment(
    comment_id: int,
    comments_repo: CommentsRepository = Depends(get_comments_repository),
    current_user: UserOut = Depends(get_current_user),
) -> CommentOut:
    if current_user.role not in [RoleEnum.admin, RoleEnum.mod]:
        raise HTTPException(
            status_code=403, detail="Only admins and mods can delete comments."
        )

    comment = await comments_repo.get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="No comment found.")

    await comments_repo.delete_comment(comment_id)
    return comment
