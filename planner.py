from datetime import datetime


def calculate_priority(deadline, difficulty, importance, estimated_hours):
    today = datetime.today().date()
    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()

    days_left = (deadline_date - today).days

    if days_left < 0:
        days_left = 0

    urgency_score = 10 / (days_left + 1)
    difficulty_score = difficulty * 2
    importance_score = importance * 3
    workload_score = estimated_hours

    total_score = urgency_score + difficulty_score + importance_score + workload_score
    return round(total_score, 2)