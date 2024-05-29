import React, { useRef, useState } from 'react';
import axios from 'axios';
import { Box, Button, TextField, Typography, Snackbar, Alert } from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';
import CustomTooltip from '../common/CustomToolTip';
import { BASE_URL } from '../config/config';

const ModelForm = () => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [modelFile, setModelFile] = useState(null);
  const [error, setError] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [alertSeverity, setAlertSeverity] = useState('error');
  const fileInputRef = useRef(null);

  const handleNameChange = (event) => setName(event.target.value);
  const handleDescriptionChange = (event) => setDescription(event.target.value);
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    const allowedExtensions = ['.pt', '.pkl'];
    const fileExtension = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();
  
    if (!allowedExtensions.includes(fileExtension)) {
      setError(`File type '${fileExtension}' is not allowed. Only ${allowedExtensions.join(', ')} files are accepted.`);
      setOpenSnackbar(true);
      setSnackbarMessage(`File type '${fileExtension}' is not allowed. Only ${allowedExtensions.join(', ')} files are accepted.`);
      setAlertSeverity('error');
      setModelFile(null);
      fileInputRef.current.value = ''; 
    } else {
      setModelFile(file);
      setError('');
    }
  };

  const handleButtonClick = () => fileInputRef.current.click();

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
    setError(''); 
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!modelFile) {
      setError('Please select a file to upload.');
      setOpenSnackbar(true);
      setSnackbarMessage('Please select a file to upload.');
      setAlertSeverity('error');
      return;
    }

    const formData = new FormData();
    formData.append('name', name);
    formData.append('description', description);
    formData.append('file', modelFile);

    try {
      await axios.post(`${BASE_URL}/api/v1/model?name=${encodeURIComponent(name)}&description=${encodeURIComponent(description)}`, formData, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
        },
      });
      setName('');
      setDescription('');
      setModelFile(null);
      fileInputRef.current.value = ''; 
      setOpenSnackbar(true);
      setSnackbarMessage('Model uploaded successfully!');
      setAlertSeverity('success');
    } catch (error) {
      console.error('Error uploading model:', error.response ? error.response.data : error);
      setError(error.response?.data?.detail?.join(', ') || 'An unexpected error occurred during model upload. Please try again.');
      setOpenSnackbar(true);
      setSnackbarMessage(error.response?.data?.detail?.join(', ') || 'An unexpected error occurred during model upload. Please try again.');
      setAlertSeverity('error');
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{ p: 3, bgcolor: '#121212', color: '#fff', display: 'flex', flexDirection: 'column', gap: 2 }}
    >
      <Typography variant="h6" align="center">
        Register Model
        <CustomTooltip title="Upload your custom Model only .pt or .pkl format" />
      </Typography>
      <TextField
        name="name"
        label="Model Name"
        variant="outlined"
        value={name}
        onChange={handleNameChange}
        InputLabelProps={{ style: { color: '#fff' } }}
        InputProps={{ style: { color: '#fff' } }}
      />
      <TextField
        name="description"
        label="Description"
        variant="outlined"
        multiline
        rows={4}
        value={description}
        onChange={handleDescriptionChange}
        InputLabelProps={{ style: { color: '#fff' } }}
        InputProps={{ style: { color: '#fff' } }}
      />
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
      <Button
        type="button"
        onClick={handleButtonClick}
        variant="contained"
        startIcon={<SaveIcon />}
        sx={{ bgcolor: '#1E88E5', '&:hover': { bgcolor: '#1565C0' }, color: '#fff', marginTop: '10px' }}
      >
        Choose File
      </Button>
      <Button
        type="submit"
        variant="contained"
        startIcon={<SaveIcon />}
        sx={{ bgcolor: '#1E88E5', '&:hover': { bgcolor: '#1565C0' }, color: '#fff', marginTop: '10px' }}
      >
        Upload Model
      </Button>
      <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity={alertSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ModelForm;
