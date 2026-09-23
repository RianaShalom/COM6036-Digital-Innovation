from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task


# Creates a new task and saves it to the database.
def create_task(db: Session, task: Task) -> Task:
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


# Finds a task belonging to the specified user.
def get_task(db: Session, task_id: UUID, user_id: UUID) -> Task | None:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id,
    )
    return db.scalars(statement).first()


# Returns all tasks belonging to the specified user, ordered by deadline.
def get_tasks(db: Session, user_id: UUID) -> list[Task]:
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.deadline.asc())
    )
    return list(db.scalars(statement).all())


# Returns all outstanding tasks belonging to the specified user.
def get_outstanding_tasks(db: Session, user_id: UUID) -> list[Task]:
    statement = (
        select(Task)
        .where(
            Task.user_id == user_id,
            Task.status == "pending",
        )
        .order_by(Task.deadline.asc())
    )
    return list(db.scalars(statement).all())


# Saves changes made to an existing task.
def update_task(db: Session, task: Task) -> Task:
    db.commit()
    db.refresh(task)
    return task


# Deletes an existing task from the database.
def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()