import React, { useState, useEffect } from 'react';
import { CircularProgress, Typography, Box } from '@mui/material';
import socket from '../socket';

const WebSocketVideoFeed = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [vehicleHeights, setVehicleHeights] = useState({});

  useEffect(() => {

    socket.on('connect', () => {
      console.log('Connected to the server');
      setIsLoading(false);
    });

    socket.on('vehicle_data', (data) => {
      console.log('Received vehicle data:', data);
      setVehicleHeights(prevHeights => ({ ...prevHeights, [data.vehicle_id]: data.height }));
    });

    socket.on('error', (error) => {
      console.error('WebSocket connection error:', error);
      setIsError(true);
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from the server');
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (isError) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <Typography variant="body1" color="error" align="center">
          Error loading vehicle data. Please try again later.
        </Typography>
      </Box>
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
