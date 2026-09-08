import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    __tablename__ = "users"                         # Stores user account data in the users table

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,                         # Generates a unique ID for each user
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