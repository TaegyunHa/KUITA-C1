import sqlite3
from contextlib import contextmanager
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "whatnow.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    source         TEXT NOT NULL,
    source_id      TEXT NOT NULL UNIQUE,
    title          TEXT NOT NULL,
    url            TEXT NOT NULL,
    summary        TEXT,
    published_at   TEXT,
    fetched_at     TEXT NOT NULL,
    category       TEXT,
    tags           TEXT,
    affects_whom   TEXT,
    categorised_at TEXT
);

CREATE TABLE IF NOT EXISTS profile (
    id            INTEGER PRIMARY KEY CHECK (id = 1),
    postcode_area TEXT NOT NULL,
    age_band      TEXT NOT NULL,
    occupation    TEXT NOT NULL,
    interests     TEXT NOT NULL,
    updated_at    TEXT NOT NULL
);
"""


@contextmanager
def connection():
    """Yield a SQLite connection, committing on success and always closing."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with connection() as conn:
        conn.executescript(SCHEMA)
