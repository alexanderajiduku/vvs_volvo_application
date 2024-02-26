import React from 'react';

const ImageViewer = ({ imageUrl }) => {
  return (
    <div>
      <img src={imageUrl} alt="Uploaded Image" />
    </div>
  );
};

export default ImageViewer;
