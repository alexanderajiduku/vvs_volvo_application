import React, { useState } from 'react';
import VideoFeed from './VideoFeed'; 
import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 'auto',
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

/**
 * Represents a component that displays a video window.
 * @component
 */
const VideoWindow = () => {
    const [isVisible, setIsVisible] = useState(false);
  
    const handleClose = () => setIsVisible(false);
  
    return (
      <div>
        <Button variant="contained" onClick={() => setIsVisible(true)}>
          Show Video Feed
        </Button>
        <Modal
          open={isVisible}
          onClose={handleClose}
          aria-labelledby="video-feed-modal"
          aria-describedby="modal-modal-description"
        >
          <Box sx={style}>
            <Button variant="contained" onClick={handleClose} style={{ marginBottom: '10px' }}>
              Close
            </Button>
            <VideoFeed isActive={isVisible} />
          </Box>
        </Modal>
      </div>
    );
  };
  
export default VideoWindow;
