import os
import sqlite3

db_path = os.getenv("pysched_db_path", "./pysched.db")


def get_connection():
    return sqlite3.connect(db_path)


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Example minimal schema — expand later
    cursor.execute("""
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
    """)
    conn.commit()
    conn.close()


def ensure_db_exists():
    """Call this from pysched.py before anything else runs."""
    if not os.path.exists(db_path):
        print("Creating database...")
    init_db()