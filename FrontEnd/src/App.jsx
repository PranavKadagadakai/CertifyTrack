// FrontEnd/src/App.jsx
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import EmailVerificationPage from "./pages/EmailVerificationPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import StudentDashboard from "./pages/StudentDashboard";
import MentorDashboard from "./pages/MentorDashboard";
import ClubDashboard from "./pages/ClubDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import ProfilePage from "./pages/ProfilePage";

const App = () => {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;

  const PrivateRoute = ({ children, userType }) => {
    if (!user) return <Navigate to="/login" />;
    // backend uses user.user_type (student, mentor, club_organizer, admin)
    if (userType && user.user_type !== userType)
      return <Navigate to="/dashboard" />;
    return children;
  };

  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/verify-email" element={<EmailVerificationPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              {user?.user_type === "student" && <StudentDashboard />}
              {user?.user?.user_type === "mentor" && <MentorDashboard />}
              {user?.user?.user_type === "club_organizer" && <ClubDashboard />}
              {user?.user_type === "admin" && <AdminDashboard />}
              {/* default fallback: show student dashboard if unknown */}
              {!["student", "mentor", "club_organizer", "admin"].includes(
                user?.user_type
              ) && <StudentDashboard />}
            </PrivateRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <PrivateRoute>
              <ProfilePage />
            </PrivateRoute>
          }
        />
      </Routes>
    </>
  );
};

export default App;
