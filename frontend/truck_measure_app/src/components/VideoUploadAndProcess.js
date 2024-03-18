// import React, { useState } from 'react';
// import Button from '@mui/material/Button';
// import axios from 'axios';
// import { BASE_URL } from '../config/config'; 
// import ModelSelection from './ModelSelection'; 

// const VideoUploadAndProcess = ({ onUploadSuccess }) => {
//     const [selectedFile, setSelectedFile] = useState(null);
//     const [modelId, setModelId] = useState('');

//     const handleModelChange = (modelId) => {
//         setModelId(modelId);
//     };

//     const handleFileChange = (event) => {
//         const file = event.target.files[0];
//         if (file && file.type === "video/mp4") {
//             setSelectedFile(file);
//         } else {
//             alert("Please select an MP4 video file.");
//         }
//     };

//     const handleUpload = async () => {
//         if (selectedFile && modelId) {
//             const formData = new FormData();
//             formData.append('file', selectedFile);

//             try {
//                 const response = await axios.post(`${BASE_URL}/api/v1/process-truck-measure/${modelId}`, formData, {
//                     headers: {
//                         'Content-Type': 'multipart/form-data',
//                     },
//                 });

//                 if (response.data) {
//                     console.log(response.data.message);
//                     onUploadSuccess();
//                 }
//             } catch (error) {
//                 console.error('Error uploading file:', error);
//             }
//         } else {
//             alert("Please select a model and a video file.");
//         }
//     };

//     return (
//         <div>
//             <ModelSelection onModelSelected={handleModelChange} />
//             <Button variant="contained" component="label" sx={{ marginTop: 2 }}>
//                 Select Video
//                 <input type="file" hidden onChange={handleFileChange} accept="video/mp4" />
//             </Button>
//             <Button variant="contained" color="primary" onClick={handleUpload} disabled={!selectedFile || !modelId} sx={{ marginTop: 2, marginLeft: 2 }}>
//                 Upload Video
//             </Button>
//         </div>
//     );
// };

// export default VideoUploadAndProcess;


// import React, { useState } from 'react';
// import Button from '@mui/material/Button';
// import TextField from '@mui/material/TextField'; // For input fields
// import axios from 'axios';
// import { BASE_URL } from '../config/config'; 
// import ModelSelection from './ModelSelection'; 

// const VideoUploadAndProcess = ({ onUploadSuccess }) => {
//     const [selectedFile, setSelectedFile] = useState(null);
//     const [modelId, setModelId] = useState('');
//     const [cameraId, setCameraId] = useState(''); // State for camera ID

//     const handleModelChange = (modelId) => {
//         setModelId(modelId);
//     };

//     const handleFileChange = (event) => {
//         const file = event.target.files[0];
//         if (file && file.type === "video/mp4") {
//             setSelectedFile(file);
//         } else {
//             alert("Please select an MP4 video file.");
//         }
//     };

//     const handleUpload = async () => {
//         if (selectedFile && modelId) {
//             const formData = new FormData();
//             formData.append('file', selectedFile);

//             try {
//                 const response = await axios.post(`${BASE_URL}/api/v1/process-truck-measure/${modelId}`, formData, {
//                     headers: {
//                         'Content-Type': 'multipart/form-data',
//                     },
//                 });

//                 if (response.data) {
//                     console.log(response.data.message);
//                     onUploadSuccess();
//                 }
//             } catch (error) {
//                 console.error('Error uploading file:', error);
//             }
//         } else {
//             alert("Please select a model and a video file.");
//         }
//     };

//     const handleStartCamera = async () => {
//         if (modelId && cameraId) {
//             try {
//                 const response = await axios.post(`${BASE_URL}/api/v1/process-truck-measure/${modelId}/${cameraId}`, {}, {
//                     headers: {
//                         'Content-Type': 'application/json',
//                     },
//                 });

