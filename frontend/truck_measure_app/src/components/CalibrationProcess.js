import React, { useState } from 'react';
import { Button, Box, CircularProgress, Snackbar, Alert, Typography, useTheme} from '@mui/material';
import axios from 'axios';
import CameraList from './CameraList';  
import CustomTooltip from '../common/CustomToolTip';

/**
 * Represents a component for camera calibration.
 * @param {Object} props - The component props.
 * @param {Function} props.onCalibrationSuccess - The callback function to be called on calibration success.
 * @returns {JSX.Element} The CalibrationProcess component.
 */
const CalibrationProcess = ({ onCalibrationSuccess }) => {
    const theme = useTheme();
    const [selectedCameraId, setSelectedCameraId] = useState(null);
    const [calibrating, setCalibrating] = useState(false);
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [calibrationSuccess, setCalibrationSuccess] = useState(false);

    const handleCameraSelect = (cameraId) => {
        setSelectedCameraId(cameraId);
    };

    const handleCalibration = async () => {
        setCalibrating(true);
        if (!selectedCameraId) {
            console.error('Camera ID is required to start calibration');
            setCalibrating(false);
            return;
        }

        try {
            const url = `http://localhost:8000/api/v1/calibration/${selectedCameraId}`;
            const response = await axios.post(url);
            setOpenSnackbar(true);
            setCalibrationSuccess(true);
            if (onCalibrationSuccess) onCalibrationSuccess();
        } catch (error) {
            console.error('Calibration error:', error);
        } finally {
            setCalibrating(false);
        }
    };

    const handleCloseSnackbar = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setOpenSnackbar(false);
    };

    return (
        <Box sx={{
            p: 3,
            bgcolor: '#121212', 
            color: '#fff', 
            borderRadius: '4px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            mt: 4,
            mb: 4
        }}>
          <Typography variant="h6" gutterBottom sx={{ textAlign: 'center', mb: theme.spacing(2) }}>
                Camera Calibration
                <CustomTooltip title="Creates a Camera Calibration matrix for distortion correction" placement="right" color="#fff" />
            </Typography>
            {calibrationSuccess ? (
                <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleCloseSnackbar}>
                    <Alert onClose={handleCloseSnackbar} severity="success" sx={{ width: '100%' }}>
                        Calibration completed successfully!
                    </Alert>
                </Snackbar>
            ) : (
                <>
                    <CameraList onSelectCamera={handleCameraSelect} />
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={handleCalibration}
                        sx={{
                            mt: 2,
                            bgcolor: '#1E88E5', '&:hover': { bgcolor: '#1565C0' },
                            color: '#fff',
                            ...(calibrating && {
                                bgcolor: 'rgba(255, 255, 255, 0.12)', 
                                color: 'rgba(255, 255, 255, 0.7)',
                            })
                        }}
                        startIcon={calibrating ? <CircularProgress size={24} color="inherit" /> : null}
                        disabled={calibrating}
                    >
                        {calibrating ? 'Calibrating...' : 'Start Calibration'}
                    </Button>
                </>
            )}
        </Box>
    );
};

export default CalibrationProcess;
