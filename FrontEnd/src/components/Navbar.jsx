import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api";
import bellIcon from "../assets/bell.svg";
import bellExclamationIcon from "../assets/bell-exclamation.svg";

const Navbar = () => {
  const { user, logout } = useAuth();
  const [unreadNotifications, setUnreadNotifications] = useState(0);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const navigate = useNavigate();

  // Fetch unread notifications count
  useEffect(() => {
    const fetchUnreadNotifications = async () => {
      if (!user) return;
      try {
        const response = await api.get("/notifications/");
        const notifications = Array.isArray(response.data) ? response.data : [];
        const unreadCount = notifications.filter((n) => !n.is_read).length;
        setUnreadNotifications(unreadCount);
      } catch (error) {
        console.error("Failed to fetch notifications count:", error);
      }
    };

    fetchUnreadNotifications();
  }, [user]);

  const handleBellClick = () => {
    navigate("/notifications");
  };

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        {user ? (
          <Link to="/dashboard" className="text-lg font-bold">
            CertifyTrack
          </Link>
        ) : (
          <Link to="/" className="text-lg font-bold">
            CertifyTrack
          </Link>
        )}
        <div className="flex items-center space-x-4">
          {user ? (
            <>
              {/* Notification Bell */}
              <div className="relative">
                <button
                  onClick={handleBellClick}
                  className="relative p-2 hover:bg-gray-700 rounded-full transition-colors flex items-center justify-center"
                >
                  <img
                    src={
                      unreadNotifications > 0 ? bellExclamationIcon : bellIcon
                    }
                    alt="Notifications"
                    className="w-6 h-6 filter brightness-0 invert"
                  />
                  {unreadNotifications > 0 && (
                    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
                      {unreadNotifications > 9 ? "9+" : unreadNotifications}
                    </span>
                  )}
                </button>
              </div>

              {/* Profile Image with Dropdown */}
              <div className="relative">
                <button
                  onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                  className="flex items-center space-x-2 p-1 hover:bg-gray-700 rounded-full transition-colors"
                >
                  <img
                    src={
                      user.profile_photo ||
                      "data:image/svg+xml;base64,PC9zdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSI+CjxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgc3Ryb2tlLXdpZHRoPSIyIiBkPSJNMTkgN2g0YTEgMSAwIDAxLTcgMWgtNGEyIDItMSAwMS0yLTJ2ME0wIDl2NmEzIDMgMCAwMTMtM2gxNGEzIDMgMCAwMTMgM3YtNmEyIDItMSAwMS0yLTJoLTE1YTIgMiAwIDAxMi0yIi8+Cjwvc3ZnPg=="
                    }
                    alt="Profile"
                    className="w-8 h-8 rounded-full object-cover border-2 border-gray-400"
                  />
                </button>

                {/* Dropdown Menu */}
                {isDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                    <Link
                      to="/profile"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      onClick={() => setIsDropdownOpen(false)}
                    >
                      <div className="flex items-center">
                        <svg
                          className="w-4 h-4 mr-2"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                          />
                        </svg>
                        Profile
                      </div>
                    </Link>
                    <button
                      onClick={() => {
                        setIsDropdownOpen(false);
                        logout();
                      }}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      <div className="flex items-center">
                        <svg
                          className="w-4 h-4 mr-2"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                          />
                        </svg>
                        Logout
                      </div>
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="space-x-4">
              <Link to="/login" className="text-white hover:text-gray-300">
                Login
              </Link>
              <Link
                to="/signup"
                className="bg-blue-600 px-4 py-2 rounded hover:bg-blue-700"
              >
                Signup
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
