from datetime import datetime, timedelta, timezone

import pytest

from app.services.priority_service import (
    calculate_difficulty,
    calculate_effort,
    calculate_priority,
    calculate_urgency,
    calculate_workload_pressure,
    priority_level,
)


def test_overdue_task_has_maximum_urgency():
    deadline = datetime.now(timezone.utc) - timedelta(hours=1)

    assert calculate_urgency(deadline) == 100.0


def test_task_due_within_one_day_has_high_urgency():
    deadline = datetime.now(timezone.utc) + timedelta(hours=12)

    assert calculate_urgency(deadline) == 95.0


def test_distant_deadline_has_low_urgency():
    deadline = datetime.now(timezone.utc) + timedelta(days=30)

    assert calculate_urgency(deadline) == 10.0


def test_effort_score_increases_with_estimated_hours():
    assert calculate_effort(1) == 10.0
    assert calculate_effort(2) == 25.0
    assert calculate_effort(4) == 50.0
    assert calculate_effort(8) == 75.0
    assert calculate_effort(10) == 100.0


def test_difficulty_is_converted_to_percentage():
    assert calculate_difficulty(1) == 20.0
    assert calculate_difficulty(3) == 60.0
    assert calculate_difficulty(5) == 100.0


def test_invalid_difficulty_is_rejected():
    with pytest.raises(ValueError):
        calculate_difficulty(0)

    with pytest.raises(ValueError):
        calculate_difficulty(6)


def test_priority_is_between_zero_and_one_hundred():
    deadline = datetime.now(timezone.utc) + timedelta(days=2)

    score = calculate_priority(
        deadline=deadline,
        estimated_hours=4,
        difficulty=3,
        workload_pressure=50,
    )

    assert 0 <= score <= 100


def test_higher_workload_increases_priority():
    deadline = datetime.now(timezone.utc) + timedelta(days=4)

    low_workload = calculate_priority(
        deadline=deadline,
        estimated_hours=4,
        difficulty=3,
        workload_pressure=10,
    )

    high_workload = calculate_priority(
        deadline=deadline,
        estimated_hours=4,
        difficulty=3,
        workload_pressure=90,
    )

    assert high_workload > low_workload


def test_priority_level_critical():
    assert priority_level(80) == "critical"
    assert priority_level(95) == "critical"


def test_priority_level_high():
    assert priority_level(60) == "high"
    assert priority_level(79.99) == "high"


def test_priority_level_medium():
    assert priority_level(40) == "medium"
    assert priority_level(59.99) == "medium"


def test_priority_level_low():
    assert priority_level(0) == "low"
    assert priority_level(39.99) == "low"

def test_workload_pressure_is_based_on_available_capacity():
    pressure = calculate_workload_pressure(
        outstanding_hours=8,
        days_available=4,
        daily_capacity_hours=4,
    )

    assert pressure == 50.0


def test_workload_pressure_reaches_one_hundred_when_capacity_is_exceeded():
    pressure = calculate_workload_pressure(
        outstanding_hours=20,
        days_available=4,
        daily_capacity_hours=4,
    )

    assert pressure == 100.0


def test_workload_pressure_is_zero_when_no_work_is_outstanding():
    pressure = calculate_workload_pressure(
        outstanding_hours=0,
        days_available=4,
        daily_capacity_hours=4,
    )

    assert pressure == 0.0


def test_workload_pressure_is_maximum_for_overdue_work():
    pressure = calculate_workload_pressure(
        outstanding_hours=5,
        days_available=0,
        daily_capacity_hours=4,
    )

    assert pressure == 100.0


def test_negative_outstanding_hours_are_rejected():
    with pytest.raises(ValueError):
        calculate_workload_pressure(
            outstanding_hours=-1,
            days_available=4,
        )


def test_invalid_daily_capacity_is_rejected():
    with pytest.raises(ValueError):
        calculate_workload_pressure(
            outstanding_hours=4,
            days_available=2,
            daily_capacity_hours=0,
        )