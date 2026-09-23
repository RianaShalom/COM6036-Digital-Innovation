from datetime import datetime, timezone


def calculate_urgency(deadline: datetime) -> float:
    now = datetime.now(timezone.utc)

    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)

    hours_remaining = (
        deadline - now
    ).total_seconds() / 3600

    if hours_remaining <= 0:
        return 100.0                 # Overdue tasks receive the highest urgency score

    days_remaining = hours_remaining / 24

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

    return 10.0                      # Tasks with distant deadlines have lower urgency


def calculate_effort(estimated_hours: float) -> float:
    if estimated_hours <= 1:
        return 10.0
    if estimated_hours <= 2:
        return 25.0
    if estimated_hours <= 4:
        return 50.0
    if estimated_hours <= 8:
        return 75.0

    return 100.0                     # Larger tasks receive a higher effort score


def calculate_difficulty(difficulty: int) -> float:
    if not 1 <= difficulty <= 5:
        raise ValueError("Difficulty must be between 1 and 5.")

    return difficulty / 5 * 100       # Converts the 1–5 difficulty rating to a 0–100 score


# Calculates workload pressure from outstanding work and available study capacity.
def calculate_workload_pressure(
    outstanding_hours: float,
    days_available: float,
    daily_capacity_hours: float = 4.0,
) -> float:
    if outstanding_hours < 0:
        raise ValueError("Outstanding hours cannot be negative.")

    if days_available <= 0:
        return 100.0

    if daily_capacity_hours <= 0:
        raise ValueError("Daily capacity must be greater than zero.")

    available_capacity = days_available * daily_capacity_hours

    workload_pressure = (
        outstanding_hours / available_capacity
    ) * 100

    return round(max(0.0, min(100.0, workload_pressure)), 2)


def calculate_priority(
    deadline: datetime,
    estimated_hours: float,
    difficulty: int,
    workload_pressure: float = 0,
) -> float:

    urgency = calculate_urgency(deadline)
    effort = calculate_effort(estimated_hours)
    difficulty_score = calculate_difficulty(difficulty)

    workload = max(0.0, min(100.0, workload_pressure))  # Keeps workload within a valid range

    priority = (
        (urgency * 0.45)
        + (effort * 0.25)
        + (difficulty_score * 0.20)
        + (workload * 0.10)
    )

    # Urgency has the greatest weight because deadlines are the main priority factor
    return round(max(0.0, min(100.0, priority)), 2)


def priority_level(score: float) -> str:
    if score >= 80:
        return "critical"

    if score >= 60:
        return "high"

    if score >= 40:
        return "medium"

    return "low"                       # Converts the numerical score into a simple priority level