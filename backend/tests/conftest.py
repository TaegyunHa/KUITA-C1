import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    """Point the app's SQLite DB at an isolated temp file and create the schema.

    `db.connection()` reads `DATA_DIR`/`DB_PATH` at call time, and `repository`
    calls `db.connection()` (not a copied constant), so patching the module
    globals reroutes every read/write in the test.
    """
    from app import db

    monkeypatch.setattr(db, "DATA_DIR", tmp_path)
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    db.init_db()
    return db


@pytest.fixture
def client(tmp_db):
    """A TestClient bound to the temp DB. Entering the context runs the app
    lifespan (init_db), which now targets the patched DB_PATH."""
    from app.main import app

    with TestClient(app) as c:
        yield c
