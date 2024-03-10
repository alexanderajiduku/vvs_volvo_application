import React, { useState } from 'react';
import { Button, Typography, Paper, Box, Grid } from '@mui/material';
import Detection from './Detection';
import Segmentation from './Segmentation';
import CameraList from './CameraList'; 

/**
 * Renders the AIProcesses component.
 * This component displays AI processes under construction and allows the user to switch between different views.
 *
 * @returns {JSX.Element} The rendered AIProcesses component.
 */
const AIProcesses = () => {
  const [activeView, setActiveView] = useState('classification'); 

  return (
    <Box sx={{ flexGrow: 1, padding: 3 }}>
      <Paper elevation={3} sx={{ padding: 2, marginBottom: 3 }}>
        <Typography variant="h4" gutterBottom component="div" sx={{ textAlign: 'center', color: '#fff' }}>
          AI Processes Under Construction
        </Typography>
        <Grid container spacing={3} alignItems="center" justifyContent="center">
          <Grid item xs={12}>
            <CameraList /> 
          </Grid>
        </Grid>
      </Paper>
      <Grid container spacing={2} justifyContent="center">
        <Grid item>
          <Button variant="contained" onClick={() => setActiveView('classification')}>
            Classification
          </Button>
        </Grid>
        <Grid item>
          <Button variant="contained" onClick={() => setActiveView('detection')}>
            Detection
          </Button>
        </Grid>
        <Grid item>
          <Button variant="contained" onClick={() => setActiveView('segmentation')}>
            Segmentation
          </Button>
        </Grid>
      </Grid>
 
      {activeView === 'detection' && <Detection />}
      {activeView === 'segmentation' && <Segmentation />}
    </Box>
  );
};

export default AIProcesses;
