from sqlalchemy import create_engine

# Define your database URL here
database_url = "postgresql://username@localhost/database_name"

try:
    engine = create_engine(database_url)
    engine.connect()
    print("Database connection successful.")
except Exception as e:
    print(f"Database connection error: {e}")
