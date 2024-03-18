import React, { useEffect, useState, useRef } from 'react';
import { Card, Typography, CardContent } from '@mui/material';


const MeasurementDisplay = () => {
  const [latestMeasurement, setLatestMeasurement] = useState(null);
  const ws = useRef(null);

  useEffect(() => {
    const connectWebSocket = () => {
      ws.current = new WebSocket('ws://localhost:8000/ws');
      ws.current.onopen = () => console.log('WebSocket Connected');
      ws.current.onmessage = (event) => {
        console.log('Raw data:', event.data);
        try {
          const data = JSON.parse(event.data);
          if (data.hasOwnProperty('height')) {
            console.log('Parsed height:', data.height);
            setLatestMeasurement(data.height);
          } else {
            console.log('Non-height message received:', data.type);
          }
        } catch (error) {
          console.error('Error parsing JSON:', error);
        }
      };

      ws.current.onclose = (event) => {
        console.log('WebSocket disconnected', event.reason);
        if (!event.wasClean) {
          console.log('Attempting to reconnect WebSocket...');
          setTimeout(connectWebSocket, 2000);
        }
      };

      ws.current.onerror = (error) => {
        console.error('WebSocket Error', error);
        ws.current.close();
      };
    };

    connectWebSocket();

    return () => {
      if (ws.current) {
        ws.current.close();
        ws.current = null;
      }
    };
  }, []);

  return (
    <Card sx={{ 
        maxWidth: 345, 
        height: 200, 
        margin: 'auto', 
        marginTop: 5, 
        bgcolor: 'black', 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
      }}>
      <Typography 
        variant="h1" 
        component="div" 
        sx={{ 
          color: '#FFFFFF', 
          fontWeight: 'bold',
          textShadow: '2px 2px 8px rgba(0, 0, 0, 0.7)', 
        }}>
        {latestMeasurement !== null ? `${latestMeasurement}` : 'Waiting for data...'}
      </Typography>
    </Card>
  );
};

export default MeasurementDisplay;