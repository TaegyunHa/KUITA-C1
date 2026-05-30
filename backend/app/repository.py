from datetime import datetime, timezone

from .db import connection

DEFAULT_PROFILE = {
    "postcode_area": "",
    "age_band": "25–34",
    "occupation": "Other",
    "interests": "",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_profile() -> dict:
    """Return the single profile row, creating a default one if none exists."""
    with connection() as conn:
        row = conn.execute("SELECT * FROM profile WHERE id = 1").fetchone()
    if row is None:
        return upsert_profile(DEFAULT_PROFILE)
    return dict(row)


def upsert_profile(data: dict) -> dict:
    """Insert or update the single profile row (id = 1)."""
    params = {**data, "updated_at": _now()}
    with connection() as conn:
        conn.execute(
            """
            INSERT INTO profile (id, postcode_area, age_band, occupation, interests, updated_at)
            VALUES (1, :postcode_area, :age_band, :occupation, :interests, :updated_at)
            ON CONFLICT(id) DO UPDATE SET
                postcode_area = excluded.postcode_area,
                age_band      = excluded.age_band,
                occupation    = excluded.occupation,
                interests     = excluded.interests,
                updated_at    = excluded.updated_at
            """,
            params,
        )
        row = conn.execute("SELECT * FROM profile WHERE id = 1").fetchone()
    return dict(row)


def insert_articles(articles: list[dict]) -> int:
    """Insert raw articles, ignoring duplicates by source_id. Returns inserted count."""
    now = _now()
    inserted = 0
    with connection() as conn:
        for a in articles:
            cur = conn.execute(
                """
                INSERT OR IGNORE INTO articles
                    (source, source_id, title, url, summary, published_at, fetched_at)
                VALUES (:source, :source_id, :title, :url, :summary, :published_at, :fetched_at)
                """,
                {**a, "fetched_at": now},
            )
            inserted += cur.rowcount
    return inserted


def list_articles(category: str | None = None) -> list[dict]:
    sql = "SELECT * FROM articles"
    params: tuple = ()
    if category:
        sql += " WHERE category = ?"
        params = (category,)
    sql += " ORDER BY COALESCE(published_at, fetched_at) DESC"
    with connection() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


def get_categorised_articles() -> list[dict]:
    with connection() as conn:
        rows = conn.execute(
            "SELECT * FROM articles WHERE category IS NOT NULL "
            "ORDER BY COALESCE(published_at, fetched_at) DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def get_uncategorised_articles(limit: int) -> list[dict]:
    with connection() as conn:
        rows = conn.execute(
            "SELECT id, title, summary FROM articles WHERE category IS NULL ORDER BY id LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def update_categories(updates: list[dict]) -> int:
    """Apply categorisation results. Each update: {id, category, tags, affects_whom}."""
    now = _now()
    updated = 0
    with connection() as conn:
        for u in updates:
            cur = conn.execute(
                """
                UPDATE articles
                SET category = :category, tags = :tags, affects_whom = :affects_whom,
                    categorised_at = :categorised_at
                WHERE id = :id
                """,
                {**u, "categorised_at": now},
            )
            updated += cur.rowcount
    return updated
