import React, { useState, useEffect, useRef } from 'react';
import { CircularProgress, Typography, Box, Paper } from '@mui/material';

const VideoStream = () => {
  const [imageSrc, setImageSrc] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(false); 
  const reconnectAttempts = useRef(0);
  const reconnectDelay = useRef(1000); 

  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket(`ws://localhost:8000/ws/video`);

      ws.onopen = () => {
        setIsLoading(true);
        setError(false); 
        reconnectAttempts.current = 0;
        reconnectDelay.current = 1000; 
      };

      ws.onmessage = (event) => {
        const blob = new Blob([event.data], { type: 'image/jpeg' });
        const url = URL.createObjectURL(blob);
        setImageSrc((prevSrc) => {
          URL.revokeObjectURL(prevSrc); 
          return url; 
        });
        setIsLoading(false);
      };

      ws.onerror = () => {
        setIsLoading(false);
        setError(true);
        ws.close();
      };

      ws.onclose = () => {
        if (!error) { 
          setTimeout(connectWebSocket, reconnectDelay.current);
          reconnectAttempts.current++;
          reconnectDelay.current *= 2; 
        }
      };

      return () => {
        ws.close();
      };
    };

    const cleanup = connectWebSocket();
    return cleanup;
  }, [error]); 

  return (
    <Box display="flex" flexDirection="column" alignItems="center" p={2}>
      {isLoading ? (
        <Box display="flex" flexDirection="column" alignItems="center">
          <CircularProgress />
          <Typography variant="subtitle1" mt={2}>
            {error ? "Error loading video stream. Attempting to reconnect..." : "Loading video stream..."}
          </Typography>
        </Box>
      ) : imageSrc && !error ? (
        <Paper elevation={4}>
          <img
            id="frame"
            src={imageSrc}
            alt="Live Stream"
            style={{ maxWidth: '100%', maxHeight: '90vh' }}
          />
        </Paper>
      ) : (
        <Typography variant="subtitle1">
          Unable to load video stream.
        </Typography>
      )}
    </Box>
  );
};

export default VideoStream;
