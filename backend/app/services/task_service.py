from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories import task_repository
from app.schemas.task import TaskCreate, TaskUpdate


# Creates a new task for the specified user.
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


# Retrieves all tasks belonging to the specified user.
def get_tasks(
    db: Session,
    user_id: UUID,
) -> list[Task]:
    return task_repository.get_tasks(db, user_id)


# Retrieves a single task belonging to the specified user.
def get_task(
    db: Session,
    task_id: UUID,
    user_id: UUID,
) -> Task | None:
    return task_repository.get_task(db, task_id, user_id)


# Updates an existing task belonging to the specified user.
def update_task(
    db: Session,
    task_id: UUID,
    task_data: TaskUpdate,
    user_id: UUID,
) -> Task | None:
    task = task_repository.get_task(db, task_id, user_id)

    if task is None:
        return None

    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    return task_repository.update_task(db, task)


# Deletes an existing task belonging to the specified user.
def delete_task(
    db: Session,
    task_id: UUID,
    user_id: UUID,
) -> bool:
    task = task_repository.get_task(db, task_id, user_id)

    if task is None:
        return False

    task_repository.delete_task(db, task)
    return True


# Marks an existing task as completed.
def complete_task(
    db: Session,
    task_id: UUID,
    user_id: UUID,
) -> Task | None:
    task = task_repository.get_task(db, task_id, user_id)

    if task is None:
        return None

    task.status = "completed"
    task.completed_at = datetime.now(timezone.utc)

    return task_repository.update_task(db, task)