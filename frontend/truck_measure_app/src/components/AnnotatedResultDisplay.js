import React from 'react';

/**
 * Renders the annotated result display component.
 * @param {Object} props - The component props.
 * @param {string} props.fileUrl - The URL of the file to be displayed.
 * @returns {JSX.Element} The rendered annotated result display component.
 */
const AnnotatedResultDisplay = ({ fileUrl }) => {
    const baseURL = "http://localhost:8000/static/";
    const displayUrl = `${baseURL}${fileUrl}`;


    const isVideo = fileUrl.endsWith('.mp4');  
    return (
        <div>
            {isVideo ? (
                <video src={displayUrl} controls preload="metadata" style={{ maxWidth: '100%', height: 'auto' }}>
                    Your browser does not support the video tag.
                </video>
            ) : (
                <img src={displayUrl} alt="Annotated result" style={{ maxWidth: '100%' }} />
            )}
        </div>
    );
};

export default AnnotatedResultDisplay;
