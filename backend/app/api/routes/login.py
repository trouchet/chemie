from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse


from ..dependencies.session import DatabaseSessionDependency
from ..dependencies.auth import PasswordFormDependency
from ..dependencies.users import CurrentUserDependency

from ... import settings
from ..utils.security import (
    get_password_hash,
    create_access_token,
)

from backend.app.exceptions import (
    WrongCredentialsException,
    InactiveUserException,
    InvalidTokenException,
    InexistentUserByEmailException,
)

from ...models.email import Message
from ...models.token import Token
from ...models.users import NewPassword, UserPublic
from backend.app.api.utils.security import get_password_hash,  verify_password

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(
    session: DatabaseSessionDependency, form_data: PasswordFormDependency
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    username = form_data.username
    password = form_data.password
    
    hashed_password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
    is_super_user = (verify_password(password, hashed_password)) and \
                    (settings.FIRST_SUPERUSER == username)

    if not is_super_user:
        raise WrongCredentialsException()

    expire_timedelta_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expires = timedelta(minutes=expire_timedelta_minutes)
    
    token_data = username
    access_token = create_access_token(token_data, expires_delta=access_token_expires)

    return Token(access_token=access_token)

@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUserDependency) -> Any:
    """
    Test access token
    """
    return current_user


