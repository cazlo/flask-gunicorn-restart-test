# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from contextlib import contextmanager
from typing import Generator

from .config import Config

# Create SQLAlchemy engine and session
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Create a db instance similar to Flask-SQLAlchemy
class DatabaseSession:
    def __init__(self):
        self.session = None

    @contextmanager
    def get_session(self) -> Generator:
        if self.session is None:
            self.session = SessionLocal()
        try:
            yield self.session
        except Exception:
            self.session.rollback()
            raise
        finally:
            pass

    def commit(self):
        if self.session:
            self.session.commit()

    def execute(self, *args, **kwargs):
        if self.session is None:
            self.session = SessionLocal()
        return self.session.execute(*args, **kwargs)


# Create a db instance with similar interface to Flask-SQLAlchemy
db = DatabaseSession()


def init_db():
    """Initialize database tables"""
    with db.get_session() as session:
        session.execute(text("""
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
        session.commit()