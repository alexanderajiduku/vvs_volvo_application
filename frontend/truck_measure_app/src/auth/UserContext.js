import React, { createContext, useContext, useState } from "react";

const defaultContextValue = {
  currentUser: null,
  setCurrentUser: () => {},
  cameras: [], 
  setCameras: () => {}, 
};

const UserContext = createContext(defaultContextValue);

export const UserProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [authToken, setAuthToken] = useState(""); 
  const [cameras, setCameras] = useState([]); // Initialize with an empty array

  const value = { currentUser, setCurrentUser, cameras, setCameras, authToken, setAuthToken};

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};

export const useUserContext = () => useContext(UserContext);

export default UserContext;