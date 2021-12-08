# app/api/api.py
from fastapi import APIRouter

from app.controllers import dataset

api_router = APIRouter()
api_router.include_router(dataset.router, tags=["dataset"])
