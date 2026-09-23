from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories import task_repository
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.priority_service import (
    calculate_priority,
    calculate_workload_pressure,
    priority_level,
)


# Creates a new task belonging to the authenticated user.
def create_task(
    db: Session,
    task_data: TaskCreate,
    user_id: UUID,
) -> Task:
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        module=task_data.module,
        deadline=task_data.deadline,
        estimated_hours=task_data.estimated_hours,
        difficulty=task_data.difficulty,
        status="pending",
    )

    return task_repository.create_task(db, task)


# Retrieves all tasks belonging to the authenticated user.
def get_tasks(
    db: Session,
    user_id: UUID,
) -> list[Task]:
    return task_repository.get_tasks(db, user_id)


# Retrieves one task, provided that it belongs to the authenticated user.
def get_task(
    db: Session,
    task_id: UUID,
    user_id: UUID,
) -> Task | None:
    return task_repository.get_task(
        db,
        task_id,
        user_id,
    )


# Updates a task belonging to the authenticated user.
def update_task(
    db: Session,
    task_id: UUID,
    task_data: TaskUpdate,
    user_id: UUID,
) -> Task | None:
    task = task_repository.get_task(
        db,
        task_id,
        user_id,
    )

    if task is None:
        return None

    update_data = task_data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    return task_repository.update_task(
        db,
        task,
    )


# Deletes a task belonging to the authenticated user.
def delete_task(
    db: Session,
    task_id: UUID,
    user_id: UUID,
) -> bool:
    task = task_repository.get_task(
        db,
        task_id,
        user_id,
    )

    if task is None:
        return False

    task_repository.delete_task(
        db,
        task,
    )

    return True


# Marks a task as completed and records when completion occurred.
def complete_task(
    db: Session,
    task_id: UUID,
    user_id: UUID,
) -> Task | None:
    task = task_repository.get_task(
        db,
        task_id,
        user_id,
    )

    if task is None:
        return None

    task.status = "completed"
    task.completed_at = datetime.now(timezone.utc)

    return task_repository.update_task(
        db,
        task,
    )


# Calculates and orders the user's outstanding tasks.
#
# The tuple structure is deliberately preserved because other parts
# of the application and the existing tests use this service contract.
def get_prioritised_tasks(
    db: Session,
    user_id: UUID,
    daily_capacity_hours: float = 4.0,
) -> list[tuple[Task, float, str]]:
    tasks = task_repository.get_outstanding_tasks(
        db,
        user_id,
    )

    if not tasks:
        return []

    now = datetime.now(timezone.utc)

    # Calculates the total amount of outstanding work.
    outstanding_hours = sum(
        float(task.estimated_hours)
        for task in tasks
    )

    prioritised_tasks = []

    for task in tasks:
        deadline = task.deadline

        # Ensures database timestamps without timezone information
        # can still be compared safely with the current UTC time.
        if deadline.tzinfo is None:
            deadline = deadline.replace(
                tzinfo=timezone.utc,
            )

        days_available = max(
            0.0,
            (deadline - now).total_seconds() / 86400,
        )

        # Calculates the workload pressure for this deadline.
        workload_pressure = calculate_workload_pressure(
            outstanding_hours=outstanding_hours,
            days_available=days_available,
            daily_capacity_hours=daily_capacity_hours,
        )

        score = calculate_priority(
            deadline=deadline,
            estimated_hours=float(task.estimated_hours),
            difficulty=task.difficulty,
            workload_pressure=workload_pressure,
        )

        prioritised_tasks.append(
            (
                task,
                score,
                priority_level(score),
            )
        )

    # Highest-priority tasks appear first on the dashboard.
    prioritised_tasks.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return prioritised_tasks