"""Read-only SQL guard shared by the sqlite-ro MCP server and its tests."""

import sqlite3
from pathlib import Path

ALLOWED_PREFIXES = ("select", "with")


def validate_read_only(sql: str) -> str:
    """Return the normalized statement or raise ValueError if it is not a single SELECT/WITH."""
    statement = sql.strip().rstrip(";").strip()
    if not statement:
        raise ValueError("empty query")
    if ";" in statement:
        raise ValueError("only a single statement is allowed")
    if not statement.lower().startswith(ALLOWED_PREFIXES):
        raise ValueError("only SELECT or WITH queries are allowed")
    return statement


def connect_read_only(db_path: str) -> sqlite3.Connection:
    """Open SQLite in read-only mode so writes fail even if the guard is bypassed."""
    path = Path(db_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"database not found: {path}")
    conn = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn
