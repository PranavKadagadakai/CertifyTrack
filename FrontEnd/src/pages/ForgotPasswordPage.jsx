import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";

const ForgotPasswordPage = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1); // 1: request OTP, 2: enter OTP & new password
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const validatePassword = (pwd) => {
    if (pwd.length < 8) {
      return "Password must be at least 8 characters long.";
    }
    return "";
  };

  const handleRequestOTP = async (e) => {
    e.preventDefault();
    if (!email.trim()) {
      setError("Please enter your email address.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      await api.post("/auth/password-reset/request/", { email });
      setSuccess("OTP sent to your email! Check your inbox.");
      setTimeout(() => {
        setStep(2);
        setSuccess("");
      }, 2000);
    } catch (err) {
      setError(
        err.response?.data?.error || "Failed to send OTP. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError("");

    // Validate inputs
    if (!otp.trim()) {
      setError("Please enter the OTP.");
      return;
    }

    if (!newPassword.trim()) {
      setError("Please enter a new password.");
      return;
    }

    const pwdError = validatePassword(newPassword);
    if (pwdError) {
      setError(pwdError);
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      await api.post("/auth/password-reset/confirm/", {
        email,
        otp,
        new_password: newPassword,
      });
      setSuccess("Password reset successfully! Redirecting to login...");
      setTimeout(() => {
        navigate("/login");
      }, 2000);
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Failed to reset password. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = (e) => {
    const pwd = e.target.value;
    setNewPassword(pwd);
    if (pwd) {
      setPasswordError(validatePassword(pwd));
    } else {
      setPasswordError("");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md p-8">
        <div className="text-center mb-6">
          <div className="text-5xl mb-4">🔐</div>
          <h1 className="text-3xl font-bold text-gray-800">Reset Password</h1>
          <p className="text-gray-600 mt-2">
            {step === 1
              ? "Enter your email to receive a reset code"
              : "Enter the code and your new password"}
          </p>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg text-sm">
            {success}
          </div>
        )}

        {step === 1 ? (
          <form onSubmit={handleRequestOTP} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading || !email.trim()}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition disabled:bg-gray-400"
            >
              {loading ? "Sending OTP..." : "Send Reset Code"}
            </button>
          </form>
        ) : (
          <form onSubmit={handleResetPassword} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                OTP Code
              </label>
              <input
                type="text"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="Enter 6-digit code from email"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
                required
                maxLength="6"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                New Password
              </label>
              <input
                type="password"
                value={newPassword}
                onChange={handlePasswordChange}
                placeholder="Minimum 8 characters"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
                required
              />
              {passwordError && (
                <p className="text-red-500 text-sm mt-1">{passwordError}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Confirm Password
              </label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Re-enter your password"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
                required
              />
              {newPassword &&
                confirmPassword &&
                newPassword !== confirmPassword && (
                  <p className="text-red-500 text-sm mt-1">
                    Passwords do not match
                  </p>
                )}
            </div>

            <button
              type="submit"
              disabled={loading || !otp.trim() || !newPassword.trim()}
              className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition disabled:bg-gray-400"
            >
              {loading ? "Resetting Password..." : "Reset Password"}
            </button>

            <button
              type="button"
              onClick={() => {
                setStep(1);
                setOtp("");
                setNewPassword("");
                setConfirmPassword("");
                setError("");
              }}
              className="w-full mt-2 bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-lg transition"
            >
              Back
            </button>
          </form>
        )}

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Remember your password?{" "}
            <Link
              to="/login"
              className="text-blue-600 hover:underline font-semibold"
            >
              Login
            </Link>
          </p>
          <p className="text-sm text-gray-600 mt-2">
            Don't have an account?{" "}
            <Link
              to="/signup"
              className="text-blue-600 hover:underline font-semibold"
            >
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;
