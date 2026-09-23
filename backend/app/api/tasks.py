from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service
from app.services.priority_service import (
    calculate_difficulty,
    calculate_effort,
    calculate_urgency,
    calculate_workload_pressure,
)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all tasks belonging to the authorised user."""
    return task_service.get_tasks(db, current_user.id)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new academic task for the authorised user."""
    return task_service.create_task(db, task_data, current_user.id)


@router.get("/prioritized")
def get_prioritised_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return outstanding tasks ordered by their calculated priority."""
    prioritised_tasks = task_service.get_prioritised_tasks(
        db,
        current_user.id,
    )

    if not prioritised_tasks:
        return []

    tasks = [item[0] for item in prioritised_tasks]

    outstanding_hours = sum(
        float(task.estimated_hours or 0)
        for task in tasks
        if task.status != "completed"
    )

    response = []

    for task, score, level in prioritised_tasks:
        deadline = task.deadline

        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        days_available = max(
            (deadline - now).total_seconds() / 86400,
            0,
        )

        workload_pressure = calculate_workload_pressure(
            outstanding_hours=outstanding_hours,
            days_available=days_available,
        )

        response.append(
            {
                **task.__dict__,
                "priority_score": score,
                "priority_level": level,
                "priority_factors": {
                    "urgency": calculate_urgency(task.deadline),
                    "effort": calculate_effort(float(task.estimated_hours)),
                    "difficulty": calculate_difficulty(task.difficulty),
                    "workload_pressure": round(workload_pressure, 2),
                },
            }
        )

    return response


@router.post("/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark an authorised user's task as completed."""
    task = task_service.complete_task(db, task_id, current_user.id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return one task belonging to the authorised user."""
    task = task_service.get_task(
        db,
        current_user.id,
        task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a task belonging to the authorised user."""
    task = task_service.update_task(
    db,
    task_id,
    task_data,
    current_user.id,
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a task belonging to the authorised user."""
    deleted = task_service.delete_task(
    db,
    task_id,
    current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return None