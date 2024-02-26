import React from 'react';
import { Grid, Box } from '@mui/material';
import ModelTable from './ModelTable';
import ModelForm from './ModelForm';

/**
 * Renders the MLModel component.
 * @returns {JSX.Element} The MLModel component.
 */
const MLModel = () => (
    <Box sx={{ flexGrow: 1, p: 2 }}>
        <Grid container spacing={2} justifyContent="center">
            <Grid item xs={12} sm={6} md={4}>
                <ModelForm />
            </Grid>
            <Grid item xs={12} sm={8} md={6}>
                <Box sx={{ width: '100%' }}>
                    <ModelTable />
                </Box>
            </Grid>
        </Grid>
    </Box>
);

export default MLModel;

