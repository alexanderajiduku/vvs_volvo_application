import React from 'react';
import Tooltip from '@mui/material/Tooltip';
import IconButton from '@mui/material/IconButton';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

const CustomTooltip = ({ title, placement = 'right', color = 'inherit' }) => { // Default color is 'inherit'
  return (
    <Tooltip title={title} placement={placement}>
      <IconButton size="small" aria-label={title}>
        <HelpOutlineIcon sx={{ color: color }} /> {/* Apply the color prop */}
      </IconButton>
    </Tooltip>
  );
};

export default CustomTooltip;
