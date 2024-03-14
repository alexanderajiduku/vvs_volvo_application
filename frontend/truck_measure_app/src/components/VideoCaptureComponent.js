import React from 'react';
import Button from '@mui/material/Button';
import { BASE_URL } from '../config/config';
import axios from 'axios';

class VideoCaptureComponent extends React.Component {
    startVideoCapture = async () => {
        try {
            const response = await axios.post(`${BASE_URL}/api/v1/video/start-video-capture`, {
                input_source: '0'
            });
            console.log('Video capture started:', response.data);
        } catch (error) {
            // Log more detailed error information
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                console.error('Error data:', error.response.data);
                console.error('Error status:', error.response.status);
                console.error('Error headers:', error.response.headers);
            } else if (error.request) {
                // The request was made but no response was received
                console.error('No response received:', error.request);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.error('Error message:', error.message);
            }
            console.error('Error config:', error.config);
        }
    };

    render() {
        return (
            <div style={{ marginTop: 20, display: 'flex', justifyContent: 'center' }}>
                {/* Use Button from Material UI with contained variant for styling */}
                <Button variant="contained" color="primary" onClick={this.startVideoCapture}>
                    Start Video Capture
                </Button>
            </div>
        );
    }
}

export default VideoCaptureComponent;
