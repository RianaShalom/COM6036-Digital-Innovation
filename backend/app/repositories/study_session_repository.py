from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.study_session import StudySession


# Creates and persists a study session.
def create_study_session(
    db: Session,
    study_session: StudySession,
) -> StudySession:
    try:
        db.add(study_session)
        db.commit()
        db.refresh(study_session)
        return study_session
    except Exception:
        db.rollback()
        raise


# Calculates the total recorded study time for a user in minutes.
def get_total_minutes_for_user(
    db: Session,
    user_id: UUID,
) -> int:
    total = (
        db.query(func.coalesce(func.sum(StudySession.duration_minutes), 0))
        .filter(StudySession.user_id == user_id)
        .scalar()
    )

    return int(total or 0)