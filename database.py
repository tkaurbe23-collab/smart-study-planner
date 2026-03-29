import sqlite3

DB_NAME = "study_planner.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            task_name TEXT NOT NULL,
            deadline TEXT NOT NULL,
            estimated_hours REAL NOT NULL,
            difficulty INTEGER NOT NULL,
            importance INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_task(subject, task_name, deadline, estimated_hours, difficulty, importance):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (subject, task_name, deadline, estimated_hours, difficulty, importance)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (subject, task_name, deadline, estimated_hours, difficulty, importance))

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    conn.close()
    return rows


def mark_task_completed(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    conn.commit()
    conn.close()