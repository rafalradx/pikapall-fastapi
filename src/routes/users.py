from fastapi import APIRouter, Depends, status
from src.services.auth_user import get_current_user
from src.schemas.users import UserOut

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