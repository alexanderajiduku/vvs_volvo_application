import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark', 
    primary: {
      main: '#05161A', 
    },
    secondary: {
      main: '#072E33', 
    },
    background: {
      default: '#0C7078', 
      paper: '#0F988C', 
    },
    text: {
      primary: '#294D61', 
      secondary: '#6DA5C0', 
    },

    error: {
      main: '#05161A', 
    },
    warning: {
      main: '#072E33',
    },
    info: {
      main: '#0C7078', 
    },
    success: {
      main: '#0F988C', 
    },
  },

});

export default theme;
