"""sqlite-ro: read-only SQLite MCP server for the TeamFeed workshop (S3).

Run: TEAMFEED_DB=backend/teamfeed.db uv run --with mcp python templates/mcp/sqlite-ro-server/server.py
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from guard import connect_read_only, validate_read_only  # noqa: E402
from mcp.server.fastmcp import FastMCP  # noqa: E402

MAX_ROWS = 200

mcp = FastMCP("sqlite-ro")


def _db_path() -> str:
    db = os.environ.get("TEAMFEED_DB")
    if not db:
        raise RuntimeError("TEAMFEED_DB environment variable is not set")
    return db


@mcp.tool()
def list_tables() -> list[str]:
    """List user tables in the TeamFeed database."""
    with connect_read_only(_db_path()) as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
    return [r["name"] for r in rows]


@mcp.tool()
def describe_table(name: str) -> list[dict]:
    """Return column name, type, nullability and primary key flag for a table."""
    with connect_read_only(_db_path()) as conn:
        if name not in {r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}:
            raise ValueError(f"unknown table: {name}")
        rows = conn.execute(f'PRAGMA table_info("{name}")').fetchall()
    return [{"name": r["name"], "type": r["type"], "notnull": bool(r["notnull"]), "pk": bool(r["pk"])} for r in rows]


@mcp.tool()
def query(sql: str) -> list[dict]:
    """Run a single read-only SELECT/WITH statement (max 200 rows)."""
    statement = validate_read_only(sql)
    with connect_read_only(_db_path()) as conn:
        rows = conn.execute(statement).fetchmany(MAX_ROWS)
    return [dict(r) for r in rows]


if __name__ == "__main__":
    mcp.run()
