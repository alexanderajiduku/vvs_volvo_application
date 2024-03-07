import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Button, Typography, LinearProgress, Box, FormControl, Paper, useTheme, Snackbar, Alert, CircularProgress } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CustomTooltip from '../common/CustomToolTip';
import { BASE_URL } from '../config/config';

/**
 * UltralyticsFileUpload component for uploading image or video files and making API requests.
 * @param {Object} props - The component props.
 * @param {string} props.selectedModelId - The ID of the selected model.
 * @param {Function} props.onUploadSuccess - Callback function triggered on successful upload.
 * @returns {JSX.Element} - The UltralyticsFileUpload component.
 */
const UltralyticsFileUpload = ({ selectedModelId, onUploadSuccess }) => {
    const theme = useTheme();
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const fileInputRef = useRef(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        console.log('File selected:', file); 
        if (file && ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml', 'video/mp4'].includes(file.type.toLowerCase())) {
            setSelectedFile(file);
            setError('');
        } else {
            setError('Unsupported file type. Please select a JPG image or MP4 video.');
        }
    };
 
    const handleUpload = async () => {
        setError('');
        if (!selectedFile || !selectedModelId) {
          setError('No file selected or model not chosen');
          return;
        }
    
        const formData = new FormData();
        formData.append('file', selectedFile);  
    
        const uploadUrl = `${BASE_URL}/api/v1/inference/${selectedModelId}`;

        try {
            const response = await axios.post(uploadUrl, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                onUploadProgress: progressEvent => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setUploadProgress(percentCompleted);
                }
            });
            setSuccessMessage('File uploaded successfully!');
            setSelectedFile(null);
            setUploadProgress(0);
            fileInputRef.current.value = '';  
    
         
            if (onUploadSuccess) onUploadSuccess(response.data.annotated_file_key, selectedFile.type);
        } catch (error) {
            console.error('Error uploading file:', error);
            setError(`Error uploading file: ${error.response ? error.response.data.detail : error.message}`);
            setUploadProgress(0);
        }
    };
    

    const handleCloseSnackbar = () => {
        setSuccessMessage('');
    };

    return (
        <Box sx={{ display: 'flex', justifyContent: 'center' }}>
            <Paper elevation={3} sx={{ p: theme.spacing(3), bgcolor: '#121212', color: '#fff', maxWidth: '500px', width: '100%' }}>
                <Typography variant="h6" gutterBottom sx={{ textAlign: 'center', mb: theme.spacing(2) }}>
                    Upload Image or Video
                    <CustomTooltip title="Upload images of your choice to get inferences from models" placement="right" color="#fff" />
                </Typography>
                <FormControl fullWidth margin="normal">
                    <Button
                        variant="outlined"
                        component="label"
                        sx={{
                            mt: theme.spacing(1),
                            borderColor: 'rgba(255, 255, 255, 0.23)',
                            color: '#fff',
                            '&:hover': {
                                borderColor: '#1E88E5',
                                backgroundColor: 'rgba(255, 255, 255, 0.08)',
                            },
                        }}>
                        Choose File
                        <input id="image-upload-input" type="file" hidden onChange={handleFileChange} ref={fileInputRef} />
                        <CloudUploadIcon />
                    </Button>
                    {selectedFile && <Typography variant="caption" sx={{ display: 'block', mt: theme.spacing(1) }}>{selectedFile.name}</Typography>}
                </FormControl>
                <Box sx={{ mt: theme.spacing(2), display: 'flex', alignItems: 'center' }}>
                    <Button
                        type="submit"
                        variant="contained"
                        sx={{ bgcolor: '#1E88E5', '&:hover': { bgcolor: '#1565C0' }, color: '#fff' }}
                        onClick={handleUpload}
                    >
                        Upload
                        {uploadProgress > 0 && <CircularProgress size={24} sx={{ color: '#fff', position: 'absolute' }} />}
                    </Button>
                    {uploadProgress > 0 && (
                        <Box sx={{ width: '100%', ml: theme.spacing(2) }}>
                            <LinearProgress variant="determinate" value={uploadProgress} />
                        </Box>
                    )}
                </Box>
                {error && <Typography color="error" sx={{ mt: theme.spacing(2), color: '#fff' }}>{error}</Typography>}
                <Snackbar open={!!successMessage} autoHideDuration={6000} onClose={handleCloseSnackbar}>
                    <Alert onClose={handleCloseSnackbar} severity="success" sx={{ width: '100%' }}>
                        {successMessage}
                    </Alert>
                </Snackbar>
            </Paper>
        </Box>
    );
};

export default UltralyticsFileUpload;