import React, { useState } from 'react';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import UltralyticsFileUpload from './UltralyticsFileUpload';
import AnnotatedResultDisplay from './AnnotatedResultDisplay';
import ModelSelection from './ModelSelection';

/**
 * Ultralytics component for performing inference.
 * @returns {JSX.Element} The Ultralytics component.
 */
const Ultralytics = () => {
  const [selectedModelId, setSelectedModelId] = useState(null);  
  const [fileType, setFileType] = useState('');
  const [fileUrl, setFileUrl] = useState('');


  const handleModelSelected = (modelId) => {
    setSelectedModelId(modelId);  
  };

  const handleUploadSuccess = (annotatedFileKey, type) => {
    setFileUrl(annotatedFileKey);
    setFileType(type.split('/')[1]); 
  };

  return (
    <Container maxWidth="lg">
       <Typography variant="h4" component="h4" gutterBottom sx={{ textAlign: 'center', color: '#fff' }}>
        Ultralytics Inference
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <ModelSelection onModelSelected={handleModelSelected} />  
        </Grid>
        <Grid item xs={12}>
          <UltralyticsFileUpload selectedModelId={selectedModelId} onUploadSuccess={handleUploadSuccess} />  
        </Grid>
        {fileUrl && (
          <Grid item xs={12} sm={6}>
            <AnnotatedResultDisplay key={fileUrl} fileType={fileType} fileUrl={fileUrl} />
          </Grid>
        )}
      </Grid>
    </Container>
  );
};

export default Ultralytics;
