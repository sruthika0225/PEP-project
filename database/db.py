import sqlite3
from datetime import datetime
from config import Config

def get_connection():
    connection = sqlite3.connect(Config.DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    Config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                alarm_date TEXT NOT NULL,
                alarm_time TEXT NOT NULL,
                repeat TEXT NOT NULL DEFAULT 'once',
                status TEXT NOT NULL DEFAULT 'pending',
                alarm_triggered INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()

def create_task(title, description, alarm_date, alarm_time, repeat):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO tasks
            (title, description, alarm_date, alarm_time, repeat, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            title, description, alarm_date, alarm_time, repeat,
            datetime.now().isoformat(timespec="seconds")
        ))
        conn.commit()
        return cursor.lastrowid

def get_tasks():
    with get_connection() as conn:
        return [dict(row) for row in conn.execute("""
            SELECT * FROM tasks
            ORDER BY alarm_date ASC, alarm_time ASC
        """).fetchall()]

def get_active_tasks():
    with get_connection() as conn:
        return [dict(row) for row in conn.execute("""
            SELECT * FROM tasks
            WHERE status = 'pending'
            ORDER BY alarm_date ASC, alarm_time ASC
        """).fetchall()]

def get_task(task_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return dict(row) if row else None

def update_task(task_id, title, description, alarm_date, alarm_time, repeat):
    with get_connection() as conn:
        conn.execute("""
            UPDATE tasks
            SET title = ?, description = ?, alarm_date = ?, alarm_time = ?,
                repeat = ?, alarm_triggered = 0
            WHERE id = ?
        """, (title, description, alarm_date, alarm_time, repeat, task_id))
        conn.commit()

def update_alarm_time(task_id, alarm_date, alarm_time):
    with get_connection() as conn:
        conn.execute("""
            UPDATE tasks
            SET alarm_date = ?, alarm_time = ?, alarm_triggered = 0,
                status = 'pending'
            WHERE id = ?
        """, (alarm_date, alarm_time, task_id))
        conn.commit()

def delete_task(task_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

def complete_task(task_id):
    with get_connection() as conn:
        conn.execute("""
            UPDATE tasks SET status = 'completed'
            WHERE id = ?
        """, (task_id,))
        conn.commit()

def mark_alarm_triggered(task_id):
    task = get_task(task_id)
    if not task:
        return

    with get_connection() as conn:
        if task["repeat"] == "once":
            conn.execute("""
                UPDATE tasks
                SET alarm_triggered = 1, status = 'completed'
                WHERE id = ?
            """, (task_id,))
        else:
            conn.execute("""
                UPDATE tasks
                SET alarm_triggered = 0
                WHERE id = ?
            """, (task_id,))
        conn.commit()

def get_stats():
    with get_connection() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM tasks"
        ).fetchone()[0]
        pending = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'pending'"
        ).fetchone()[0]
        completed = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'completed'"
        ).fetchone()[0]

    now = datetime.now()
    overdue = 0
    for task in get_active_tasks():
        try:
            alarm_dt = datetime.strptime(
                f"{task['alarm_date']} {task['alarm_time']}",
                "%Y-%m-%d %H:%M"
            )
            if alarm_dt < now:
                overdue += 1
        except ValueError:
            pass

    return {
        "total": total,
        "pending": pending,
        "completed": completed,
        "overdue": overdue
    }

def reuse_task(task_id):
    with get_connection() as conn:
        conn.execute("""
            UPDATE tasks
            SET status = 'pending',
                alarm_triggered = 0
            WHERE id = ?
        """, (task_id,))
        conn.commit()