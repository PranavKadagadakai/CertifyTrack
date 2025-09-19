// App.js
import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import StudentDashboard from "./pages/StudentDashboard";
import ClubDashboard from "./pages/ClubDashboard";
import MentorDashboard from "./pages/MentorDashboard";
import Navbar from "./components/Navbar";
import LandingPage from "./pages/LandingPage";
import ProfilePage from "./pages/ProfilePage"; // +++ Import ProfilePage

// ... PrivateRoute and HomeRedirect functions (no changes) ...
function PrivateRoute({ children, roles }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  if (roles && !roles.includes(user.profile.role))
    return <Navigate to="/unauthorized" />;
  return children;
}
function HomeRedirect() {
  const { user } = useAuth();
  if (!user) return <LandingPage />;
  switch (user.profile.role) {
    case "student":
      return <Navigate to="/student-dashboard" />;
    case "club":
      return <Navigate to="/club-dashboard" />;
    case "mentor":
      return <Navigate to="/mentor-dashboard" />;
    default:
      return <LandingPage />;
  }
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomeRedirect />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />

            <Route
              path="/student-dashboard"
              element={
                <PrivateRoute roles={["student"]}>
                  <StudentDashboard />
                </PrivateRoute>
              }
            />
            <Route
              path="/club-dashboard"
              element={
                <PrivateRoute roles={["club"]}>
                  <ClubDashboard />
                </PrivateRoute>
              }
            />
            <Route
              path="/mentor-dashboard"
              element={
                <PrivateRoute roles={["mentor"]}>
                  <MentorDashboard />
                </PrivateRoute>
              }
            />

            {/* +++ Add Profile Route +++ */}
            <Route
              path="/profile"
              element={
                <PrivateRoute>
                  <ProfilePage />
                </PrivateRoute>
              }
            />

            <Route
              path="/unauthorized"
              element={
                <div className="text-center">
                  <h1 className="text-2xl font-bold">Unauthorized Access</h1>
                </div>
              }
            />
          </Routes>
        </main>
      </Router>
    </AuthProvider>
  );
}

export default App;
