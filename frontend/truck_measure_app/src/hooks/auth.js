// auth.js
import useLocalStorage from "./useLocalStorage";

const useAuth = () => {
  const [authToken, setAuthToken] = useLocalStorage("authToken", "");
  const isAuthenticated = !!authToken;
  return { isAuthenticated, authToken, setAuthToken };
}

export default useAuth;
