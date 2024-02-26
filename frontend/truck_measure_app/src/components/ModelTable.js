import React, { useState, useEffect } from 'react';
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TablePagination, TableRow, Typography, Box, Snackbar, Alert } from '@mui/material';
import AuthApi from '../api/api';

const columns = [
  { id: 'name', label: 'Name', minWidth: 170 },
  { id: 'id', label: 'ID', minWidth: 100 }, 
  { id: 'description', label: 'Description', minWidth: 250 },
  { 
    id: 'created_at',  
    label: 'Created At', 
    minWidth: 170, 
    align: 'right', 
    format: (value) => new Date(value).toLocaleString() 
  },
]

/**
 * Represents a table component for displaying models.
 * @component
 */
const ModelTable = () => {
  const [models, setModels] = useState([]);
  const [error, setError] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const response = await AuthApi.getAllModels();
        if (response.success) {
          setModels(response.models);
        } else {
          setError('Failed to fetch models');
        }
      } catch (error) {
        setError('Error fetching models');
        console.error('Error fetching models:', error);
      }
    };

    fetchModels();
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
        Models Upload
      </Typography>
      <Paper sx={{ width: '100%', bgcolor: '#000' }}> 
        <TableContainer sx={{ maxHeight: 440 }}>
          <Table stickyHeader aria-label="sticky table">
            <TableHead>
              <TableRow>
                {columns.map((column) => (
                  <TableCell
                    key={column.id}
                    align={column.align || 'left'}
                    style={{ minWidth: column.minWidth, color: '#fff' }}> 
                    {column.label}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {models.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((model) => (
                <TableRow key={model.id}> 
                  {columns.map((column) => (
                    <TableCell key={column.id} align={column.align} style={{ color: '#fff' }}> 
                      {column.format && column.id === 'created_at' ? column.format(model[column.id]) : model[column.id]}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[10, 25, 100]}
          component="div"
          count={models.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          sx={{ '.MuiToolbar-root': { color: '#fff' }, '.MuiSvgIcon-root': { color: '#fff' } }}/>
      </Paper>
      {error && (
        <Snackbar open={Boolean(error)} autoHideDuration={6000} onClose={handleCloseSnackbar}>
          <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
            {error}
          </Alert>
        </Snackbar>)}
    </Box>
  );
};

export default ModelTable;
