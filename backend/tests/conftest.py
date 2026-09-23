import pytest
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.database import Base
from app.models.task import Task
from app.models.user import User


# Creates a separate PostgreSQL database connection for integration tests.
TEST_DATABASE_URL = settings.database_url.rsplit("/", 1)[0] + "/studybuddy_test"


@pytest.fixture(scope="session")
def test_engine():
    # Creates all application tables in the dedicated test database.
    engine = create_engine(
        TEST_DATABASE_URL,
        pool_pre_ping=True,
    )
    Base.metadata.create_all(bind=engine)

    yield engine

    # Removes the test tables when the complete test session finishes.
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db(test_engine):
    # Creates a database session for an individual integration test.
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        # Rolls back any failed transaction before cleaning the test data.
        session.rollback()

        # Removes test records so each test starts with a clean database.
        session.execute(delete(Task))
        session.execute(delete(User))
        session.commit()

        session.close()