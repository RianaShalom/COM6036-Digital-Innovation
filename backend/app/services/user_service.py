from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories import user_repository
from app.schemas.user import UserCreate


# Registers a new user and securely hashes their password before storage.
def register_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    existing_user = user_repository.get_user_by_email(
        db,
        user_data.email,
    )

    if existing_user is not None:
        raise ValueError("A user with this email already exists.")

    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )

    return user_repository.create_user(db, user)


# Authenticates a user by checking their email and password.
def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = user_repository.get_user_by_email(db, email)

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


# Retrieves a user by their unique ID.
def get_user(
    db: Session,
    user_id: UUID,
) -> User | None:
    return user_repository.get_user_by_id(db, user_id)