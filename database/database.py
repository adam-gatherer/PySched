import os
import sqlite3
import json as jason

db_path = os.getenv("pysched_db_path", "./pysched.db")


def get_connection():
    return sqlite3.connect(db_path)


def init_db():
    # Create table if doesn't exist
    conn = get_connection()
    cursor = conn.cursor()

    # schema
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_name TEXT UNIQUE NOT NULL,
            command TEXT NOT NULL,
            job_type TEXT NOT NULL,
            start_time TEXT NOT NULL,
            run_days TEXT NOT NULL,
            conditions TEXT,
            timeout_seconds INTEGER DEFAULT 300,
            retry_count INTEGER DEFAULT 0,
            enabled BOOLEAN NOT NULL,
            description TEXT
        );
    """
    )
    conn.commit()
    conn.close()


def ensure_db_exists():
    if not os.path.exists(db_path):
        print("Creating database...")
    init_db()


def insert_job(job_data: dict):
    # Fetching data
    job_name = job_data.get("job_name")
    command = job_data.get("command")
    job_type = job_data.get("job_type")
    start_time = job_data.get("start_time")
    run_days = job_data.get("run_days", [])
    conditions = job_data.get("condition_type")
    retry_count = job_data.get("retry_count", 0)
    timeout_seconds = job_data.get("timeout_seconds", 300)
    enabled = job_data.get("enabled", True)
    description = job_data.get("description", "")

    # serialise list fields
    run_days_str = jason.dumps(run_days)
    conditions_str = jason.dumps(conditions)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO jobs (
                job_name, command, job_type, start_time, run_days,
                conditions, retry_count, timeout_seconds, enabled, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_name,
                command,
                job_type,
                start_time,
                run_days_str,
                conditions_str,
                retry_count,
                timeout_seconds,
                int(enabled),  # SQLite uses 0/1 for bools
                description,
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"A job with the name {job_name} already exists.")
    finally:
        conn.close()


def list_jobs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "select id, job_name, command, job_type, start_time, run_days, conditions, retry_count, timeout_seconds, enabled, description from jobs"
    )
    rows = cursor.fetchall()
    cursor.close()

    jobs = []
    for row in rows:
        job = {
            "id": row[0],
            "job_name": row[1],
            "command": row[2],
            "job_type": row[3],
            "start_time": row[4],
            "run_days": row[5],
            "conditions": row[6],
            "retry_count": row[7],
            "timeout_seconds": row[8],
            "enabled": bool(row[9]),
            "description": row[10],
        }
        jobs.append(job)
    return jobs


def get_job_by_name(job_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select * from jobs where job_name = ?", (job_name,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_job_by_id(job_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select * from jobs where id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def rm_job_by_name(job_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_name = ?", (job_name,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def rm_job_by_id(job_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
