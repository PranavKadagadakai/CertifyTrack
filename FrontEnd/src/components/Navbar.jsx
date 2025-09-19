import React from "react";
import { Link, NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { user, logout } = useAuth();

  const getDashboardLink = () => {
    if (!user) return "/";
    switch (user.profile.role) {
      case "student":
        return "/student-dashboard";
      case "club":
        return "/club-dashboard";
      case "mentor":
        return "/mentor-dashboard";
      default:
        return "/";
    }
  };

  return (
    <header className="bg-blue-600 text-white shadow-md">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/" className="text-xl font-bold">
          CertifyTrack
        </Link>
        <nav className="space-x-4 flex items-center">
          <NavLink
            to="/"
            className={({ isActive }) => (isActive ? "font-bold" : "")}
          >
            Home
          </NavLink>
          {user ? (
            <>
              <NavLink
                to={getDashboardLink()}
                className={({ isActive }) => (isActive ? "font-bold" : "")}
              >
                Dashboard
              </NavLink>
              <NavLink
                to="/profile"
                className={({ isActive }) => (isActive ? "font-bold" : "")}
              >
                Profile
              </NavLink>
              <button
                onClick={logout}
                className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <NavLink
                to="/login"
                className="bg-green-500 hover:bg-green-600 px-3 py-1 rounded"
              >
                Login
              </NavLink>
              <NavLink
                to="/signup"
                className="bg-gray-200 text-blue-600 hover:bg-gray-300 px-3 py-1 rounded"
              >
                Sign Up
              </NavLink>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
