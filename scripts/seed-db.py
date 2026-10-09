"""Seed TeamFeed SQLite DB for S3: 20 members, 200 posts, 60 follows.

Usage (from repo root): uv run --directory backend python ../scripts/seed-db.py
DB path: TEAMFEED_DB env var, default backend/teamfeed.db.

TODO(build): align table/column names with the s2-done schema
(intentionally uncommon names: posts.body, posts.created_ts, follows.follower_member_id).
"""

import os
import random
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("TEAMFEED_DB", ROOT / "backend" / "teamfeed.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL DEFAULT 'MEMBER'
);
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    author_member_id INTEGER NOT NULL REFERENCES members(id),
    body TEXT NOT NULL,
    created_ts TEXT NOT NULL,
    is_hidden INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS follows (
    follower_member_id INTEGER NOT NULL REFERENCES members(id),
    followee_member_id INTEGER NOT NULL REFERENCES members(id),
    PRIMARY KEY (follower_member_id, followee_member_id)
);
"""


def main() -> None:
    random.seed(42)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.executescript("DELETE FROM follows; DELETE FROM posts; DELETE FROM members;")

    members = [(i, f"member{i:02d}", "ADMIN" if i == 1 else "MEMBER") for i in range(1, 21)]
    conn.executemany("INSERT INTO members (id, name, role) VALUES (?, ?, ?)", members)

    base = datetime(2026, 10, 1, tzinfo=timezone.utc)
    posts = [
        (i, random.randint(1, 20), f"post #{i} from TeamFeed", (base + timedelta(minutes=17 * i)).isoformat())
        for i in range(1, 201)
    ]
    conn.executemany("INSERT INTO posts (id, author_member_id, body, created_ts) VALUES (?, ?, ?, ?)", posts)

    pairs: set[tuple[int, int]] = set()
    while len(pairs) < 60:
        a, b = random.sample(range(1, 21), 2)
        pairs.add((a, b))
    conn.executemany("INSERT INTO follows (follower_member_id, followee_member_id) VALUES (?, ?)", sorted(pairs))

    conn.commit()
    conn.close()
    print(f"seeded {DB_PATH}: 20 members, 200 posts, 60 follows")


if __name__ == "__main__":
    main()
