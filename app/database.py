# app/database.py
from flask import current_app, g
from sqlalchemy import create_engine, text
import logging
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
# from . import db

logger = logging.getLogger(__name__)


def get_db():
    """Get database connection"""
    if 'db_engine' not in g:
        g.db_engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    return g.db_engine


def close_db(e=None):
    """Close database connection"""
    db_engine = g.pop('db_engine', None)
    if db_engine is not None:
        logger.debug("Closing database connection")


def setup_db(app):
    """Setup database connection and teardown"""
    app.teardown_appcontext(close_db)


def init_db():
    """Initialize database tables"""
    try:
        engine = get_db()
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS visits
                (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP NOT NULL,
                    path VARCHAR(255) NOT NULL
                )
            """))
            conn.commit()
        return True
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        return False
