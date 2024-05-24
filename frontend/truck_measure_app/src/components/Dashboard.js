import React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import VehicleDetailTable from './VehicleDetailTable';
import Paper from '@mui/material/Paper';
import LineChart from './LineChart';
import BarChart from './BarChart';

const theme = createTheme();

const Dashboard = () => {
    return (
        <ThemeProvider theme={theme}>
            <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
                <Grid container spacing={5} justifyContent="space-between">
                    <Grid item xs={12} md={8}>
                        <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 240 }}>
                            <Typography variant="h6" gutterBottom>
                                Number of Vehicles Month-Year
                            </Typography>
                            <LineChart />
                        </Paper>
                    </Grid>
                    <Grid item xs={12} md={4}>
                        <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 240 }}>
                            <Typography variant="h6" gutterBottom>
                                Vehicle Height Distribution
                            </Typography>
                            <BarChart />
                        </Paper>
                    </Grid>
                    <Grid item xs={12}>
                        <VehicleDetailTable />
                    </Grid>
                </Grid>
            </Container>
        </ThemeProvider>
    );
};

export default Dashboard;
