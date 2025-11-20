// FrontEnd/src/api.js
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  timeout: 10000, // 10s timeout for requests (helpful during dev)
});

// request interceptor: add Bearer token if we have one
api.interceptors.request.use(
  (config) => {
    const access = localStorage.getItem("access");
    if (access) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${access}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// response interceptor: simple centralized error logging
api.interceptors.response.use(
  (res) => res,
  (error) => {
    // optional: more advanced handling (refresh tokens, redirect on 401) can be added
    console.error(
      "API error:",
      error?.response?.status,
      error?.response?.data || error
    );
    return Promise.reject(error);
  }
);

export default api;
