import React, { useState, useEffect } from 'react';
import { Box, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TablePagination, TableRow, Typography, IconButton, Snackbar, Alert } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import AuthApi from '../api/api';
import CustomTooltip from '../common/CustomToolTip';

const columns = [
  { id: 'name', label: 'Name', minWidth: 170 },
  { id: 'id', label: 'ID', minWidth: 100 },
  { id: 'description', label: 'Description', minWidth: 250 },
  { id: 'created_at', label: 'Created At', minWidth: 170, align: 'right', format: (value) => new Date(value).toLocaleString() },
  { id: 'select', label: 'Select', minWidth: 100, align: 'center' },
];

/**
 * ModelSelection component displays a table of selectable models.
 * It fetches the models from the server and allows the user to select a model.
 * When a model is selected, it calls the onModelSelected callback function with the selected model ID.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {Function} props.onModelSelected - The callback function to be called when a model is selected.
 * @returns {JSX.Element} The ModelSelection component.
 */
const ModelSelection = ({ onModelSelected }) => {
  const [models, setModels] = useState([]);
  const [selectedModelId, setSelectedModelId] = useState(null);
  const [error, setError] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [selectedModelPath, setSelectedModelPath] = useState('');

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


  const getModelPath = async (model_id) => {
    try {
      const response = await AuthApi.getModelPath(model_id);
  
      if (!response || !response.success || !response.model_path) {
        console.error('Invalid response:', response);
        throw new Error('Invalid response');
      }
  
      return response.model_path;
    } catch (error) {
      console.error('Error fetching model path:', error);
      throw new Error('Failed to fetch model path');
    }
  };
  

  
  const handleSelectModel = async (model_id) => {
    try {
      const modelPath = await getModelPath(model_id);
      if (modelPath) {
        setSelectedModelPath(modelPath);
        setSelectedModelId(model_id);
        onModelSelected(model_id);
      } else {
        setError('Model path not found');
      }
    } catch (error) {
      console.error('Error selecting model:', error);
      setError('Failed to select model');
    }
  };
  

  const handleChangePage = (event, newPage) => setPage(newPage);
  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };
  const handleCloseSnackbar = () => setError('');

  return (
    <Box sx={{ p: 3, bgcolor: '#121212', overflow: 'hidden' }}>
      <Typography variant="h6" align="center" gutterBottom sx={{ color: '#fff' }}>
        Selectable Models
        <CustomTooltip title="Select a model of choice for inference and annotation" />
      </Typography>
      <Paper sx={{ width: '100%', bgcolor: '#000' }}>
        <TableContainer sx={{ maxHeight: 440 }}>
          <Table stickyHeader aria-label="sticky table">
            <TableHead>
              <TableRow>
                {columns.map((column) => (
                  <TableCell key={column.id} align={column.align || 'left'} style={{ minWidth: column.minWidth, color: '#fff' }}>
                    {column.label}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {models.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((model) => (
                <TableRow hover key={model.id} selected={model.id === selectedModelId} onClick={() => handleSelectModel(model.id)} sx={{ cursor: 'pointer', '&.Mui-selected, &.Mui-selected:hover': { backgroundColor: 'rgba(255, 255, 255, 0.08)' } }}>
                  {columns.map((column) => (
                    <TableCell key={column.id} align={column.align} style={{ color: '#fff' }}>
                      {column.id === 'select' ? (
                        <IconButton color="inherit">
                          {selectedModelId === model.id ? <CheckCircleIcon style={{ color: '#fff' }} /> : <CheckCircleIcon style={{ opacity: 0.3, color: '#fff' }} />}
                        </IconButton>
                      ) : column.format && column.id === 'created_at' ? column.format(model[column.id]) : model[column.id]}
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
          sx={{ '.MuiToolbar-root': { color: '#fff' }, '.MuiSvgIcon-root': { color: '#fff' } }}
        />
      </Paper>
      {error && (
        <Snackbar open={Boolean(error)} autoHideDuration={6000} onClose={handleCloseSnackbar}>
          <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
            {error}
          </Alert>
        </Snackbar>
      )}
      {selectedModelPath && <p></p>}
    </Box>
  );
};

export default ModelSelection;
