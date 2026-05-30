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
