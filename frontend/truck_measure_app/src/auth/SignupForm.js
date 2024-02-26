import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUserContext } from './UserContext'; // Update the path as necessary
import AuthApi from '../api/api' // Update the path as necessary
import { Button, TextField, FormControlLabel, Checkbox, Link, Grid, Box, Typography, Container, Snackbar, Alert, CssBaseline } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { Link as RouterLink } from 'react-router-dom';


const customTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ffffff', 
    },
    secondary: {
      main: '#eeeeee',
    },
    background: {
      default: '#0C7078',
      paper: '#0F988C',
    },
    text: {
      primary: '#ffffff', 
      secondary: '#eeeeee', 
    },
  },
  components: {
    MuiTextField: {
      styleOverrides: {
        root: {
          '& label.Mui-focused': {
            color: '#ffffff', 
          },
          '& .MuiInput-underline:after': {
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
    MuiCheckbox: {
      styleOverrides: {
        root: {
          color: '#ffffff', 
        },
      },
    },
  },
});

/**
 * Renders a sign-up form component.
 *
 * @returns {JSX.Element} The sign-up form component.
  */

export default function SignUp() {
  const navigate = useNavigate();
  const { setAuthToken, setCurrentUser } = useUserContext();
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const payload = {
      first_name: data.get('firstName'),
      last_name: data.get('lastName'),
      username: data.get('username'),
      email: data.get('email'),
      password: data.get('password'),
    };

    // Client-side validation
    if (!payload.email || !payload.password || !payload.username) {
      setErrorMessage("Username, password, and email are required.");
      setOpenSnackbar(true);
      return;
    }

    try {
      const response = await AuthApi.signup(payload);
      if (response.success) {
        setAuthToken(response.token); 
        setCurrentUser(response.user); 
        navigate('/protected/component'); 
      } else {
        const errors = response.errors ? extractErrorMessages(response) : ['An error occurred during signup. Please try again.'];
        handleErrors(errors);
      }
    } catch (error) {
      console.error('Signup failed:', error);
      handleErrors(['An unexpected error occurred. Please try again.']);
    }
  };

  const handleErrors = (errors) => {
    setErrorMessage(errors.join(', '));
    setOpenSnackbar(true);
  };

  const extractErrorMessages = (data) => {
    if (Array.isArray(data.errors)) {
      return data.errors.map(err => err.message || err);
    } else if (data.message) {
      return [data.message];
    }
    return ['An unexpected error occurred. Please try again.'];
  };

  return (
    <ThemeProvider theme={customTheme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Typography component="h1" variant="h5">
            Sign Up
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField autoComplete="given-name" name="firstName" required fullWidth id="firstName" label="First Name" autoFocus />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField required fullWidth id="lastName" label="Last Name" name="lastName" autoComplete="family-name" />
              </Grid>
              <Grid item xs={12}>
                <TextField required fullWidth id="username" label="Username" name="username" autoComplete="username" />
              </Grid>
              <Grid item xs={12}>
                <TextField required fullWidth id="email" label="Email Address" name="email" autoComplete="email" />
              </Grid>
              <Grid item xs={12}>
                <TextField required fullWidth name="password" label="Password" type="password" id="password" autoComplete="new-password" />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel control={<Checkbox value="allowExtraEmails" color="primary" />} label="I want to receive marketing promotions and updates via email." />
              </Grid>
            </Grid>
            <Button
                      type="submit"
                      fullWidth
                      variant="contained"
                      sx={{
                        mt: 3,
                        mb: 2,
                        color: 'text.primary', 
                        backgroundColor: '#000000', 
                        '&:hover': {
                          backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        },
                      }}
                    >
                      Sign Up
            </Button>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link component={RouterLink} to="/signin" variant="body2">
                  Already have an account? Sign in
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
        <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={() => setOpenSnackbar(false)}>
          <Alert onClose={() => setOpenSnackbar(false)} severity="error" sx={{ width: '100%' }}>
            {errorMessage}
          </Alert>
        </Snackbar>
        <Box mt={5} align="center">
          <Typography variant="body2" color="text.secondary">
            {'Copyright © '}
            <Link color="inherit" href="https://volvo.com/">
              Volvo Trucks Inc
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
          </Typography>
        </Box>
      </Container>
    </ThemeProvider>
  );
}


