import React, { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import api from "../api";

const EmailVerificationPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [token, setToken] = useState("");
  const [manualToken, setManualToken] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    // Check if token is in URL
    const tokenFromUrl = searchParams.get("token");
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
      verifyEmail(tokenFromUrl);
    }
  }, [searchParams]);

  const verifyEmail = async (tokenToVerify) => {
    setLoading(true);
    setError("");
    try {
      const response = await api.post("/auth/verify-email/", {
        token: tokenToVerify,
      });
      setSuccess(true);
      setTimeout(() => {
        navigate("/login");
      }, 3000);
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Email verification failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleManualVerification = async (e) => {
    e.preventDefault();
    if (!manualToken.trim()) {
      setError("Please enter the verification token.");
      return;
    }
    await verifyEmail(manualToken);
  };

  const handleResendEmail = async (e) => {
    e.preventDefault();
    if (!email.trim()) {
      setError("Please enter your email address.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      await api.post("/auth/resend-verification/", { email });
      setEmail("");
      setError("");
      // Show success message
      setSuccess(false);
      alert("Verification email sent! Check your inbox.");
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Failed to resend verification email. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md p-8">
        <div className="text-center mb-6">
          <div className="text-5xl mb-4">{success ? "✅" : "📧"}</div>
          <h1 className="text-3xl font-bold text-gray-800">
            {success ? "Email Verified!" : "Verify Your Email"}
          </h1>
          <p className="text-gray-600 mt-2">
            {success
              ? "Your email has been successfully verified. Redirecting to login..."
              : "We've sent a verification link to your email address."}
          </p>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}

        {!success && (
          <>
            {/* Token from URL (automatic verification) */}
            {token && (
              <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg text-center">
                <p className="text-sm text-blue-800">
                  {loading
                    ? "Verifying your email..."
                    : "Token detected from email link"}
                </p>
              </div>
            )}

            {/* Manual token entry */}
            {!token && (
              <form
                onSubmit={handleManualVerification}
                className="space-y-4 mb-6"
              >
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Verification Token
                  </label>
                  <input
                    type="text"
                    value={manualToken}
                    onChange={(e) => setManualToken(e.target.value)}
                    placeholder="Paste your verification token here"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={loading}
                  />
                </div>
                <button
                  type="submit"
                  disabled={loading || !manualToken.trim()}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition disabled:bg-gray-400"
                >
                  {loading ? "Verifying..." : "Verify Email"}
                </button>
              </form>
            )}

            {/* Resend verification email */}
            <div className="border-t pt-6">
              <p className="text-sm text-gray-600 mb-3">
                Didn't receive the email?
              </p>
              <form onSubmit={handleResendEmail} className="space-y-3">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email address"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={loading || !email.trim()}
                  className="w-full bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded-lg transition disabled:bg-gray-400 text-sm"
                >
                  {loading ? "Sending..." : "Resend Verification Email"}
                </button>
              </form>
            </div>
          </>
        )}

        {success && (
          <div className="mt-6">
            <button
              onClick={() => navigate("/login")}
              className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition"
            >
              Go to Login
            </button>
          </div>
        )}

        <p className="text-xs text-center text-gray-500 mt-4">
          Problems verifying? Contact support@certifytrack.com
        </p>
      </div>
    </div>
  );
};

export default EmailVerificationPage;
