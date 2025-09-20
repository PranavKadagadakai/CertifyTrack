import React, { createContext, useState, useContext } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const login = async (username, password) => {
    try {
      const response = await api.post("login/", { username, password });
      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);
      setUser(response.data.user); // <-- Set user from response
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  };

  const register = async (userData) => {
    try {
      await api.post("register/", userData);
      // Optionally auto-login after registration
      await login(userData.username, userData.password);
    } catch (error) {
      throw error.response?.data || error;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    navigate("/login");
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
