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
            condition_type TEXT,
            dependent_jobs TEXT,
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
    condition_type = job_data.get("condition_type")
    dependent_jobs = job_data.get("dependent_jobs", [])
    enabled = job_data.get("enabled", True)
    description = job_data.get("description", "")

    # serialise list fields
    run_days_str = jason.dumps(run_days)
    dependent_jobs_str = jason.dumps(dependent_jobs)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO jobs (
                job_name, command, job_type, start_time, run_days,
                condition_type, dependent_jobs, enabled, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_name,
                command,
                job_type,
                start_time,
                run_days_str,
                condition_type,
                dependent_jobs_str,
                int(enabled),  # SQLite uses 0/1 for bools
                description
            )
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError(f"A job with the name {job_name} already exists.")
    finally:
        conn.close()