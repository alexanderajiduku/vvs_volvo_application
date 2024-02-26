import React, { useState } from 'react';
import { Button, TextField, FormControlLabel, Checkbox, Link, Grid, Box, Typography, Container, Snackbar, Alert, CssBaseline } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import { useUserContext } from './UserContext';
import AuthApi from '../api/api';
import { Link as RouterLink } from 'react-router-dom';


const customTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ffffff', 
    },
   
    secondary: {
      main: '#ffffff', 
    },
    background: {
      default: '#0C7078',
      paper: '#0F988C',
    },

    text: {
      primary: '#ffffff',
      secondary: '#ffffff',
    },
  },
  components: {
  
    MuiTextField: {
      styleOverrides: {
        root: {
          '& label': {
            color: '#ffffff', 
          },
          '& .MuiInput-underline:before': {
            borderBottomColor: '#ffffff',
          },
          '& .MuiInput-underline:hover:not(.Mui-disabled):before': {
            borderBottomColor: '#ffffff', 
          },
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: '#ffffff', 
            },
            '&:hover fieldset': {
              borderColor: '#ffffff', 
            },
            '&.Mui-focused fieldset': {
              borderColor: '#ffffff', 
            },
          },
        },
      },
    },
  },
});

/**
 * Renders a sign-in form component.
 * 
 * @returns {JSX.Element} The sign-in form component.
 */

export default function SignIn() {
  const navigate = useNavigate();
  const { setAuthToken, setCurrentUser, } = useUserContext();
  const [errorMessage, setErrorMessage] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);

  const handleErrors = (errors) => {
    setErrorMessage(errors.join(', '));
    setOpenSnackbar(true);
    return;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const formData = {
        email: data.get('email'),
        password: data.get('password'),
    };

    try {
        const response = await AuthApi.signin(formData);
        if (response.success) {
            setCurrentUser(response.user);
            navigate('/protected/component'); 
        } else {
            console.error('SignIn failed with response:', { success, errors });
            handleErrors(errors || ['An error occurred. Please try again.']);
        }
    } catch (error) {
        console.error('SignIn Error:', error);
        setErrorMessage('An unexpected error occurred. Please try again.');
        setOpenSnackbar(true);
    }
};

  return (
    <ThemeProvider theme={customTheme}> 
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email"
              name="email"
              autoComplete="email"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item xs>
                <Link href="#" variant="body2">
                  Forgot password?
                </Link>
              </Grid>
              <Grid item>
                <Link href="#" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
        <Box mt={8} mb={4} align="center">
          <Typography variant="body2" color="text.secondary">
            {'Copyright © '}
            <Link color="inherit" href="https://yourwebsite.com/">
              Your Website
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
          </Typography>
        </Box>
        <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={() => setOpenSnackbar(false)}>
          <Alert onClose={() => setOpenSnackbar(false)} severity="error" sx={{ width: '100%' }}>
            {errorMessage}
          </Alert>
        </Snackbar>
      </Container>
    </ThemeProvider>
  );
}
