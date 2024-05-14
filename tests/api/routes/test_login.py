from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlmodel import Session, select
from typing import Dict

from backend.app.core.config import settings
from backend.app.api.utils.security import verify_password
from backend.app.models.users import User


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()

    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "incorrect",
    }
    route = f"{settings.API_V1_STR}/login/access-token"
    r = client.post(route, data=login_data)
    assert r.status_code == 400


def test_use_access_token(
    client: TestClient, 
    superuser_token_headers: Dict[str, str]
) -> None:
    route = f"{settings.API_V1_STR}/login/test-token"
    
    r = client.post(route, headers=superuser_token_headers)
    result = r.json()

    assert r.status_code == 200
    assert "email" in result
