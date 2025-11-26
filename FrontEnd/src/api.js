// FrontEnd/src/api.js
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  timeout: 20000, // 20s timeout for requests (helpful during dev)
});

// Flag to prevent multiple simultaneous refresh attempts
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });

  failedQueue = [];
};

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

// response interceptor: handle token refresh on 401 errors
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't already tried to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // If refresh is in progress, queue the request
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch((err) => {
            return Promise.reject(err);
          });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = localStorage.getItem("refresh");
      if (refreshToken) {
        try {
          // Attempt to refresh the token
          const response = await axios.post(
            `${
              import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api"
            }/auth/token/refresh/`,
            { refresh: refreshToken }
          );

          const newAccessToken = response.data.access;
          localStorage.setItem("access", newAccessToken);

          // Update the token in the failed request and retry
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

          processQueue(null, newAccessToken);
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, clear tokens and reject
          localStorage.removeItem("access");
          localStorage.removeItem("refresh");
          processQueue(refreshError, null);

          // Optionally redirect to login (can be handled by calling component)
          window.location.href = "/login";

          return Promise.reject(refreshError);
        } finally {
          isRefreshing = false;
        }
      } else {
        // No refresh token, reject immediately
        return Promise.reject(error);
      }
    }

    // Log other errors
    console.error(
      "API error:",
      error?.response?.status,
      error?.response?.data || error
    );
    return Promise.reject(error);
  }
);

export default api;
