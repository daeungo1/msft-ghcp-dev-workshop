import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from guard import connect_read_only, validate_read_only  # noqa: E402


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT * FROM posts",
        "  select id from members;",
        "WITH t AS (SELECT 1) SELECT * FROM t",
    ],
)
def test_allows_single_read_statement(sql):
    assert validate_read_only(sql)


@pytest.mark.parametrize(
    "sql",
    [
        "INSERT INTO posts VALUES (1)",
        "UPDATE posts SET body = 'x'",
        "DELETE FROM posts",
        "DROP TABLE posts",
        "SELECT 1; DROP TABLE posts",
        "",
    ],
)
def test_rejects_writes_and_multiple_statements(sql):
    with pytest.raises(ValueError):
        validate_read_only(sql)


def test_connection_is_read_only(tmp_path):
    db = tmp_path / "t.db"
    setup = sqlite3.connect(db)
    setup.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY)")
    setup.commit()
    setup.close()

    conn = connect_read_only(str(db))
    with pytest.raises(sqlite3.OperationalError):
        conn.execute("INSERT INTO posts VALUES (1)")
    conn.close()
