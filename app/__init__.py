# app/__init__.py
from fastapi import FastAPI
from sqlalchemy import text

from .config import Config
from .routes import register_routers
from .database import db, init_db


def create_app():
    """Application factory function to create and configure FastAPI app"""
    app = FastAPI(
        title=Config.APP_TITLE,
    )

    # Register all routers
    register_routers(app)

    # Initialize database tables - should happen before app startup
    @app.on_event("startup")
    async def startup_event():
        init_db()

    return app