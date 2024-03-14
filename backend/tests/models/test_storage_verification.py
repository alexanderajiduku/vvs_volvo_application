import pytest
from sqlalchemy.orm import sessionmaker
from app.models.calibrationdata import CalibrationData
from app.database.database import engine

@pytest.fixture
def session():
    # Create a new session
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_data_integrity(session):
    test_matrix = [[1000, 0, 640], [0, 1000, 360], [0, 0, 1]]
    test_distortion = [0.1, -0.01, 0, 0, 0]
    calibration_data = CalibrationData(matrix=test_matrix, distortion=test_distortion)
    session.add(calibration_data)
    session.commit()

    retrieved_data = session.query(CalibrationData).first()
    assert retrieved_data.matrix == test_matrix, "Matrix data integrity check failed"
    assert retrieved_data.distortion == test_distortion, "Distortion data integrity check failed"
