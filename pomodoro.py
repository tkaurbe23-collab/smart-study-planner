def get_pomodoro_sessions(estimated_hours):
    total_minutes = estimated_hours * 60
    sessions = int(total_minutes // 25)

    if total_minutes % 25 != 0:
        sessions += 1

    return sessions