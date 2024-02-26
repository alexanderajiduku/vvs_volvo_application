import React, { useState, useEffect } from 'react';
import AuthApi from '../api/api';


/**
 * Renders a component that displays a live video feed.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {boolean} props.isActive - Indicates whether the video feed is active.
 * @returns {JSX.Element} The rendered VideoFeed component.
 */
const VideoFeed = ({ isActive }) => {
  const [isError, setIsError] = useState(false);
  const camera_id = 1; 
  const videoFeedUrl = `http://localhost:8000/video-feed/${camera_id}`;

  useEffect(() => {
    if (isActive) {
      const authToken = AuthApi.getAuthToken();
      fetch(videoFeedUrl, {
        headers: {
          'Authorization': `Bearer ${authToken}` 
        }
      }).then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
      }).catch(() => {
        setIsError(true);
      });
    }
  }, [isActive, videoFeedUrl]);
  if (isError) {
    return <div>Error loading video feed. Please try again later.</div>;
  }

  return (
    <div>
      <h2>Live Video Feed</h2>
      <img src={videoFeedUrl} alt="Live Video Feed" />
    </div>
  );
};


export default VideoFeed;
