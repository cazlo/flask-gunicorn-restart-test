# app/routes/main.py
import time
from random import random
from datetime import datetime
import logging
from fastapi import APIRouter, Depends
from sqlalchemy import text
from fastapi.responses import JSONResponse
from ..config import Config
from ..database import db

main_router = APIRouter()
logger = logging.getLogger(__name__)

@main_router.get("/")
async def index():
    """Main index route"""
    # Record visit
    try:
        db.execute(
            text("INSERT INTO visits (timestamp, path) VALUES (:timestamp, :path)"),
            {"timestamp": datetime.now(), "path": "/"}
        )
        db.commit()
    except Exception as e:
        logger.error(f"Database error: {e}")

    return {
        "message": f"Welcome to {Config.APP_TITLE}",
        "timestamp": datetime.now().isoformat()
    }