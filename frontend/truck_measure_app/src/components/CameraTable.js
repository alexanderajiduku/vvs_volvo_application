import React, { useState, useEffect } from 'react';
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TablePagination, TableRow, Typography, Box } from '@mui/material';
import AuthApi from '../api/api';

const columns = [
  { id: 'camera_name', label: 'Camera Name', minWidth: 170 },
  { id: 'camera_model', label: 'Camera Model', minWidth: 100 },
  {
    id: 'checkerboard_width',
    label: 'Checkerboard Width',
    minWidth: 170,
    align: 'right',
  },
  {
    id: 'checkerboard_height',
    label: 'Checkerboard Height',
    minWidth: 170,
    align: 'right',
  },
  {
    id: 'description',
    label: 'Description',
    minWidth: 170,
    align: 'right',
  },
];

/**
 * Renders a table component that displays registered cameras.
 * @returns {JSX.Element} The CameraTable component.
 */
const CameraTable = () => {
  const [cameras, setCameras] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  useEffect(() => {
    const fetchCameras = async () => {
      try {
        const response = await AuthApi.getAllCameras(); 
        if (response.success) {
          setCameras(response.cameras);
        } else {
          console.error('Failed to fetch cameras:', response.errors);
        }
      } catch (error) {
        console.error('Error fetching cameras:', error);
      }
    };

    fetchCameras();
  }, []);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  return (
    <Box sx={{ p: 2, bgcolor: '#121212', borderRadius: '4px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
      <Paper sx={{ width: '100%', overflow: 'hidden', bgcolor: '#121212', color: '#fff' }}>
        <Typography variant="h6" align="center" sx={{ my: 2, color: '#fff' }}>
          Registered Cameras
        </Typography>
        <TableContainer>
          <Table stickyHeader aria-label="camera table">
            <TableHead>
              <TableRow>
                {columns.map((column) => (
                  <TableCell
                    key={column.id}
                    align={column.align || 'center'}
                    sx={{ minWidth: column.minWidth, fontWeight: 'bold', color: '#fff', bgcolor: '#121212' }}
                  >
                    {column.label}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {cameras.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((camera) => (
                <TableRow hover tabIndex={-1} key={camera.id}>
                  {columns.map((column) => {
                    const value = camera[column.id];
                    return (
                      <TableCell key={column.id} align={column.align || 'center'} sx={{ color: '#fff' }}>
                        {value}
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
          count={cameras.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          sx={{
            color: '#fff',
            '.MuiTablePagination-selectLabel, .MuiTablePagination-select, .MuiTablePagination-selectIcon, .MuiTablePagination-actions': {
              color: '#fff',
            },
          }}
        />
      </Paper>
    </Box>
  );
};

export default CameraTable;
