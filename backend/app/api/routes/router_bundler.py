from fastapi import APIRouter

from . import setup, login

api_router = APIRouter()

# Add routers here
api_router.include_router(setup.router, tags=["setup"])
api_router.include_router(login.router, tags=["login"])
