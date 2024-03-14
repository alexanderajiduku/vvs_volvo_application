import pytest
from unittest.mock import MagicMock, patch
import numpy as np
from  app.services.calibration_service import CameraCalibrationService

class TestCameraCalibrationService:
    """
    Unit tests for the CameraCalibrationService class.
    """

    @pytest.fixture
    def setup(self):
        with patch('camera_calibration_service.Session') as MockSession:
            db = MockSession()
            camera_id = 1
            calibration_service = CameraCalibrationService(db, camera_id)
            yield db, calibration_service

    def test_fetch_checkerboard_dims(self, setup):
        db, calibration_service = setup
        db.query.return_value.filter.return_value.first.return_value = MagicMock(checkerboard_height=9, checkerboard_width=6)
        dims = calibration_service.fetch_checkerboard_dims()
        assert dims == (9, 6)

    def test_fetch_image_paths(self, setup):
        db, calibration_service = setup
        mock_response = [MagicMock(path='path/to/image1.jpg'), MagicMock(path='path/to/image2.jpg')]
        db.query.return_value.all.return_value = mock_response
        paths = calibration_service.fetch_image_paths()
        assert paths == ['path/to/image1.jpg', 'path/to/image2.jpg']

    @patch('camera_calibration_service.load_images')
    @patch('camera_calibration_service.cv2.cvtColor')
    @patch('camera_calibration_service.cv2.findChessboardCorners')
    @patch('camera_calibration_service.cv2.cornerSubPix')
    def test_find_checkerboard_corners(self, mock_subpix, mock_find_corners, mock_cvt_color, mock_load_images, setup):
        db, calibration_service = setup
        mock_load_images.return_value = [MagicMock(), MagicMock()]
        mock_cvt_color.return_value = MagicMock()
        mock_find_corners.return_value = (True, np.array([[1, 2], [3, 4]]))
        mock_subpix.return_value = np.array([[1, 2], [3, 4]])

        objpoints, imgpoints = calibration_service.find_checkerboard_corners(mock_load_images.return_value)

        assert len(objpoints) > 0
        assert len(imgpoints) > 0

    @patch('camera_calibration_service.cv2.calibrateCamera')
    def test_calibrate_camera(self, mock_calibrate_camera, setup):
        db, calibration_service = setup
        mock_calibrate_camera.return_value = (0.5, np.array([[1, 2, 3], [4, 5, 6]]), np.array([0.1, 0.2]), [], [])

        params = calibration_service.calibrate_camera([], [], (640, 480))

        assert "ret" in params
        assert "mtx" in params
        assert "dist" in params
        assert "rvecs" in params
        assert "tvecs" in params

    @patch('camera_calibration_service.CalibrationData')
    def test_save_calibration_parameters(self, MockCalibrationData, setup):
        db, calibration_service = setup
        mock_instance = MockCalibrationData.return_value

        params = {"mtx": np.array([[1, 2, 3], [4, 5, 6]]), "dist": np.array([0.1, 0.2]), "rvecs": [], "tvecs": []}
        result = calibration_service.save_calibration_parameters(params)

        db.add.assert_called_with(mock_instance)
        db.commit.assert_called_once()
        db.refresh.assert_called_with(mock_instance)
