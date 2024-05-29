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
  
            if (error.response) {
                console.error('Error data:', error.response.data);
                console.error('Error status:', error.response.status);
                console.error('Error headers:', error.response.headers);
            } else if (error.request) {
                console.error('No response received:', error.request);
            } else {
                console.error('Error message:', error.message);
            }
            console.error('Error config:', error.config);
        }
    };

    render() {
        return (
            <div style={{ marginTop: 20, display: 'flex', justifyContent: 'center' }}>
                <Button variant="contained" color="primary" onClick={this.startVideoCapture}>
                    Start Video Capture
                </Button>
            </div>
        );
    }
}

export default VideoCaptureComponent;
