from fastapi import Depends
from typing_extensions import Annotated
from jwt import PyJWTError, decode
from pydantic import ValidationError

from ... import settings

from ...models.users import User, UserPublic

from ...exceptions import (
    CredentialsException,
    UserNotFoundException,
    InactiveUserException,
    InsufficientPrivilegesException,
)

from .auth import TokenDependency

from ...models.token import TokenPayload


def get_current_user(token: TokenDependency) -> User:
    try:
        secret = settings.SECRET_KEY
        algorithms = [settings.JWT_ALGORITHM]
        payload = decode(token, secret, algorithms=algorithms)
        
        token_data = TokenPayload(**payload)
        
    except (PyJWTError, ValidationError):
        raise CredentialsException()
    
    db_user = UserPublic(email=token_data.sub)
    
    return db_user


# Dependency to get the current user
CurrentUserDependency = Annotated[User, Depends(get_current_user)]
