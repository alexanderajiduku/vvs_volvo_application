import React, { useState } from 'react';
import Button from '@mui/material/Button';
import axios from 'axios';
import { BASE_URL } from '../config/config';
import ModelSelection from './ModelSelection';
import WebSocketVideoFeed from './WebSocketVideoFeed'; // Import WebSocket component

const VideoUploadAndProcess = ({ onUploadSuccess }) => { // Pass onUploadSuccess function as a prop
    const [selectedFile, setSelectedFile] = useState(null);
    const [modelId, setModelId] = useState('');

    const handleModelChange = (modelId) => {
        setModelId(modelId);
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file && file.type === "video/mp4") {
            setSelectedFile(file);
        } else {
            alert("Please select an MP4 video file.");
        }
    };

    const handleUpload = async () => {
        if (selectedFile && modelId) {
            const formData = new FormData();
            formData.append('file', selectedFile);

            try {
                const response = await axios.post(`${BASE_URL}/api/v1/process-truck-measure/${modelId}`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });

                if (response.data) {
                    console.log(response.data.message);
                    onUploadSuccess(modelId); // Trigger WebSocket initialization upon successful upload
                }
            } catch (error) {
                console.error('Error uploading file:', error);
            }
        } else {
            alert("Please select a model and a video file.");
        }
    };

    return (
        <div>
            <ModelSelection onModelSelected={handleModelChange} />
            <Button variant="contained" component="label" sx={{ marginTop: 2 }}>
                Select Video
                <input type="file" hidden onChange={handleFileChange} accept="video/mp4" />
            </Button>
            <Button variant="contained" color="primary" onClick={handleUpload} disabled={!selectedFile || !modelId} sx={{ marginTop: 2, marginLeft: 2 }}>
                Upload Video
            </Button>
        </div>
    );
};

export default VideoUploadAndProcess;
