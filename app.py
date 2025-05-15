# app.py
from flask import Flask, jsonify
import os
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Database configuration
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'flask_app')

# Create SQLAlchemy engine
DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URI)


# Initialize database
def init_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("""
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
            conn.commit()
        return True
    except Exception as e:
        app.logger.error(f"Database initialization error: {e}")
        return False


@app.before_first_request
def setup():
    init_db()


@app.route('/')
def index():
    # Record visit
    try:
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO visits (timestamp, path) VALUES (:timestamp, :path)"),
                {"timestamp": datetime.now(), "path": "/"}
            )
            conn.commit()
    except Exception as e:
        app.logger.error(f"Database error: {e}")

    return jsonify({
        "message": "Welcome to Flask App",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/health')
def health():
    # Check database connection
    db_status = "healthy"
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            if not result.scalar():
                db_status = "unhealthy"
    except Exception as e:
        app.logger.error(f"Health check error: {e}")
        db_status = f"unhealthy: {str(e)}"

    return jsonify({
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "db_status": db_status,
        "timestamp": datetime.now().isoformat()
    }), 200 if db_status == "healthy" else 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)