//                 if (response.data) {
//                     console.log(response.data.message);
//                 }
//             } catch (error) {
//                 console.error('Error starting camera:', error);
//             }
//         } else {
//             alert("Please select a model and specify a camera ID.");
//         }
//     };

//     return (
//         <div>
//             <ModelSelection onModelSelected={handleModelChange} />
//             <TextField
//                 label="Camera ID"
//                 variant="outlined"
//                 value={cameraId}
//                 onChange={(e) => setCameraId(e.target.value)}
//                 sx={{ marginTop: 2, marginRight: 2 }}
//                 fullWidth
//             />
//             <Button variant="contained" component="label" sx={{ marginTop: 2 }}>
//                 Select Video
//                 <input type="file" hidden onChange={handleFileChange} accept="video/mp4" />
//             </Button>
//             <Button variant="contained" color="primary" onClick={handleUpload} disabled={!selectedFile || !modelId} sx={{ marginTop: 2, marginLeft: 2 }}>
//                 Upload Video
//             </Button>
//             <Button variant="contained" color="secondary" onClick={handleStartCamera} disabled={!modelId || !cameraId} sx={{ marginTop: 2, marginLeft: 2 }}>
//                 Start Camera
//             </Button>
//         </div>
//     );
// };

// export default VideoUploadAndProcess;



import React, { useState } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import axios from 'axios';
import { BASE_URL } from '../config/config'; 
import ModelSelection from './ModelSelection'; 

const VideoUploadAndProcess = ({ onUploadSuccess }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [modelId, setModelId] = useState('');
    const [cameraId, setCameraId] = useState('');

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
                    onUploadSuccess();
                }
            } catch (error) {
                console.error('Error uploading file:', error);
            }
        } else {
            alert("Please select a model and a video file.");
        }
    };

    const handleStartCamera = async () => {
        if (modelId && cameraId) {
            try {
                const response = await axios.post(`${BASE_URL}/api/v1/process-truck-measure/${modelId}/${cameraId}`, {}, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (response.data) {
                    console.log(response.data.message);
                }
            } catch (error) {
                console.error('Error starting camera:', error);
            }
        } else {
            alert("Please select a model and specify a camera ID.");
        }
    };

    const handleCameraIdChange = (e) => {
        const newValue = e.target.value;
        // Allow only a single digit
        if (newValue === '' || /^[0-9]$/.test(newValue)) {
            setCameraId(newValue);
        }
    };

    return (
        <div style={{ backgroundColor: '#000', color: '#fff', padding: '20px' }}>
            <ModelSelection onModelSelected={handleModelChange} />
            <TextField
                label="Camera ID"
                variant="outlined"
                value={cameraId}
                onChange={handleCameraIdChange}
                sx={{
                    marginTop: 2,
                    marginRight: 2,
                    width: '150px', 
                    input: { color: '#fff' }, 
                    label: { color: '#aaa' }, 
                    '& .MuiOutlinedInput-root': {
                        '& fieldset': {
                            borderColor: '#fff',
                        },
                        '&:hover fieldset': {
                            borderColor: '#fff', 
                        },
                        '&.Mui-focused fieldset': {
                            borderColor: '#fff', 
                        },
                    },
                }}
                InputLabelProps={{
                    style: { color: '#fff' }, 
                }}
                fullWidth={false} 
            />
            <Button variant="contained" component="label" sx={{ marginTop: 2 }}>
                Select Video
                <input type="file" hidden onChange={handleFileChange} accept="video/mp4" />
            </Button>
            <Button variant="contained" color="primary" onClick={handleUpload} disabled={!selectedFile || !modelId} sx={{ marginTop: 2, marginLeft: 2 }}>
                Upload Video
            </Button>
            <Button variant="contained" color="secondary" onClick={handleStartCamera} disabled={!modelId || !cameraId} sx={{ marginTop: 2, marginLeft: 20 }}>
                Start Camera
            </Button>
        </div>
    );
};

export default VideoUploadAndProcess;
