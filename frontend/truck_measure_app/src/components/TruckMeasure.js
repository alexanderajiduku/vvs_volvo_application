import React, { useState } from 'react';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import VideoUploadAndProcess from './VideoUploadAndProcess';
import MeasurementsDisplay from './MeasurementDisplay';
import VideoStream from './VideoFeed';

const TruckMeasure = () => {
    const [isActive, setIsActive] = useState(false);
    const [modelId, setModelId] = useState('');

    const onVideoProcessingStart = (selectedModelId) => {
        setModelId(selectedModelId);
        setIsActive(true);
    };

    return (
        <Container maxWidth="lg">
            <Typography variant="h4" component="h4" gutterBottom sx={{ textAlign: 'center', color: '#fff' }}>
                TruckMeasure Inference
            </Typography>
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <VideoUploadAndProcess onUploadSuccess={onVideoProcessingStart} />
                </Grid>
                <Grid item xs={12}>
                    <MeasurementsDisplay isActive={isActive} />
                </Grid>
                <Grid item xs={12}>
                    <VideoStream /> 
                </Grid>
            </Grid>
        </Container>
    );
};

export default TruckMeasure;
