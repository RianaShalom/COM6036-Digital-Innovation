from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# Defines the data required when recording study time.
class StudySessionCreate(BaseModel):
    task_id: UUID
    duration_minutes: int = Field(gt=0, le=1440)


# Defines the data returned after a study session is recorded.
class StudySessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    task_id: UUID
    duration_minutes: int
    recorded_at: datetime