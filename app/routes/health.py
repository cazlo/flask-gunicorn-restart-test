# app/routes/health.py
from fastapi import APIRouter
from ..database import db
from sqlalchemy import text

health_router = APIRouter()

@health_router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Execute a simple query to check database connectivity
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": f"error: {str(e)}"}