import React, { useEffect, useState, useRef } from 'react';
import { Card, Typography, CardContent } from '@mui/material';


const MeasurementDisplay = () => {
  const [latestMeasurement, setLatestMeasurement] = useState(null);
  const ws = useRef(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;
  const latestMeasurementRef = useRef(latestMeasurement);

  useEffect(() => {
    const connectWebSocket = () => {
      if (reconnectAttempts.current >= maxReconnectAttempts) {
        console.log('Max reconnect attempts reached, not trying further.');
        return;
      }
      ws.current = new WebSocket('ws://localhost:8000/ws');
      ws.current.onopen = () => console.log('WebSocket Connected');
      reconnectAttempts.current = 0;
      // ws.current.onmessage = (event) => {
      //   console.log('Raw data:', event.data);
      //   try {
      //     const data = JSON.parse(event.data);
      //     if (data.hasOwnProperty('height')) {
      //       console.log('Parsed height:', data.height);
      //       setLatestMeasurement(data.height);
      //     } else {
      //       console.log('Non-height message received:', data.type);
      //     }
      //   } catch (error) {
      //     console.error('Error parsing JSON:', error);
      //   }
      // };

      ws.current.onmessage = (event) => {
        console.log('Raw data:', event.data);
        try {
            const data = JSON.parse(event.data);
            if (typeof data === 'object' && data !== null && 'height' in data) {
                console.log('Parsed height:', data.height);
                if (latestMeasurementRef.current !== data.height && (typeof data.height === 'number' || latestMeasurementRef.current === null)) {
                    setLatestMeasurement(data.height);
                    latestMeasurementRef.current = data.height;
                }
            } else {
                console.log('Message received without a height property or not in expected format:', data);
            }
        } catch (error) {
            console.error('Error parsing JSON:', error);
        }
    };
      

      ws.current.onclose = (event) => {
        console.log('WebSocket disconnected', event.reason);
        if (!event.wasClean && reconnectAttempts.current < maxReconnectAttempts) {
          setTimeout(connectWebSocket, 2000);
          reconnectAttempts.current++;
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
        maxWidth: 1000, 
        height: 1000, 
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
          fontSize: '25rem',
        }}>
        {latestMeasurement !== null ? `${latestMeasurement}` : '...'}
      </Typography>
    </Card>
  );
};

export default MeasurementDisplay;