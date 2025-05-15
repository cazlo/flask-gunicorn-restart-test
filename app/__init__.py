# app/__init__.py
from flask import Flask
from sqlalchemy import text

from .config import Config
# from .database import init_db, setup_db
from .routes import register_blueprints
# from flask_sqlalchemy import SQLAlchemy
#
#
# db = SQLAlchemy()
from .database import db

def create_app(config_class=Config):
    """Application factory function to create and configure Flask app"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database connection
    # setup_db(app)
    db.init_app(app)

    # Register all blueprints
    register_blueprints(app)

    # Initialize database tables
    with app.app_context():
        # init_db()
        db.session.execute(text("""
                          CREATE TABLE IF NOT EXISTS visits
                          (
                              id
                              SERIAL
                              PRIMARY
                              KEY,
                              timestamp
                              TIMESTAMP
                              NOT
                              NULL,
                              path
                              VARCHAR
                          (
                              255
                          ) NOT NULL
                              )
                          """))
        db.session.commit()
        con = db.session.connection()
        con.engine.dispose()
        return app
