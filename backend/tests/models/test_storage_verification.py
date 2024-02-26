import unittest

from sqlalchemy.orm import sessionmaker
from app.models.calibrationdata import CalibrationData
from app.database.database import engine  # Assuming you have an engine defined

class TestStorageVerification(unittest.TestCase):
    def setUp(self):
        # Create a new session
        Session = sessionmaker(bind=engine)
        self.session = Session()

        # Example data (simplified for demonstration)
        self.test_matrix = [[1000, 0, 640], [0, 1000, 360], [0, 0, 1]]  # A simple camera matrix
        self.test_distortion = [0.1, -0.01, 0, 0, 0]  # Simplified distortion coefficients

        # Create a new CalibrationData instance
        self.calibration_data = CalibrationData(matrix=self.test_matrix, distortion=self.test_distortion)

        # Add to the session and commit to the database
        self.session.add(self.calibration_data)
        self.session.commit()

    def tearDown(self):
        # Close the session
        self.session.close()

    def test_data_integrity(self):
        # Retrieve the data
        retrieved_data = self.session.query(CalibrationData).first()

        # Verify the data integrity
        self.assertEqual(retrieved_data.matrix, self.test_matrix, "Matrix data integrity check failed")
        self.assertEqual(retrieved_data.distortion, self.test_distortion, "Distortion data integrity check failed")

if __name__ == '__main__':
    unittest.main()
