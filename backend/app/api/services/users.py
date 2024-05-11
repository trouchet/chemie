from typing import Any, Union

from sqlmodel import Session, select

from ..utils.security import get_password_hash, verify_password
from ...models.users import User, UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    password_dict = {"hashed_password": get_password_hash(user_create.password)}
    db_obj = User.model_validate(user_create, update=password_dict)

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)

    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password

    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def get_user_by_email(*, session: Session, email: str) -> Union[User, None]:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()

    return session_user


def authenticate(*, session: Session, email: str, password: str) -> Union[User, None]:
    db_user = get_user_by_email(session=session, email=email)

    if not db_user:
        return None

    if not verify_password(password, db_user.hashed_password):
        return None

    return db_user
