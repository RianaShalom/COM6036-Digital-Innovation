from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task


# Adds a new task to the database and returns the saved task.
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


# Retrieves all tasks belonging to the specified user.
def get_tasks(db: Session, user_id: UUID) -> list[Task]:
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.deadline.asc())
    )
    return list(db.scalars(statement).all())


# Saves changes made to an existing task and returns the updated task.
def update_task(db: Session, task: Task) -> Task:
    db.commit()
    db.refresh(task)
    return task


# Deletes the specified task from the database.
def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()