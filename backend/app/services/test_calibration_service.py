import unittest
from unittest.mock import MagicMock, patch
import numpy as np


from  calibration_service import CameraCalibrationService

class TestCameraCalibrationService(unittest.TestCase):
    """
    Unit tests for the CameraCalibrationService class.
    """

    @patch('camera_calibration_service.Session')
    def setUp(self, MockSession):
        self.db = MockSession()
        self.camera_id = 1
        self.calibration_service = CameraCalibrationService(self.db, self.camera_id)

    def test_fetch_checkerboard_dims(self):
        self.db.query.return_value.filter.return_value.first.return_value = MagicMock(checkerboard_height=9, checkerboard_width=6)
        dims = self.calibration_service.fetch_checkerboard_dims()
        self.assertEqual(dims, (9, 6))

    def test_fetch_image_paths(self):
        mock_response = [MagicMock(path='path/to/image1.jpg'), MagicMock(path='path/to/image2.jpg')]
        self.db.query.return_value.all.return_value = mock_response
        paths = self.calibration_service.fetch_image_paths()
        self.assertEqual(paths, ['path/to/image1.jpg', 'path/to/image2.jpg'])

    @patch('camera_calibration_service.load_images')
    @patch('camera_calibration_service.cv2.cvtColor')
    @patch('camera_calibration_service.cv2.findChessboardCorners')
    @patch('camera_calibration_service.cv2.cornerSubPix')
    def test_find_checkerboard_corners(self, mock_subpix, mock_find_corners, mock_cvt_color, mock_load_images):
        mock_load_images.return_value = [MagicMock(), MagicMock()]
        mock_cvt_color.return_value = MagicMock()
        mock_find_corners.return_value = (True, np.array([[1, 2], [3, 4]]))
        mock_subpix.return_value = np.array([[1, 2], [3, 4]])

        objpoints, imgpoints = self.calibration_service.find_checkerboard_corners(mock_load_images.return_value)

        self.assertTrue(len(objpoints) > 0)
        self.assertTrue(len(imgpoints) > 0)

    @patch('camera_calibration_service.cv2.calibrateCamera')
    def test_calibrate_camera(self, mock_calibrate_camera):
        mock_calibrate_camera.return_value = (0.5, np.array([[1, 2, 3], [4, 5, 6]]), np.array([0.1, 0.2]), [], [])

        params = self.calibration_service.calibrate_camera([], [], (640, 480))

        self.assertIn("ret", params)
        self.assertIn("mtx", params)
        self.assertIn("dist", params)
        self.assertIn("rvecs", params)
        self.assertIn("tvecs", params)

    @patch('camera_calibration_service.CalibrationData')
    def test_save_calibration_parameters(self, MockCalibrationData):
        mock_instance = MockCalibrationData.return_value

        params = {"mtx": np.array([[1, 2, 3], [4, 5, 6]]), "dist": np.array([0.1, 0.2]), "rvecs": [], "tvecs": []}
        result = self.calibration_service.save_calibration_parameters(params)

        self.db.add.assert_called_with(mock_instance)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_with(mock_instance)



if __name__ == '__main__':
    unittest.main()
