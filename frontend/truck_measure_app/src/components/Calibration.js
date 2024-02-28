import React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import ImageUploader from './ImageUploader';
import CameraRegistrationForm from './CameraRegistrationForm';
import CalibrationProcess from './CalibrationProcess';
import CameraTable from './CameraTable';

const theme = createTheme();

const Calibration = () => {
    const handleCalibrationSuccess = () => {
        console.log('Calibration was successful');
        // Here you can add any logic you want to execute after successful calibration
        // For example, you might want to refresh a list of cameras, or show a success message
    };

    return (
        <ThemeProvider theme={theme}>
            <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
                <Grid container spacing={5} justifyContent="space-between">
                    <Grid item xs={12} md={5}>
                        <CameraRegistrationForm />
                    </Grid>
                    <Grid item xs={12} md={3.5}>
                        <Typography variant="h6" gutterBottom sx={{ textAlign: 'center' }}>
                        </Typography>
                        <ImageUploader onUploadSuccess={() => console.log()} />
                    </Grid>
                    <Grid item xs={12} md={3.5}> 
                        <Typography variant="h6" gutterBottom sx={{ textAlign: 'center' }}>
                        </Typography>
                        <CalibrationProcess onCalibrationSuccess={handleCalibrationSuccess} />
                    </Grid>
                    <Grid item xs={12}>
                        <CameraTable />
                    </Grid>
                </Grid>
            </Container>
        </ThemeProvider>
    );
};

export default Calibration;
