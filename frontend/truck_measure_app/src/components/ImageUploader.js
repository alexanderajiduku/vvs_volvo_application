import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Button, Typography, LinearProgress, Box, FormControl, Paper, useTheme } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import SaveIcon from '@mui/icons-material/Save';
import CameraList from './CameraList';
import CustomTooltip from '../common/CustomToolTip';

/**
 * Component for uploading images.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {Function} props.onUploadSuccess - Callback function to be called when the image upload is successful.
 * @returns {JSX.Element} The ImageUploader component.
 */
const ImageUploader = ({ onUploadSuccess }) => {
    const theme = useTheme();
    const [selectedCameraId, setSelectedCameraId] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [error, setError] = useState('');
    const fileInputRef = useRef(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
        setError('');
    };

    const handleCameraSelect = (camera_id) => {
        setSelectedCameraId(camera_id);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError('No file selected');
            return;
        }
    
        if (!selectedCameraId) {
            setError('No camera selected');
            return;
        }
    
        const formData = new FormData();
        formData.append('file', selectedFile);
    
        const uploadUrl = `http://localhost:8000/api/v1/uploadimages/${selectedCameraId}`;
    
        try {
            await axios.post(uploadUrl, formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setUploadProgress(percentCompleted);
                },
            });
            console.log('Image uploaded successfully');
            setSelectedFile(null);
            setSelectedCameraId(null);
            setUploadProgress(0);
            fileInputRef.current.value = null; // Reset file input
            if (onUploadSuccess) onUploadSuccess();
        } catch (error) {
            setError(`Error uploading image: ${error.message}`);
            setUploadProgress(0);
        }
    };
    return (
        <Paper elevation={3} sx={{ p: theme.spacing(3), mt: theme.spacing(3), bgcolor: '#121212', color: '#fff' }}>
            <Typography variant="h6" gutterBottom sx={{ textAlign: 'center', mb: theme.spacing(2) }}>
                Upload Image
                <CustomTooltip title="Upload only Checkered box images with the selected height and width " placement="right" color="#fff" />
            </Typography>
            <CameraList onSelectCamera={handleCameraSelect} />
            <FormControl fullWidth margin="normal">
                <Button
                    variant="outlined"
                    component="label"
                    htmlFor="image-upload-input"
                    sx={{
                        mt: theme.spacing(1),
                        borderColor: 'rgba(255, 255, 255, 0.23)',
                        color: '#fff',
                        '&:hover': {
                            borderColor: '#1E88E5',
                            backgroundColor: 'rgba(255, 255, 255, 0.08)',
                        },
                        '& .MuiButton-startIcon': {
                            color: 'inherit',
                        },
                    }}
                >
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
                    startIcon={<SaveIcon />}
                    onClick={handleUpload}
                    sx={{ bgcolor: '#1E88E5', '&:hover': { bgcolor: '#1565C0' }, color: '#fff' }}
                >
                    Upload
                </Button>
                {uploadProgress > 0 && (
                    <Box sx={{ width: '100%', ml: theme.spacing(2) }}>
                        <LinearProgress variant="determinate" value={uploadProgress} />
                    </Box>
                )}
            </Box>
            {error && <Typography color="error" sx={{ mt: theme.spacing(2) }}>{error}</Typography>}
        </Paper>
    );
};

export default ImageUploader;
