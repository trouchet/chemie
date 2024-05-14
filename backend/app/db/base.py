from sqlmodel import Session, create_engine, select
from typing import Generator
from sqlmodel import SQLModel

from ..models.users import User, UserCreate
from backend.app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

