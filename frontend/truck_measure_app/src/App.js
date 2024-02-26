import React, { useState, useEffect } from "react";
import { BrowserRouter } from "react-router-dom";
import "./App.css";
import RoutesNav from "./routes/RoutesNav";
import Navigation from "./routes/Navigation";
import { jwtDecode } from "jwt-decode";
import useLocalStorage from "./hooks/useLocalStorage";
import AuthApi from "./api/api";
import LoadingSpinner from "./common/LoadingSpinner";
import { UserProvider } from "./auth/UserContext";  
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';
import CssBaseline from '@mui/material/CssBaseline';

export const TOKEN_STORAGE_ID = "Authtoken";

/**
 * The main component of the application.
 * @returns {JSX.Element} The rendered App component.
 */
const App = () => {
  const [infoLoaded, setInfoLoaded] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useLocalStorage(TOKEN_STORAGE_ID);

  useEffect(() => {
    console.debug("App useEffect loadUserInfo", "token=", token);

    const loadUserInfo = async () => {
      if (token) {
        try {
          let { username } = jwtDecode(token);
          AuthApi.token = token;
          let currentUser = await AuthApi.getCurrentUser(username);
          setCurrentUser(currentUser);
        } catch (err) {
          console.error("App loadUserInfo: problem loading", err);
          setCurrentUser(null);
        }
      }
      setInfoLoaded(true);
    };

    setInfoLoaded(false);
    loadUserInfo();
  }, [token]);

  const logout = () => {
    setCurrentUser(null);
    setToken(null);
  };

  const signup = async (signupData) => {
    try {
      let token = await AuthApi.signup(signupData);
      setToken(token);
      return { success: true };
    } catch (errors) {
      console.error("signup failed", errors);
      return { success: false, errors };
    }
  };

  const signin = async (signinData) => {
    try {
      let token = await AuthApi.signin(signinData);
      setToken(token);
      return { success: true };
    } catch (errors) {
      console.error("login failed", errors);
      return { success: false, errors };
    }
  };

  if (!infoLoaded) return <LoadingSpinner />;

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <UserProvider>
        <BrowserRouter>
          <UserProvider value={{ currentUser, setCurrentUser }}>
            <div className="wallpaper">
              <Navigation logout={logout} />
              <RoutesNav signin={signin} signup={signup} />
            </div>
          </UserProvider>
        </BrowserRouter>
      </UserProvider>
    </ThemeProvider>
  );
}

export default App;
