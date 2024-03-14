import pytest
from sqlalchemy import create_engine

# Define your database URL here
database_url = "postgresql://username@localhost/database_name"

def test_db_connection():
    try:
        engine = create_engine(database_url)
        engine.connect()
    except Exception as e:
        pytest.fail(f"Database connection error: {e}")

def test_db_connection_success():
    engine = create_engine(database_url)
    assert engine.connect() is not None, "Database connection unsuccessful."
