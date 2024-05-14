import random
import string

from typing import Dict
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.app import settings

from backend.app.models.users import User, UserCreate, UserUpdate


EMAIL_LEN = 5
def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=EMAIL_LEN))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()

    user_in = UserCreate(email=email, password=password)
    user = create_user(session=db, user_create=user_in)
    return user


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    route = f"{settings.API_V1_STR}/login/access-token"
    r = client.post(route, data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    return headers


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return user_authentication_headers(
        client=client,
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
    )


