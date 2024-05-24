import React, { useState, useEffect } from 'react';
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TablePagination, TableRow, Typography, Box, Snackbar, Alert } from '@mui/material';
import axios from 'axios';
import { BASE_URL } from '../config/config';

const columns = [
    { id: 'id', label: 'ID', minWidth: 100 },
    { id: 'vehicle_id', label: 'Vehicle ID', minWidth: 170 },
    { id: 'height', label: 'Height', minWidth: 170 },
    {
        id: 'created_at',
        label: 'Created At',
        minWidth: 170,
        align: 'right',
        format: (value) => new Date(value).toLocaleString()
    },
];

const VehicleDetailTable = () => {
    const [data, setData] = useState([]);
    const [error, setError] = useState('');
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`${BASE_URL}/api/v1/vehicle-details`);
                setData(response.data);
            } catch (error) {
                setError('Failed to fetch vehicle details');
                console.error('Error fetching vehicle details:', error);
            }
        };

        fetchData();
    }, []);

    const handleChangePage = (event, newPage) => setPage(newPage);
    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };
    const handleCloseSnackbar = () => setError('');

    return (
        <Box sx={{ p: 3, bgcolor: '#121212', overflow: 'hidden' }}>
            <Typography variant="h6" align="center" gutterBottom style={{ color: '#fff' }}>
                Vehicle Details
            </Typography>
            <Paper sx={{ width: '100%', bgcolor: '#000' }}>
                <TableContainer sx={{ maxHeight: 440 }}>
                    <Table stickyHeader aria-label="vehicle details table">
                        <TableHead>
                            <TableRow>
                                {columns.map((column) => (
                                    <TableCell
                                        key={column.id}
                                        align={column.align || 'left'}
                                        style={{ minWidth: column.minWidth, color: '#fff', backgroundColor: '#008080' }} // Blue background color
                                    >
                                        {column.label}
                                    </TableCell>
                                ))}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => (
                                <TableRow hover tabIndex={-1} key={row.id}>
                                    {columns.map((column) => {
                                        const value = row[column.id];
                                        return (
                                            <TableCell key={column.id} align={column.align} style={{ color: '#fff' }}>
                                                {column.format && column.id === 'created_at' ? column.format(value) : value}
                                            </TableCell>
                                        );
                                    })}
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
                <TablePagination
                    rowsPerPageOptions={[10, 25, 100]}
                    component="div"
                    count={data.length}
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onPageChange={handleChangePage}
                    onRowsPerPageChange={handleChangeRowsPerPage}
                    sx={{ '.MuiToolbar-root': { color: '#fff' }, '.MuiSvgIcon-root': { color: '#fff' } }} />
            </Paper>
            {error && (
                <Snackbar open={Boolean(error)} autoHideDuration={6000} onClose={handleCloseSnackbar}>
                    <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
                        {error}
                    </Alert>
                </Snackbar>
            )}
        </Box>
    );
};

export default VehicleDetailTable;
