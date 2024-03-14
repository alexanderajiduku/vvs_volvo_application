import React, { useEffect, useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

const MeasurementDisplay = () => {
  const [latestMeasurement, setLatestMeasurement] = useState('');
  const connectWebSocket = () => {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onopen = () => {
      console.log('WebSocket Connected');
    };

    ws.onmessage = (event) => {
      const message = event.data;
      console.log('Message from server:', message);
      setLatestMeasurement(message);
    };

    ws.onclose = (event) => {
      console.log('WebSocket disconnected', event.reason);
      if (!event.wasClean) {
        setTimeout(() => {
          console.log('Reconnecting WebSocket');
          connectWebSocket();
        }, 3000);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket Error', error);
    };
    return () => {
      ws.close();
    };
  };

  useEffect(() => {
    const cleanup = connectWebSocket();
    return cleanup;
  }, []);

  return (
    <Card sx={{ maxWidth: 345, margin: 'auto', marginTop: 5 }}>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          Latest Measurement
        </Typography>
        <Typography variant="h1" component="p" sx={{ fontWeight: 'bold' }}>
          {latestMeasurement}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default MeasurementDisplay;