import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import UserContext from '../auth/UserContext';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import { useTheme } from '@mui/material/styles';

const Navigation = ({ logout }) => {
    const { currentUser } = useContext(UserContext);
    
    const theme = useTheme();
    

    const loggedInNav = () => {
        if (currentUser) {
            const displayName = currentUser.first_name || currentUser.username;
            return (
                <Box sx={{ flexGrow: 1, justifyContent: 'flex-end', display: 'flex' }}>
                    <Button variant="text" component={NavLink} to="/calibration" sx={{ color: 'white', mr: 2 }}>
                        Calibration
                    </Button>
                    <Button variant="text" component={NavLink} to="/mlmodel" sx={{ color: 'white', mr: 2 }}>
                        ML Model
                    </Button>
                   
                    <Button variant="text" component={NavLink} to="/ultralytics" sx={{ color: 'white', mr: 2 }}>
                        Ultralytics
                    </Button>
                    <Button onClick={logout} sx={{ color: 'white' }}>
                        Log out {displayName}
                    </Button>
                </Box>
            );
        } else {
            return null;
        }
    };
    

    const loggedOutNav = () => (
        <Box sx={{ flexGrow: 1, justifyContent: 'flex-end', display: 'flex' }}>
            <Button variant="text" component={NavLink} to="/signin" sx={{ color: 'white', mr: 2 }}>
                Login
            </Button>
            <Button variant="text" component={NavLink} to="/signup" sx={{ color: 'white' }}>
                Sign Up
            </Button>
        </Box>
    );

    return (
        <AppBar position="static" sx={{ backgroundColor: theme.palette.primary.dark }}>
            <Container maxWidth="xl">
                <Toolbar disableGutters sx={{ justifyContent: 'space-between' }}>
                    <Typography variant="h4" noWrap component="div" sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
                        <a href="https://www.volvo.com" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: 'white', fontWeight: 'bold', display: 'flex', alignItems: 'center' }}>
                            <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ficon-library.com%2Fimages%2F2018%2F10395687_volvo-logo-ab-volvo-hd-png-download.png&f=1&nofb=1" alt="Volvo Logo" style={{ height: '25px', marginRight: '10px' }} />
                            <span>Volvo</span>
                        </a>
                    </Typography>
                    {currentUser ? loggedInNav() : loggedOutNav()}
                </Toolbar>
            </Container>
        </AppBar>
    );
};


export default Navigation;