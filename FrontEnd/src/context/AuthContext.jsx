// FrontEnd/src/context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

export const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Load user if access token exists
  useEffect(() => {
    const loadUser = async () => {
      const access = localStorage.getItem("access");
      if (!access) {
        setLoading(false);
        return;
      }

      try {
        const response = await api.get("/profile/");
        setUser(response.data);
      } catch (err) {
        console.error("Profile load failed:", err);
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
      }
      setLoading(false);
    };

    loadUser();
  }, []);

  const register = async (payload) => {
    try {
      await api.post("/auth/register/", payload);
      return { success: true };
    } catch (err) {
      throw err;
    }
  };

  const login = async (username, password) => {
    try {
      const response = await api.post("/auth/login/", { username, password });

      const { access, refresh } = response.data;

      // Save tokens
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);

      // Fetch user profile
      const profile = await api.get("/profile/");
      setUser(profile.data);

      navigate("/dashboard");
    } catch (err) {
      console.error("Login failed:", err);
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setUser(null);
    navigate("/");
  };

  const refreshUser = async () => {
    try {
      const profile = await api.get("/profile/");
      setUser(profile.data);
    } catch (err) {
      console.error("Failed to refresh user:", err);
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register, loading, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
