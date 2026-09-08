from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.database_url,       # Uses the database URL from the application settings
    pool_pre_ping=True,          # Checks connections before use to avoid stale connections
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()        # Base class used by all database models


def get_db():
    db = SessionLocal()          # Creates a new database session for each request

    try:
        yield db
    finally:
        db.close()               # Ensures the database session is always closed