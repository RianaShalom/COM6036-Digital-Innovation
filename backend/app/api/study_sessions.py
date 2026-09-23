from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.study_session import (
    StudySessionCreate,
    StudySessionResponse,
)
from app.services import study_session_service

router = APIRouter(
    prefix="/api/study-sessions",
    tags=["study-sessions"],
)


@router.post(
    "",
    response_model=StudySessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_study_session(
    session_data: StudySessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record study time against the authorised user's task."""
    study_session = study_session_service.create_study_session(
        db,
        session_data,
        current_user.id,
    )

    if study_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return study_session


@router.get("/summary")
def get_study_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return the total recorded study time for the authorised user."""
    total_minutes = study_session_service.get_total_study_minutes(
        db,
        current_user.id,
    )

    return {
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60, 2),
    }