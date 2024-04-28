from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from fastapi.requests import Request
from src.repository.abstract import AbstractUserRepository
from dependencies import get_users_repository, get_password_handler

from src.schemas.users import UserChangeRole, UserIn, UserOut, Token
from src.services.auth import auth_service
from src.services.auth_user import get_current_user
from src.services.pwd_handler import AbstractPasswordHashHandler


router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    new_user: UserIn,
    background_tasks: BackgroundTasks,
    request: Request,
    # current_user: UserOut = Depends(get_current_user),
    users_repository: AbstractUserRepository = Depends(get_users_repository),
    pwd_handler: AbstractPasswordHashHandler = Depends(get_password_handler),
) -> UserOut:
    """
    Endpoint to register a new user.

    :param new_user: The user details to be registered.
    :type new_user: UserIn

    :param background_tasks: Background tasks to be executed.
    :type background_tasks: BackgroundTasks

    :param request: The incoming request.
    :type request: Request

    :param users_repository: The repository for user data.
    :type users_repository: AbstractUserRepository

    :param pwd_handler: The password hashing handler.
    :type pwd_handler: AbstractPasswordHashHandler

    :return: The registered user details.
    :rtype: UserOut

    :raises HTTPException 409: If the account already exists.
    """
    # print(current_user.role)

    exist_user = await users_repository.get_user_by_email(new_user.email)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    new_user.password = pwd_handler.get_password_hash(new_user.password)
    new_user = await users_repository.create_user(new_user)

    return new_user


@router.post("/login")
async def login(
    login_form: OAuth2PasswordRequestForm = Depends(),
    users_repository: AbstractUserRepository = Depends(get_users_repository),
    pwd_handler: AbstractPasswordHashHandler = Depends(get_password_handler),
) -> Token:
    """
    Endpoint for user login.

    :param login_form: The login form containing username (email) and password.
    :type login_form: OAuth2PasswordRequestForm

    :param users_repository: The repository for user data.
    :type users_repository: AbstractUserRepository

    :param pwd_handler: The password hashing handler.
    :type pwd_handler: AbstractPasswordHashHandler

    :param auth_service: The JWT handling service.
    :type auth_service: HandleJWT

    :return: The generated access and refresh tokens.
    :rtype: Token

    :raises HTTPException 401: If the email, password, or email verification is invalid.
    """
    # confusing! email address is a username in body of login request
    user = await users_repository.get_user_by_email(login_form.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )

    if not pwd_handler.verify_password(login_form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    # Generate JWT
    payload = {"sub": user.email}
    access_token = await auth_service.create_access_token(data=payload)
    refresh_token = await auth_service.create_refresh_token(data=payload)
    await users_repository.update_token(user, refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/promote/{user_id}")
async def promote_user(
    user_id: int,
    current_user: UserOut = Depends(get_current_user),
    users_repository: AbstractUserRepository = Depends(get_users_repository),
) -> UserOut:
    if not current_user.role == "administrator":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admin can do that"
        )
    user = await users_repository.get_user_by_id(user_id)
    user_changed = await users_repository.change_user_role(
        email=user.email, body=UserChangeRole(role="moderator")
    )
    return user_changed


@router.get("/refresh_token")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    users_repository: AbstractUserRepository = Depends(get_users_repository),
) -> Token:
    """
    Endpoint to refresh the access token using the refresh token.

    :param credentials: The HTTP Authorization Credentials containing the refresh token.
    :type credentials: HTTPAuthorizationCredentials

    :param users_repository: The repository for user data.
    :type users_repository: AbstractUserRepository

    :param auth_service: The JWT handling service.
    :type auth_service: HandleJWT

    :return: The generated access and refresh tokens.
    :rtype: Token

    :raises HTTPException 401: If the refresh token is invalid.
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await users_repository.get_user_by_email(email)
    if user.refresh_token != token:
        await users_repository.update_token(user, None)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    payload = {"sub": user.email}
    access_token = await auth_service.create_access_token(data=payload)
    refresh_token = await auth_service.create_refresh_token(data=payload)
    await users_repository.update_token(user, refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)
