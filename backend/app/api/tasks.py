from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service

from app.schemas.task import (
    TaskCreate,
    TaskPriorityResponse,
    TaskResponse,
    TaskUpdate,
)

# Creates the router for authenticated task management endpoints.
router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)


# Creates a new task for the currently authenticated user.
@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.create_task(
        db=db,
        task_data=task_data,
        user_id=current_user.id,
    )


# Returns all tasks belonging to the currently authenticated user.
@router.get(
    "",
    response_model=list[TaskResponse],
)
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.get_tasks(
        db=db,
        user_id=current_user.id,
    )

# Returns the user's outstanding tasks ordered by calculated priority.
@router.get("/prioritized", response_model=list[TaskPriorityResponse])
def get_prioritised_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prioritised_tasks = task_service.get_prioritised_tasks(
        db=db,
        user_id=current_user.id,
    )

    return [
        {
            **task.__dict__,
            "priority_score": score,
            "priority_level": level,
        }
        for task, score, level in prioritised_tasks
    ]

# Marks a task as completed for the currently authenticated user.
@router.post("/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_service.complete_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return task

# Returns a single task belonging to the currently authenticated user.
@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_service.get_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return task


# Updates a task belonging to the currently authenticated user.
@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_service.update_task(
        db=db,
        task_id=task_id,
        task_data=task_data,
        user_id=current_user.id,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return task


# Deletes a task belonging to the currently authenticated user.
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = task_service.delete_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )