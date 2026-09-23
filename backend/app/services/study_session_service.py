from uuid import UUID

from sqlalchemy.orm import Session

from app.models.study_session import StudySession
from app.repositories import study_session_repository
from app.repositories import task_repository
from app.schemas.study_session import StudySessionCreate


# Records study time against a task owned by the authenticated user.
def create_study_session(
    db: Session,
    session_data: StudySessionCreate,
    user_id: UUID,
) -> StudySession | None:
    task = task_repository.get_task(
        db,
        session_data.task_id,
        user_id,
    )

    if task is None:
        return None

    study_session = StudySession(
        user_id=user_id,
        task_id=session_data.task_id,
        duration_minutes=session_data.duration_minutes,
    )

    return study_session_repository.create_study_session(
        db,
        study_session,
    )


# Returns the total recorded study time for a user in minutes.
def get_total_study_minutes(
    db: Session,
    user_id: UUID,
) -> int:
    return study_session_repository.get_total_minutes_for_user(
        db,
        user_id,
    )