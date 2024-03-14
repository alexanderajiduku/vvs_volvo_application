import React, { useEffect, useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

const MeasurementDisplay = ({ isActive }) => {
  const [latestMeasurement, setLatestMeasurement] = useState('');

  
  useEffect(() => {
    if (!isActive) return;
    const ws = new WebSocket('ws://localhost:8000/ws');
    ws.onopen = () => {
      console.log('WebSocket Connected');
    };
    ws.onmessage = (event) => {
      console.log('Received message:', event.data);
      setLatestMeasurement(event.data);  
    };
    ws.onclose = (event) => {
      console.log('WebSocket disconnected', event.reason);
      if (!event.wasClean) {
        setTimeout(() => {
          console.log('Reconnecting WebSocket');
        }, 1000);
      }
    };
    ws.onerror = (error) => {
      console.error('WebSocket Error', error);
    };
    return () => {
      ws.close();
    };
  }, [isActive]); 

  return (
    <Card sx={{ maxWidth: 345, margin: 'auto', marginTop: 5 }}>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          Latest Measurement
        </Typography>
        <Typography variant="h1" component="p" sx={{ fontWeight: 'bold' }}>
          {latestMeasurement || 'Waiting for data...'} 
        </Typography>
      </CardContent>
    </Card>
  );
};

export default MeasurementDisplay;
