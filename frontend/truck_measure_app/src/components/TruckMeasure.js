import React, { useState } from 'react';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import VideoUploadAndProcess from './VideoUploadAndProcess';
import WebSocketVideoFeed from './WebSocketVideoFeed';

const TruckMeasure = () => {
    const [isActive, setIsActive] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [isError, setIsError] = useState(false);
    const [modelId, setModelId] = useState('');
    const [errorMessages, setErrorMessages] = useState([]);

    const onVideoProcessingStart = (selectedModelId) => {
        setModelId(selectedModelId);
        setIsActive(true);
        setIsLoading(true);
        setIsError(false);
        setErrorMessages([]);
    };

    const onVideoProcessingError = (errors) => {
        setIsError(true);
        setErrorMessages(Array.isArray(errors) ? errors : [errors]); // Ensure errors is always an array
        setIsLoading(false);
    };

    const handleConnectionEstablished = () => {
        setIsLoading(false); // Update the isLoading state when the WebSocket connection is established
    };

    return (
        <Container maxWidth="lg">
            <Typography variant="h4" gutterBottom sx={{ textAlign: 'center' }}>
                TruckMeasure Inference
            </Typography>
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <VideoUploadAndProcess 
                        onUploadSuccess={onVideoProcessingStart} 
                        onUploadError={onVideoProcessingError} 
                    />
                </Grid>
                {isLoading && (
                    <Grid item xs={12} display="flex" justifyContent="center">
                        <CircularProgress />
                    </Grid>
                )}
                {isError && errorMessages.map((msg, index) => (
                    <Grid item xs={12} key={index}>
                        <Typography variant="body1" color="error" align="center">{msg}</Typography>
                    </Grid>
                ))}
                {isActive && !isLoading && !isError && (
                    <Grid item xs={12}>
                        <WebSocketVideoFeed 
                            isActive={isActive} 
                            modelId={modelId} 
                            onConnectionEstablished={handleConnectionEstablished} 
                        />
                    </Grid>
                )}
            </Grid>
        </Container>
    );
};

export default TruckMeasure;
