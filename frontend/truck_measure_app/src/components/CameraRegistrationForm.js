import React, { useState } from 'react';
import { TextField, Button, Grid, Typography, Container, Box } from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';
import axios from 'axios';
import CustomTooltip from '../common/CustomToolTip';

/**
 * Represents a form for registering a camera.
 * @returns {JSX.Element} The camera registration form component.
 */
const CameraRegistrationForm = () => {
    const [cameraName, setCameraName] = useState('');
    const [cameraModel, setCameraModel] = useState('');
    const [checkerboardWidth, setCheckerboardWidth] = useState('');
    const [checkerboardHeight, setCheckerboardHeight] = useState('');
    const [description, setDescription] = useState('');
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');

    const handleCloseSnackbar = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setOpenSnackbar(false);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        const data = {
            camera_name: cameraName,
            camera_model: cameraModel,
            checkerboard_width: checkerboardWidth,
            checkerboard_height: checkerboardHeight,
            description: description
        };
    
        try {
            await axios.post(`${BASE_URL}/api/v1/registercamera`, data, {
                headers: { 'Content-Type': 'application/json' }
            });
            setCameraName('');
            setCameraModel('');
            setCheckerboardWidth('');
            setCheckerboardHeight('');
            setDescription('');
            setSnackbarMessage('Camera registered successfully!');
            setOpenSnackbar(true);
        } catch (error) {
            console.error("Error registering camera:", error.response ? error.response.data : error);
            setSnackbarMessage('Failed to register camera. Please try again.');
            setOpenSnackbar(true);
        }
    };

    return (
        <Container maxWidth="sm">
            <Box sx={{ 
                p: 3, 
                bgcolor: '#121212', // Dark background
                color: '#fff', // White text color
                borderRadius: '4px', 
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)', 
                mt: 4, mb: 4 
            }}>
                <Typography variant="h6" gutterBottom align="center" sx={{ color: '#fff' }}>
                    Register Camera
                    <CustomTooltip title="Add the Checkerboard Calibration height and width for calib  " placement="right" color="#fff" />
                </Typography>
                <form onSubmit={handleSubmit}>
                    <Grid container spacing={3}>
                        {['Camera Name', 'Camera Model', 'Checkerboard Width', 'Checkerboard Height', 'Description'].map((field, index) => (
                            <Grid item xs={index < 4 ? 6 : 12} key={field}>
                                <TextField
                                    fullWidth
                                    label={field}
                                    variant="outlined"
                                    type={index >= 2 && index < 4 ? "number" : "text"}
                                    value={[cameraName, cameraModel, checkerboardWidth, checkerboardHeight, description][index]}
                                    onChange={(e) => [setCameraName, setCameraModel, setCheckerboardWidth, setCheckerboardHeight, setDescription][index](e.target.value)}
                                    InputLabelProps={{
                                        style: { color: '#fff' },
                                    }}
                                    InputProps={{
                                        style: { color: '#fff' },
                                        sx: {
                                            '& .MuiOutlinedInput-notchedOutline': {
                                                borderColor: 'rgba(255, 255, 255, 0.23)', // Light border color
                                            },
                                            '&:hover .MuiOutlinedInput-notchedOutline': {
                                                borderColor: 'rgba(255, 255, 255, 0.87)', // Lighter border color on hover
                                            },
                                            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                                                borderColor: '#1E88E5', // Blue border color when focused
                                            },
                                        },
                                    }}
                                    multiline={index === 4}
                                    rows={index === 4 ? 4 : 1}
                                />
                            </Grid>
                        ))}

                        <Grid item xs={12}>
                            <Button
                                type="submit"
                                variant="contained"
                                startIcon={<SaveIcon />}
                                sx={{ bgcolor: '#1E88E5', '&:hover': { bgcolor: '#1565C0' }, color: '#fff' }}
                            >
                                Register Camera
                            </Button>
                        </Grid>
                    </Grid>
                </form>
            </Box>
        </Container>
    );
};

export default CameraRegistrationForm;
