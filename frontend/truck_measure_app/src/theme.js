import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark', // Ensuring the theme stays dark
    primary: {
      main: '#05161A', // Using the darkest shade for primary elements like buttons
    },
    secondary: {
      main: '#072E33', // Next darkest shade for secondary elements
    },
    background: {
      default: '#0C7078', // Lighter shade for the main background
      paper: '#0F988C', // Even lighter for paper elements, providing a subtle contrast
    },
    text: {
      primary: '#294D61', // Light shade for primary text, ensuring readability
      secondary: '#6DA5C0', // Lightest shade for secondary text, enhancing contrast and readability
    },
    // Since the provided colors don't include specific hues for error, warning, info, and success states,
    // you might consider reusing some of the given colors or defining new ones that fit within your palette.
    error: {
      main: '#05161A', // Example: Reusing a darker shade for errors
    },
    warning: {
      main: '#072E33', // Example: Using a slightly lighter dark shade for warnings
    },
    info: {
      main: '#0C7078', // Example: Lighter shade for info, consistent with the background
    },
    success: {
      main: '#0F988C', // Example: Lightest shade for success, aligning with paper elements
    },
  },
  // Additional customizations can go here
});

export default theme;
