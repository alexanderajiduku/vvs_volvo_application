// import React, { useEffect, useRef, useState } from 'react';
// import { CircularProgress, Typography, Box } from '@mui/material';

// const VideoFeed = ({ isActive, modelId }) => {
//   const [isLoading, setIsLoading] = useState(true);
//   const [isError, setIsError] = useState(false);
//   const canvasRef = useRef(null);

//   useEffect(() => {
//     if (!isActive || !modelId) {
//       setIsLoading(false);
//       return;
//     }

//     // Construct WebSocket URL
//     const wsBaseUrl = process.env.NODE_ENV === 'development'
//       ? `ws://${window.location.hostname}:8000`
//       : `wss://${window.location.hostname}`;
//     const wsUrl = `${wsBaseUrl}/ws/stream-processed-video/${modelId}`;

//     const ws = new WebSocket(wsUrl);

//     ws.onopen = () => {
//       console.log('WebSocket Connected');
//       setIsLoading(false);
//     };

//     ws.onmessage = (event) => {
//       const data = event.data;
//       if (data instanceof Blob) {
//         const url = URL.createObjectURL(data);
//         const image = new Image();
//         image.onload = () => {
//           if (canvasRef.current) {
//             const ctx = canvasRef.current.getContext('2d');
//             ctx.drawImage(image, 0, 0, canvasRef.current.width, canvasRef.current.height);
//           }
//           URL.revokeObjectURL(url); // Clean up
//         };
//         image.src = url;
//       }
//     };

//     ws.onerror = (error) => {
//       console.error('WebSocket Error:', error);
//       setIsError(true);
//       setIsLoading(false);
//     };

//     ws.onclose = () => {
//       console.log('WebSocket Disconnected');
//       setIsLoading(false);
//     };

//     return () => {
//       ws.close();
//     };
//   }, [isActive, modelId]);

//   if (isLoading) {
//     return <Box display="flex" justifyContent="center" alignItems="center"><CircularProgress /></Box>;
//   }

//   if (isError) {
//     return <Typography variant="body1" color="error" align="center">Error loading video feed. Please try again later.</Typography>;
//   }

//   return (
//     <Box>
//       <Typography variant="h5" gutterBottom align="center">Live Video Feed</Typography>
//       <canvas ref={canvasRef} width="640" height="480" style={{ width: '75%' }}></canvas>
//     </Box>
//   );
// };

// export default VideoFeed;
