import React, { useState, useEffect } from "react";
import api from "../api";

const ClubCoordinatorSignature = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [signatureFile, setSignatureFile] = useState(null);
  const [signaturePreview, setSignaturePreview] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const response = await api.get("/profile/");
      setProfile(response.data);
      if (response.data.signature) {
        setSignaturePreview(response.data.signature);
      }
    } catch (err) {
      console.error("Failed to fetch profile:", err);
      setError("Failed to load signature information");
    } finally {
      setLoading(false);
    }
  };

  const handleSignatureChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      const allowedTypes = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/gif",
      ];
      if (!allowedTypes.includes(file.type)) {
        setError("Please upload a valid image file (JPEG, PNG, or GIF).");
        return;
      }

      // Validate file size (5MB limit)
      const maxSize = 5 * 1024 * 1024; // 5MB in bytes
      if (file.size > maxSize) {
        setError("File size must be less than 5MB.");
        return;
      }

      setSignatureFile(file);
      setError("");

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setSignaturePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    if (!signatureFile) {
      setError("Please select a signature file to upload.");
      return;
    }

    setUploading(true);
    setError("");
    setSuccess("");

    try {
      const formData = new FormData();
      formData.append("signature", signatureFile);

      const response = await api.patch("/profile/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setProfile(response.data);
      setSuccess("Signature uploaded successfully!");
      setSignatureFile(null);

      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccess("");
      }, 3000);
    } catch (err) {
      console.error("Upload failed:", err);
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          err.response?.data?.signature?.[0] ||
          "Failed to upload signature. Please try again."
      );
    } finally {
      setUploading(false);
    }
  };

  const handleRemove = async () => {
    setUploading(true);
    setError("");
    setSuccess("");

    try {
      const formData = new FormData();
      formData.append("signature", null);

      const response = await api.patch("/profile/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setProfile(response.data);
      setSignaturePreview(null);
      setSignatureFile(null);
      setSuccess("Signature removed successfully!");
    } catch (err) {
      console.error("Remove failed:", err);
      setError("Failed to remove signature. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Digital Signature
        </h2>
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
          <p className="text-gray-600 mt-2">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="flex items-center gap-2 mb-4">
        <svg
          className="h-6 w-6 text-gray-600"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <h2 className="text-xl font-bold text-gray-900">Digital Signature</h2>
      </div>

      <p className="text-gray-600 mb-6">
        Upload your digital signature for use in certificate generation. This
        signature will be used on certificates for events where you are the
        faculty coordinator.
      </p>

      <div className="space-y-4">
        {/* Current Signature Status */}
        {signaturePreview && !signatureFile ? (
          <div className="flex items-center gap-4 p-4 border border-gray-200 rounded-lg">
            <div className="flex-shrink-0">
              <div className="w-16 h-16 border border-gray-300 rounded bg-gray-50 flex items-center justify-center">
                <svg
                  className="h-8 w-8 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">
                Signature Uploaded
              </p>
              <p className="text-xs text-gray-600">
                Your signature is ready for use in certificate generation
              </p>
            </div>
          </div>
        ) : (
          <div className="flex items-center gap-4 p-4 border-2 border-dashed border-gray-300 rounded-lg">
            <div className="flex-shrink-0">
              <svg
                className="h-12 w-12 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">
                No Signature Uploaded
              </p>
              <p className="text-xs text-gray-600">
                Upload a signature image to enable certificate generation
              </p>
            </div>
          </div>
        )}

        {/* Signature Preview */}
        {signaturePreview && (
          <div className="flex items-center justify-center p-4 border border-gray-200 rounded-lg bg-gray-50">
            <div className="text-center">
              <img
                src={signaturePreview}
                alt="Signature preview"
                className="max-w-xs max-h-20 object-contain border border-gray-300 rounded bg-white p-2"
              />
              <p className="text-xs text-gray-600 mt-2">
                {signatureFile ? "New signature preview" : "Current signature"}
              </p>
            </div>
          </div>
        )}

        {/* File Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Upload Signature Image
          </label>
          <input
            type="file"
            accept="image/*"
            onChange={handleSignatureChange}
            disabled={uploading}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-50"
          />
          <p className="mt-1 text-xs text-gray-500">PNG, JPEG, GIF up to 5MB</p>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          {signatureFile && (
            <>
              <button
                onClick={handleUpload}
                disabled={uploading}
                className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {uploading ? "Uploading..." : "Upload Signature"}
              </button>
              <button
                onClick={() => {
                  setSignatureFile(null);
                  setSignaturePreview(profile?.signature || null);
                  setError("");
                }}
                disabled={uploading}
                className="px-4 py-2 bg-gray-300 text-gray-800 text-sm font-medium rounded-md hover:bg-gray-400 disabled:opacity-50 transition-colors"
              >
                Cancel
              </button>
            </>
          )}

          {signaturePreview && !signatureFile && (
            <button
              onClick={handleRemove}
              disabled={uploading}
              className="px-4 py-2 bg-red-600 text-white text-sm font-medium rounded-md hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {uploading ? "Removing..." : "Remove Signature"}
            </button>
          )}
        </div>

        {/* Messages */}
        {error && (
          <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded-md text-sm">
            {error}
          </div>
        )}

        {success && (
          <div className="p-3 bg-green-100 border border-green-400 text-green-700 rounded-md text-sm">
            {success}
          </div>
        )}
      </div>
    </div>
  );
};

export default ClubCoordinatorSignature;
