import React, { useState, useEffect } from 'react';
import { CircularProgress, Typography, Box } from '@mui/material';
import { io } from 'socket.io-client';

const WebSocketVideoFeed = ({ isActive, modelId, videoId, onConnectionEstablished }) => {
    const [isLoading, setIsLoading] = useState(true);
    const [isError, setIsError] = useState(false);
    const [vehicleHeights, setVehicleHeights] = useState({});

    useEffect(() => {
        if (!isActive || !modelId || !videoId) {
            console.error('WebSocket is not active, modelId, or videoId is missing.');
            setIsLoading(false);
            setIsError(true);
            return;
        }

        const socket = io('http://localhost:8000', {
            path: '/ws/socket.io',
            transports: ['websocket'],
        });

        socket.on("connect", () => {
            console.log("Connected to the server.");
            setIsLoading(true);
            onConnectionEstablished(); // Call the callback to indicate the connection is established
        });

        socket.on("height_data", (data) => {
            setVehicleHeights(prevHeights => ({ ...prevHeights, [data.vehicle_id]: data.height }));
        });

        socket.on("process_completed", () => {
            setIsLoading(false);
            console.log("Process completed.");
        });

        socket.on("connect_error", (error) => {
            console.error('Socket.IO error:', error);
            setIsError(true);
            setIsLoading(false);
        });

        return () => {
            socket.disconnect();
        };
    }, [isActive, modelId, videoId, onConnectionEstablished]); // Added onConnectionEstablished to the dependency array

    if (isLoading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center">
                <CircularProgress />
            </Box>
        );
    }

    if (isError) {
        return (
            <Typography variant="body1" color="error" align="center">
                Error loading vehicle data. Please try again later.
            </Typography>
        );
    }

    return (
        <Box>
            <Typography variant="h5" gutterBottom align="center">
                Vehicle Heights
            </Typography>
            {Object.entries(vehicleHeights).map(([id, height]) => (
                <Typography key={id} variant="body2" align="center">
                    Vehicle {id}: Height - {height} units
                </Typography>
            ))}
        </Box>
    );
};

export default WebSocketVideoFeed;
