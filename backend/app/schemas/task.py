from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# Defines the common fields used when creating or returning a task.
class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    module: str = Field(min_length=1, max_length=100)
    deadline: datetime
    estimated_hours: Decimal = Field(gt=0, le=100)
    difficulty: int = Field(ge=1, le=5)


# Defines the data required when creating a new task.
class TaskCreate(TaskBase):
    pass


# Defines the optional fields that can be changed when updating a task.
class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    module: str | None = Field(default=None, min_length=1, max_length=100)
    deadline: datetime | None = None
    estimated_hours: Decimal | None = Field(default=None, gt=0, le=100)
    difficulty: int | None = Field(default=None, ge=1, le=5)


# Defines the task data returned by the API to the frontend.
class TaskResponse(TaskBase):
    # Allows Pydantic to create this response from a SQLAlchemy model.
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
    completed_at: datetime | None = None


# Extends the task response with the calculated priority information.
class TaskPriorityResponse(TaskResponse):
    priority_score: float
    priority_level: str