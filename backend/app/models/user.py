from datetime import datetime, timezone
import uuid

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task


class User(Base):
    __tablename__ = "users"                         # Stores user account data in the users table

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,                         # Generates a unique ID for each user
    )

    tasks: Mapped[list["Task"]] = relationship(
    back_populates="user",
    cascade="all, delete-orphan",
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,                                # Prevents multiple accounts using the same email
        nullable=False,
        index=True,                                 # Improves the speed of email-based lookups
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,                             # Stores the hashed password rather than the plain password
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc), # Records when the account was created in UTC
        nullable=False,
    )
    