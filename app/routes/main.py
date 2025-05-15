# app/routes/main.py
import time
from random import random

from flask import Blueprint, jsonify, current_app
from datetime import datetime
# from ..database import get_db
from ..database import db
from sqlalchemy import text
import logging

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)


@main_bp.route('/')
def index():
    """Main index route"""
    # Record visit
    try:
        # db.session.execute(db.select("1")).scalar_one_or_none()
        # engine = get_db()
        # with engine.connect() as conn:
        # db.session.begin()
        db.session.execute(
                text("INSERT INTO visits (timestamp, path) VALUES (:timestamp, :path)"),
                {"timestamp": datetime.now(), "path": "/"}
            )
        db.session.commit()
        # time.sleep(random() * 500 / 1000)

    except Exception as e:
        logger.error(f"Database error: {e}")

    return jsonify({
        "message": f"Welcome to {current_app.config['APP_TITLE']}",
        "timestamp": datetime.now().isoformat()
    })
