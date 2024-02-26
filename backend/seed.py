# database/seed.py
from app.database.database import SessionLocal
from app.models import User, Camera, CalibrationData, UploadedFile, AnnotatedFile, Model, UploadedImages
from datetime import datetime
from sqlalchemy.orm import Session

def seed_users(db: Session):
    users = [
        User(
            first_name="Alex",
            last_name="Ajiduku",
            username="aajiduku",
            email="jalexajiduku@gmail.com",
            hashed_password="123456789", 
            is_active=True,
            created_at=datetime.utcnow()
        ),
        User(
            first_name="Jane",
            last_name="Doe",
            username="janedoe",
            email="janedoe@example.com",
            hashed_password="hashed_janedoe_password",  # Assume pre-hashed
            is_active=True,
            created_at=datetime.utcnow()
        )
        # Add more users as needed
    ]
    db.bulk_save_objects(users)
    db.commit()

def seed_cameras(db: Session):
    cameras = [
        Camera(
            camera_name="Camera A",
            camera_model="Model A",
            checkerboard_width=9,
            checkerboard_height=6,
            description="Camera A Description"
        ),
        Camera(
            camera_name="Camera B",
            camera_model="Model B",
            checkerboard_width=8,
            checkerboard_height=5,
            description="Camera B Description"
        )
        # Add more cameras as needed
    ]
    db.bulk_save_objects(cameras)
    db.commit()

# Define similar seeding functions for CalibrationData, UploadedFile, AnnotatedFile, Model, and UploadedImages

def seed_all():
    db = SessionLocal()
    try:
        seed_users(db)
        seed_cameras(db)
        # Call other seed functions here
    except Exception as e:
        db.rollback()
        print(f"Error occurred during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_all()
# Run the seed script
# python backend/seed.py
