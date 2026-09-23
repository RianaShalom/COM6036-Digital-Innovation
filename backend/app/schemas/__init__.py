from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service


router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)


# Returns the database session used by the current request.
def get_database(db: Session = Depends(get_db)) -> Session:
    return db


# Creates a new task for the current user.
@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_database),
):
    # Temporary user ID until JWT authentication is implemented.
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    return task_service.create_task(
        db=db,
        task_data=task_data,
        user_id=user_id,
    )


# Returns all tasks belonging to the current user.
@router.get(
    "",
    response_model=list[TaskResponse],
)
def get_tasks(
    db: Session = Depends(get_database),
):
    # Temporary user ID until JWT authentication is implemented.
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    return task_service.get_tasks(
        db=db,
        user_id=user_id,
    )


# Returns one task belonging to the current user.
@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_database),
):
    # Temporary user ID until JWT authentication is implemented.
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    task = task_service.get_task(
        db=db,
        task_id=task_id,
        user_id=user_id,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return task


# Updates an existing task belonging to the current user.
@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    db: Session = Depends(get_database),
):
    # Temporary user ID until JWT authentication is implemented.
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    task = task_service.update_task(
        db=db,
        task_id=task_id,
        task_data=task_data,
        user_id=user_id,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return task


# Deletes an existing task belonging to the current user.
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_database),
):
    # Temporary user ID until JWT authentication is implemented.
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    deleted = task_service.delete_task(
        db=db,
        task_id=task_id,
        user_id=user_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )