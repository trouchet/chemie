# Description: This file contains the setup routes for the FastAPI application.
from fastapi import APIRouter
import toml

from backend.app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    return dict(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status="OK",
        message="Visit /docs for more information.",
    )


@router.get("/info")
async def info():
    with open("pyproject.toml", "r") as f:
        config = toml.load(f)

    return {
        "name": config["tool"]["poetry"]["name"],
        "version": config["tool"]["poetry"]["version"],
        "description": config["tool"]["poetry"]["description"],
    }

