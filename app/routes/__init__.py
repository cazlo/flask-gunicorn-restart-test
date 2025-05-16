# app/routes/__init__.py
from fastapi import FastAPI
from .main import main_router
from .health import health_router

def register_routers(app: FastAPI):
    """Register all routers with the FastAPI application"""
    app.include_router(main_router)
    app.include_router(health_router)