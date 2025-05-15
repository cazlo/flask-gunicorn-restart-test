# app/routes/health.py
from flask import Blueprint, jsonify
from datetime import datetime
# from ..database import get_db
from sqlalchemy import text
import logging
from ..database import db

health_bp = Blueprint('health', __name__)
logger = logging.getLogger(__name__)


@health_bp.route('/health')
def health():
    """Health check endpoint"""
    # Check database connection
    db_status = "healthy"
    try:
        # result = db.session.execute(db.select("1")).scalar_one_or_none()
        result = db.session.execute(text("SELECT 1"))
        if not result:
            db_status = "unhealthy"
    except Exception as e:
        logger.error(f"Health check error: {e}")
        db_status = f"unhealthy: {str(e)}"

    return jsonify({
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "db_status": db_status,
        "timestamp": datetime.now().isoformat()
    }), 200 if db_status == "healthy" else 500
