// import React, { useEffect, useState, useRef } from 'react';
// import Card from '@mui/material/Card';
// import CardContent from '@mui/material/CardContent';
// import Typography from '@mui/material/Typography';

// const MeasurementDisplay = () => {
//   const [latestMeasurement, setLatestMeasurement] = useState('');
//   const ws = useRef(null);

//   useEffect(() => {
//     const connectWebSocket = () => {
//       ws.current = new WebSocket('ws://localhost:8000/ws');

//       ws.current.onopen = () => {
//         console.log('WebSocket Connected');
//       };

//       ws.current.onmessage = (event) => {
//         try {
//           const data = JSON.parse(event.data);
//           setLatestMeasurement(data.height);
//           console.log('Parsed height:', data.height);
//         } catch (error) {
//           console.error('Error parsing JSON:', error);
//         }
//       };

//       ws.current.onclose = (event) => {
//         console.log('WebSocket disconnected', event.reason);
//         if (!event.wasClean) {
//           console.log('Attempting to reconnect WebSocket...');
//           setTimeout(connectWebSocket, 2000);
//         }
//       };

//       ws.current.onerror = (error) => {
//         console.error('WebSocket Error', error);
//         ws.current.close(); 
//       };
//     };

//     connectWebSocket();

//     return () => {
//       ws.current.close();
//     };
//   }, []);

//   return (
//     <Card sx={{ maxWidth: 345, margin: 'auto', marginTop: 5 }}>
//       <CardContent>
//         <Typography gutterBottom variant="h5" component="div">
//           Latest Measurement
//         </Typography>
//         <Typography variant="h1" component="p" sx={{ fontWeight: 'bold' }}>
//           {latestMeasurement || 'Waiting for data...'}
//         </Typography>
//       </CardContent>
//     </Card>
//   );
// };

// export default MeasurementDisplay;


import React, { useEffect, useState, useRef } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

const MeasurementDisplay = () => {
  const [latestMeasurement, setLatestMeasurement] = useState(null);
  const ws = useRef(null);

  useEffect(() => {
    const connectWebSocket = () => {
      ws.current = new WebSocket('ws://localhost:8000/ws');

      ws.current.onopen = () => console.log('WebSocket Connected');

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('Parsed height:', data.height); 
          setLatestMeasurement(data.height); 
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
      }
    };
  }, []);

  return (
    <Card sx={{ maxWidth: 345, margin: 'auto', marginTop: 5 }}>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          Latest Measurement
        </Typography>
        <Typography variant="h1" component="p" sx={{ fontWeight: 'bold' }}>
          {latestMeasurement !== null ? `Height: ${latestMeasurement}` : 'Waiting for data...'}
        </Typography>
        <button onClick={() => setLatestMeasurement('Test Height')}>Set Test Height</button>
      </CardContent>
    </Card>
  );
};

export default MeasurementDisplay;






