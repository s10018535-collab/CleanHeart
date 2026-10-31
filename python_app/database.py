import sqlite3
from contextlib import closing
from datetime import datetime, timedelta, timezone

from config import DB_PATH, DEPARTMENTS, SEED_ISSUES

SCHEMA = """
CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK (length(title) BETWEEN 3 AND 120),
    description TEXT NOT NULL CHECK (length(description) BETWEEN 10 AND 2000),
    address TEXT NOT NULL CHECK (length(address) BETWEEN 5 AND 200),
    department TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'normal' CHECK (priority IN ('normal', 'urgent')),
    status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'in_progress', 'resolved')),
    photo_url TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS issues_department_created_idx ON issues (department, created_at DESC);
"""


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with closing(_connect()) as connection, connection:
        connection.executescript(SCHEMA)
        existing = connection.execute("SELECT COUNT(*) FROM issues").fetchone()[0]
        if existing:
            return
        now = datetime.now(timezone.utc)
        for seed in SEED_ISSUES:
            created_at = now - timedelta(hours=seed["hours_ago"])
            connection.execute(
                """
                INSERT INTO issues (title, description, address, department, priority, status, photo_url, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    seed["title"],
                    seed["description"],
                    seed["address"],
                    seed["department"],
                    seed["priority"],
                    seed["status"],
                    DEPARTMENTS[seed["department"]]["photo"],
                    created_at.isoformat(timespec="seconds"),
                ),
            )


def list_issues(department: str | None = None, limit: int = 100) -> list[dict]:
    query = "SELECT * FROM issues"
    params: tuple = ()
    if department is not None:
        query += " WHERE department = ?"
        params = (department,)
    query += " ORDER BY created_at DESC LIMIT ?"
    with closing(_connect()) as connection:
        rows = connection.execute(query, (*params, limit)).fetchall()
    return [dict(row) for row in rows]


def insert_issue(
    title: str,
    description: str,
    address: str,
    department: str,
    priority: str,
    photo_url: str,
) -> None:
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with closing(_connect()) as connection, connection:
        connection.execute(
            """
            INSERT INTO issues (title, description, address, department, priority, status, photo_url, created_at)
            VALUES (?, ?, ?, ?, ?, 'new', ?, ?)
            """,
            (title, description, address, department, priority, photo_url, created_at),
        )


def update_status(issue_id: int, department: str, status: str) -> bool:
    with closing(_connect()) as connection, connection:
        cursor = connection.execute(
            "UPDATE issues SET status = ? WHERE id = ? AND department = ?",
            (status, issue_id, department),
        )
        return cursor.rowcount > 0
