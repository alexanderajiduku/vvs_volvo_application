import React, { useState, useEffect } from 'react';
import AuthApi from '../api/api'; // Assuming this is where you get your auth token
import { BASE_URL } from '../config/config'; // Your API base URL
import { CircularProgress, Typography, Box } from '@mui/material';

const VideoFeed = ({ isActive, modelId, inputSource }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [videoStream, setVideoStream] = useState(null);

  useEffect(() => {
    const fetchVideoStream = async () => {
      if (!modelId || !isActive || !inputSource) {
        return;
      }
      setIsLoading(true);
      setIsError(false); 
      try {
        const authToken = AuthApi.getAuthToken(); 
        const encodedInputSource = encodeURIComponent(inputSource);
        const response = await fetch(`${BASE_URL}/stream-processed-video/${modelId}?input_source=${encodedInputSource}`, {
          headers: {
            'Authorization': `Bearer ${authToken}`
          }
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        setVideoStream(URL.createObjectURL(await response.blob()));
      } catch (error) {
        console.error('Error loading video feed:', error);
        setIsError(true); 
      } finally {
        setIsLoading(false); 
      }
    };

    fetchVideoStream();
  }, [isActive, modelId, inputSource]); 

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
      {videoStream && (
        <video src={videoStream} controls autoPlay style={{ width: '100%' }} alt="Live Video Feed" />
      )}
    </Box>
  );
};

export default VideoFeed;
