import React, { useState, useEffect, useRef } from 'react';
import Button from '@mui/material/Button';
import axios from 'axios';
import { BASE_URL } from '../config/config';
import ModelSelection from './ModelSelection';
import io from "socket.io-client";

const VideoUploadAndProcess = ({ onUploadSuccess }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [modelId, setModelId] = useState('');
    const [heightMeasurements, setHeightMeasurements] = useState([]);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadError, setUploadError] = useState('');
    const socketRef = useRef(null);

    useEffect(() => {
        console.log("Initializing socket connection...");
        socketRef.current = io("http://localhost:8000", {
            path: "/socket.io",
            transports: ["websocket"],
        });

        socketRef.current.on("connect", () => {
            console.log("Connected to socket.io server");
        });

        socketRef.current.on("disconnect", (reason) => {
            console.log("Disconnected from socket.io server:", reason);
        });

        socketRef.current.on("reconnect_attempt", () => {
            console.log("Attempting to reconnect to socket.io server...");
        });

        socketRef.current.on("vehicle_height", (data) => {
            console.log("Received vehicle height:", data);
            if (data && data.vehicle_id && data.height) {
                setHeightMeasurements(prevMeasurements => [...prevMeasurements, data]);
                console.log("Height measurement received from server:", data);
                console.log("Updated height measurements state with new data.");
            } else {
                console.error("Invalid vehicle height data received:", data);
            }
        });

        return () => {
            console.log("Closing socket connection...");
            socketRef.current.disconnect();
        };
    }, []);

    const handleModelChange = (modelId) => {
        console.log("Model selected:", modelId);
        setModelId(modelId);
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file && file.type === "video/mp4") {
            console.log("File selected:", file);
            setSelectedFile(file);
        } else {
            console.log("Invalid file type selected:", file);
            setSelectedFile(null);
            setUploadError('Please select an MP4 video file.');
        }
    };

    const handleUpload = async () => {
        console.log("Upload button clicked...");
        if (selectedFile && modelId) {
            setIsUploading(true);
            setUploadError('');
            console.log("Starting file upload...");

            const formData = new FormData();
            formData.append('file', selectedFile);

            try {
                console.log("Sending upload request...");
                const response = await axios.post(`${BASE_URL}/api/v1/process-truck-measure/${modelId}`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                    onUploadProgress: progressEvent => {
                        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                        console.log(`Upload progress: ${percentCompleted}%`);
                    }
                });

                if (response.data) {
                    console.log("Upload successful:", response.data.message);
                    onUploadSuccess({ message: response.data.message, modelId }); // Now passing an object with message and modelId
                }
            } catch (error) {
                console.error('Error uploading file:', error);
                setUploadError('Error uploading file. Please try again later.');
            } finally {
                setIsUploading(false);
            }
        } else {
            console.log("Model or file not selected.");
            setUploadError('Please select a model and a video file.');
        }
    };

    return (
        <div>
            <ModelSelection onModelSelected={handleModelChange} />
            <Button variant="contained" component="label" sx={{ marginTop: 2 }}>
                Select Video
                <input type="file" hidden onChange={handleFileChange} accept="video/mp4" />
            </Button>
            <Button variant="contained" color="primary" onClick={handleUpload} disabled={!selectedFile || !modelId || isUploading} sx={{ marginTop: 2, marginLeft: 2 }}>
                {isUploading ? 'Uploading...' : 'Upload Video'}
            </Button>
            {uploadError && <p style={{ color: 'red' }}>{uploadError}</p>}
            <div>
                <h1>Height Measurements</h1>
                <ul>
                    {heightMeasurements.map((measurement, index) => (
                        <li key={index}>
                            Vehicle ID: {measurement.vehicle_id}, Height: {measurement.height}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default VideoUploadAndProcess;
