from typing import Dict, Generator
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete
from os import getcwd, path
from pathlib import Path

from backend.app import settings
from backend.app.app import app
from backend.app.db.base import engine
from backend.app.models.users import User
from .utils import get_superuser_token_headers

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


def clean_directory(directory: Path):
    for file in directory.iterdir():
        if file.is_file():
            file.unlink()


@pytest.fixture()
def directory():
    filepath=path.join(getcwd(), 'logs')
    directory = Path(filepath)
    clean_directory(directory)
    
    return directory

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# src/api/routes
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def sample_data():
    return {"data": 42}


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# src/api/utils/native
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def sample_dict():
    return {"a": [1, 2, 3], "b": [2, 4, 6], "c": [3, 6, 9]}


@pytest.fixture
def mangled_sample_dict():
    # Value is not a list
    return {"a": [1, 2, 3], "b": [2, 4, 6], "c": {"foo": "bar"}}
