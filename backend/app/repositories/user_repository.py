from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


# Finds a user by their email address.
def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return db.scalars(statement).first()


# Finds a user by their unique ID.
def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    statement = select(User).where(User.id == user_id)
    return db.scalars(statement).first()


# Adds a new user to the database and returns the saved user.
def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user