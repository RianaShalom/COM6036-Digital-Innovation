import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"              # Stores the tasks created by users

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,              # Gives each task a unique identifier
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,                      # Links each task to its owner and speeds up lookups
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,                   # Allows users to provide additional task details
    )

    module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,                  # Identifies which academic module the task belongs to
    )

    deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,                      # Allows tasks to be efficiently sorted or filtered by deadline
    )

    estimated_hours: Mapped[Decimal] = mapped_column(
        Numeric(6, 2),
        nullable=False,                  # Records the expected effort needed to complete the task
    )

    difficulty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,                  # Stores the task difficulty for workload planning
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",               # Tracks whether a task is pending or completed
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,                   # Records when a task is completed
    )