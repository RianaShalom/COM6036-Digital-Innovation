from app.db.database import Base, engine
from app.models.task import Task
from app.models.user import User
from app.models.study_session import StudySession

def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
