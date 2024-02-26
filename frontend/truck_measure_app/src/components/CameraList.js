import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Typography, Box, CircularProgress, Select, MenuItem } from '@mui/material';

/**
 * Renders a list of cameras and allows the user to select a camera.
 *
 * @param {Object} props - The component props.
 * @param {Function} props.onSelectCamera - The function to be called when a camera is selected.
 * @returns {JSX.Element} The rendered component.
 */
const CameraList = ({ onSelectCamera }) => {
  const [cameras, setCameras] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCameras = async () => {
      setLoading(true);
      try {
        const response = await axios.get('http://localhost:8000/api/v1/camera');
        setCameras(response.data);  
        setError(null);
      } catch (err) {
        setError('Failed to fetch cameras');
        setCameras([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCameras();
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Box sx={{ minWidth: 120, maxWidth: 300, marginBottom: 2 }}>
      <Typography variant="h6" sx={{ marginBottom: 1 }}></Typography>
      <Select
        fullWidth
        displayEmpty
        onChange={(e) => onSelectCamera(e.target.value)}
        defaultValue=""
        sx={{
          height: 36,
          '& .MuiSelect-select': {
            paddingTop: '8px',
            paddingBottom: '8px',
            color: '#fff', 
          },
          '& .MuiOutlinedInput-notchedOutline': {
            borderColor: 'rgba(255, 255, 255, 0.23)',
          },
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: 'rgba(255, 255, 255, 0.87)', 
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: '#1E88E5', 
          },
        }}
      >
        <MenuItem disabled value="" sx={{ color: '#fff' }}>
          <em>Select a camera</em>
        </MenuItem>
        {cameras.map((camera) => (
          <MenuItem key={camera.id} value={camera.id}>
            {camera.camera_name}
          </MenuItem>
        ))}
      </Select>
    </Box>
  );
};

export default CameraList;
