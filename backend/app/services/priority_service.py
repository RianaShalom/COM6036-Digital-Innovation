from datetime import datetime, timezone


# Calculates how urgent a task is based on the time remaining
# before its deadline.
def calculate_urgency(deadline: datetime) -> float:
    now = datetime.now(timezone.utc)

    if deadline.tzinfo is None:
        deadline = deadline.replace(
            tzinfo=timezone.utc,
        )

    days_remaining = (
        deadline - now
    ).total_seconds() / 86400

    if days_remaining < 0:
        return 100.0

    if days_remaining <= 1:
        return 95.0

    if days_remaining <= 2:
        return 85.0

    if days_remaining <= 4:
        return 70.0

    if days_remaining <= 7:
        return 50.0

    if days_remaining <= 14:
        return 30.0

    return 10.0


# Converts estimated study time into an effort score.
def calculate_effort(
    estimated_hours: float,
) -> float:
    if estimated_hours < 0:
        raise ValueError(
            "Estimated hours cannot be negative."
        )

    if estimated_hours <= 1:
        return 10.0

    if estimated_hours <= 2:
        return 25.0

    if estimated_hours <= 4:
        return 50.0

    if estimated_hours <= 8:
        return 75.0

    return 100.0


# Converts the user's 1-5 difficulty rating into
# a normalised 0-100 difficulty score.
def calculate_difficulty(
    difficulty: int,
) -> float:
    if difficulty < 1 or difficulty > 5:
        raise ValueError(
            "Difficulty must be between 1 and 5."
        )

    return (difficulty / 5) * 100


# Calculates how much outstanding work is competing
# with the available study capacity.
def calculate_workload_pressure(
    outstanding_hours: float,
    days_available: float,
    daily_capacity_hours: float = 4.0,
) -> float:
    if outstanding_hours < 0:
        raise ValueError(
            "Outstanding hours cannot be negative."
        )

    if daily_capacity_hours <= 0:
        raise ValueError(
            "Daily capacity must be greater than zero."
        )

    if days_available <= 0:
        return 100.0

    available_hours = (
        days_available * daily_capacity_hours
    )

    pressure = (
        outstanding_hours / available_hours
    ) * 100

    return min(100.0, pressure)


# Combines the four priority factors into one
# explainable weighted score.
def calculate_priority(
    deadline: datetime,
    estimated_hours: float,
    difficulty: int,
    workload_pressure: float,
) -> float:
    urgency = calculate_urgency(deadline)
    effort = calculate_effort(estimated_hours)
    difficulty_score = calculate_difficulty(
        difficulty,
    )

    score = (
        0.45 * urgency
        + 0.25 * effort
        + 0.20 * difficulty_score
        + 0.10 * workload_pressure
    )

    return round(score, 2)


# Converts the numerical score into the existing
# API priority categories.
def priority_level(score: float) -> str:
    if score >= 80:
        return "critical"

    if score >= 60:
        return "high"

    if score >= 40:
        return "medium"

    return "low"