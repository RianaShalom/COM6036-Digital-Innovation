from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import uuid4

from app.core.security import hash_password
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate
from app.services import task_service
from app.services.priority_service import priority_level


def create_test_user(db, email: str) -> User:
    # Creates a user specifically for integration testing.
    user = User(
        email=email,
        password_hash=hash_password("TestPassword123!"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_task(
    db,
    user_id,
    title: str,
    deadline: datetime,
    estimated_hours: Decimal,
    difficulty: int,
    status: str = "pending",
) -> Task:
    # Creates a task directly in PostgreSQL for integration testing.
    task = Task(
        user_id=user_id,
        title=title,
        description="Integration test task",
        module="COM6036",
        deadline=deadline,
        estimated_hours=estimated_hours,
        difficulty=difficulty,
        status=status,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def test_create_task_saves_task_to_database(db):
    user = create_test_user(db, "create@example.com")

    task_data = TaskCreate(
        title="Integration test",
        description="Test task creation",
        module="COM6036",
        deadline=datetime.now(timezone.utc) + timedelta(days=5),
        estimated_hours=Decimal("3.00"),
        difficulty=3,
    )

    task = task_service.create_task(
        db=db,
        task_data=task_data,
        user_id=user.id,
    )

    assert task.id is not None
    assert task.user_id == user.id
    assert task.title == "Integration test"
    assert task.status == "pending"


def test_prioritised_tasks_are_returned_in_priority_order(db):
    user = create_test_user(db, "priority@example.com")

    now = datetime.now(timezone.utc)

    urgent_task = create_test_task(
        db=db,
        user_id=user.id,
        title="Urgent task",
        deadline=now + timedelta(days=1),
        estimated_hours=Decimal("4.00"),
        difficulty=4,
    )

    distant_task = create_test_task(
        db=db,
        user_id=user.id,
        title="Distant task",
        deadline=now + timedelta(days=10),
        estimated_hours=Decimal("2.00"),
        difficulty=2,
    )

    prioritised = task_service.get_prioritised_tasks(
        db=db,
        user_id=user.id,
    )

    assert len(prioritised) == 2
    assert prioritised[0][0].id == urgent_task.id
    assert prioritised[1][0].id == distant_task.id

    # Confirms that the service returns calculated scores and levels.
    assert prioritised[0][1] > prioritised[1][1]
    assert prioritised[0][2] == priority_level(prioritised[0][1])


def test_completed_tasks_are_excluded_from_prioritisation(db):
    user = create_test_user(db, "completed@example.com")

    now = datetime.now(timezone.utc)

    pending_task = create_test_task(
        db=db,
        user_id=user.id,
        title="Pending task",
        deadline=now + timedelta(days=2),
        estimated_hours=Decimal("3.00"),
        difficulty=3,
        status="pending",
    )

    create_test_task(
        db=db,
        user_id=user.id,
        title="Completed task",
        deadline=now + timedelta(days=1),
        estimated_hours=Decimal("5.00"),
        difficulty=5,
        status="completed",
    )

    prioritised = task_service.get_prioritised_tasks(
        db=db,
        user_id=user.id,
    )

    assert len(prioritised) == 1
    assert prioritised[0][0].id == pending_task.id


def test_complete_task_changes_status_and_records_completion_time(db):
    user = create_test_user(db, "complete@example.com")

    task = create_test_task(
        db=db,
        user_id=user.id,
        title="Task to complete",
        deadline=datetime.now(timezone.utc) + timedelta(days=3),
        estimated_hours=Decimal("2.00"),
        difficulty=2,
    )

    completed_task = task_service.complete_task(
        db=db,
        task_id=task.id,
        user_id=user.id,
    )

    assert completed_task is not None
    assert completed_task.status == "completed"
    assert completed_task.completed_at is not None


def test_complete_task_returns_none_for_missing_task(db):
    user = create_test_user(db, "missing@example.com")

    missing_task = task_service.get_task(
        db=db,
        task_id=uuid4(),
        user_id=user.id,
    )

    assert missing_task is None


def test_users_can_only_prioritise_their_own_tasks(db):
    first_user = create_test_user(db, "first@example.com")
    second_user = create_test_user(db, "second@example.com")

    now = datetime.now(timezone.utc)

    first_task = create_test_task(
        db=db,
        user_id=first_user.id,
        title="First user's task",
        deadline=now + timedelta(days=2),
        estimated_hours=Decimal("3.00"),
        difficulty=3,
    )

    create_test_task(
        db=db,
        user_id=second_user.id,
        title="Second user's task",
        deadline=now + timedelta(days=1),
        estimated_hours=Decimal("6.00"),
        difficulty=5,
    )

    prioritised = task_service.get_prioritised_tasks(
        db=db,
        user_id=first_user.id,
    )

    assert len(prioritised) == 1
    assert prioritised[0][0].id == first_task.id
    assert prioritised[0][0].user_id == first_user.id