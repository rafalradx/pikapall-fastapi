from fastapi import APIRouter, HTTPException, Depends, status
from src.services.auth_user import get_current_user
from src.schemas.users import UserOut, UserChangeRole
from src.repository.abstract import AbstractUserRepository
from dependencies import get_users_repository
from src.schemas.users import RoleEnum


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", status_code=status.HTTP_200_OK)
async def read_users_me(
    current_user: UserOut = Depends(get_current_user),
) -> UserOut:
    """
    Get the details of the current authenticated user.

    :param current_user: The current authenticated user.
    :type current_user: User

    :return: The details of the current authenticated user.
    :rtype: UserOut
    """
    return current_user


@router.get("/promote/{user_id}")
async def promote_user(
    user_id: int,
    role: RoleEnum,
    current_user: UserOut = Depends(get_current_user),
    users_repository: AbstractUserRepository = Depends(get_users_repository),
) -> UserOut:
    if not current_user.role == RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admin can perform this operation."
        )
    
    if not await users_repository.get_user_by_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    
    user_changed = await users_repository.change_user_role(
        user_id=user_id, role=role
    )
    return user_changed