# app/api/api.py
"""Adds the controllers to the router"""
from fastapi import APIRouter
from app.controllers import dataset

router = APIRouter()
router.include_router(dataset.router, tags=["dataset"])
