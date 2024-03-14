import React, { useState, useEffect, useRef } from 'react';
import { BASE_URL } from '../config/config'; // Your WebSocket base URL (if different from HTTP API)
import { CircularProgress, Typography, Box } from '@mui/material';

const VideoFeed = ({ isActive, modelId }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const imageRef = useRef(null);

  useEffect(() => {
    if (!isActive || !modelId) {
      return;
    }

    let ws;

    const connectWebSocket = () => {
      ws = new WebSocket(`${BASE_URL.replace("http", "ws")}/ws?modelId=${modelId}`);

      ws.onopen = () => {
        console.log('WebSocket Connected');
        setIsLoading(false);
      };

      ws.onmessage = (event) => {
        if (imageRef.current) {
          const blob = new Blob([event.data], { type: 'image/jpeg' });
          imageRef.current.src = URL.createObjectURL(blob);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket Error:', error);
        setIsError(true);
      };

      ws.onclose = () => console.log('WebSocket Disconnected');
    };

    connectWebSocket();

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [isActive, modelId]);

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
        Error loading video feed. Please try again later.
      </Typography>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom align="center">
        Live Video Feed
      </Typography>
      <Box display="flex" justifyContent="center" alignItems="center">
        <img ref={imageRef} alt="Live Video Feed" style={{ width: '100%' }} />
      </Box>
    </Box>
  );
};

export default VideoFeed;
