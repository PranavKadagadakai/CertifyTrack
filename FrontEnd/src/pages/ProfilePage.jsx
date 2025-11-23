import React, { useState, useEffect } from "react";
import api from "../api";
import { useAuth } from "../context/AuthContext";

function ProfilePage() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [profilePhoto, setProfilePhoto] = useState(null);
  const [photoPreview, setPhotoPreview] = useState(null);

  // Fetch profile on component mount
  useEffect(() => {
    if (user) {
      fetchProfile();
    }
  }, [user]);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const response = await api.get("/profile/");
      setProfile(response.data);
      // console.log("Fetched profile:", response.data);

      // Initialize form with existing data
      const data = { ...response.data };
      delete data.profile_completed_at;
      delete data.created_at;
      delete data.updated_at;
      setFormData(data);

      // Set photo preview if exists
      if (response.data.profile_photo) {
        setPhotoPreview(response.data.profile_photo);
      }
    } catch (err) {
      console.error("Failed to fetch profile:", err);
      setError("Failed to load profile. Please refresh the page.");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "number" ? parseInt(value) : value,
    }));
  };

  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setProfilePhoto(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhotoPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    setSuccess("");

    try {
      const submitData = new FormData();

      // Add all form fields
      Object.keys(formData).forEach((key) => {
        const value = formData[key];
        if (value !== null && value !== undefined && value !== "") {
          submitData.append(key, value);
        }
      });

      // Only add profile_photo if a new file is selected
      if (profilePhoto instanceof File) {
        submitData.append("profile_photo", profilePhoto);
      }

      const response = await api.patch("/profile/", submitData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setProfile(response.data);
      setSuccess("Profile updated successfully!");

      // Reset photo state
      setProfilePhoto(null);

      setTimeout(() => {
        setSuccess("");
      }, 2000);
    } catch (err) {
      console.error("Profile update failed:", err);
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          "Failed to update profile. Please try again."
      );
    } finally {
      setSaving(false);
    }
  };

  const getProfileCompletionMessage = () => {
    if (!profile) return null;

    if (profile.profile_completed) {
      return (
        <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          ✓ Your profile is complete!
        </div>
      );
    }

    return (
      <div className="mb-4 p-4 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded">
        ⚠ Please complete your profile to get full access to the platform.
      </div>
    );
  };

  const getRequiredFields = () => {
    if (!user) return [];

    switch (user.user_type) {
      case "student":
        return [
          "phone_number",
          "date_of_birth",
          "address",
          "emergency_contact_name",
          "emergency_contact_phone",
        ];
      case "mentor":
        return ["phone_number", "date_of_birth", "address", "qualifications"];
      case "club_organizer":
        return [
          "phone_number",
          "date_of_birth",
          "address",
          "designation_in_club",
        ];
      default:
        return [];
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading profile...</div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg text-red-600">Failed to load profile</div>
      </div>
    );
  }

  const requiredFields = getRequiredFields();

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">My Profile</h1>
          <p className="mt-2 text-gray-600">
            Manage your account information and preferences
          </p>
        </div>

        {/* Alerts */}
        {getProfileCompletionMessage()}
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}
        {success && (
          <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded">
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow">
          <div className="px-4 py-5 sm:p-6">
            {/* User Info (Read-only) */}
            <div className="mb-8 pb-8 border-b">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                Account Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Username
                  </label>
                  <input
                    type="text"
                    name="username"
                    value={formData.username || profile.user?.username || ""}
                    onChange={handleInputChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    First Name
                  </label>
                  <input
                    type="text"
                    name="first_name"
                    value={
                      formData.first_name || profile.user?.first_name || ""
                    }
                    onChange={handleInputChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Last Name
                  </label>
                  <input
                    type="text"
                    name="last_name"
                    value={formData.last_name || profile.user?.last_name || ""}
                    onChange={handleInputChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Email
                  </label>
                  <p className="mt-1 text-gray-900 font-medium">
                    {profile.user?.email}
                  </p>
                </div>
              </div>
            </div>

            {/* Profile Photo */}
            <div className="mb-8 pb-8 border-b">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                Profile Photo
              </h2>
              <div className="flex items-center gap-6">
                {photoPreview && (
                  <img
                    src={photoPreview}
                    alt="Profile preview"
                    className="w-24 h-24 rounded-full object-cover border-2 border-gray-300"
                  />
                )}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Upload Photo
                  </label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handlePhotoChange}
                    className="block w-full text-sm text-gray-500
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-md file:border-0
                      file:text-sm file:font-semibold
                      file:bg-blue-50 file:text-blue-700
                      hover:file:bg-blue-100"
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    JPG, PNG, GIF up to 5MB
                  </p>
                </div>
              </div>
            </div>

            {/* Role-Specific Profile Fields */}
            <div className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                Personal Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Phone Number */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Phone Number
                    {requiredFields.includes("phone_number") && (
                      <span className="text-red-500 ml-1">*</span>
                    )}
                  </label>
                  <input
                    type="tel"
                    name="phone_number"
                    value={formData.phone_number || ""}
                    onChange={handleInputChange}
                    placeholder="Enter your phone number"
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                {/* Date of Birth */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Date of Birth
                    {requiredFields.includes("date_of_birth") && (
                      <span className="text-red-500 ml-1">*</span>
                    )}
                  </label>
                  <input
                    type="date"
                    name="date_of_birth"
                    value={formData.date_of_birth || ""}
                    onChange={handleInputChange}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                {/* Address */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Address
                    {requiredFields.includes("address") && (
                      <span className="text-red-500 ml-1">*</span>
                    )}
                  </label>
                  <textarea
                    name="address"
                    value={formData.address || ""}
                    onChange={handleInputChange}
                    placeholder="Enter your address"
                    rows="3"
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                {/* Student-Specific Fields */}
                {user.user_type === "student" && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        USN
                      </label>
                      <p className="mt-1 text-gray-900 font-medium">
                        {profile.usn}
                      </p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Department
                      </label>
                      <p className="mt-1 text-gray-900 font-medium">
                        {profile.department}
                      </p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Semester
                      </label>
                      <p className="mt-1 text-gray-900 font-medium">
                        {profile.semester}
                      </p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Emergency Contact Name
                        <span className="text-red-500 ml-1">*</span>
                      </label>
                      <input
                        type="text"
                        name="emergency_contact_name"
                        value={formData.emergency_contact_name || ""}
                        onChange={handleInputChange}
                        placeholder="Enter emergency contact name"
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Emergency Contact Phone
                        <span className="text-red-500 ml-1">*</span>
                      </label>
                      <input
                        type="tel"
                        name="emergency_contact_phone"
                        value={formData.emergency_contact_phone || ""}
                        onChange={handleInputChange}
                        placeholder="Enter emergency contact phone"
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </>
                )}

                {/* Mentor-Specific Fields */}
                {user.user_type === "mentor" && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Employee ID
                      </label>
                      <p className="mt-1 text-gray-900 font-medium">
                        {profile.employee_id}
                      </p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Department
                      </label>
                      <p className="mt-1 text-gray-900 font-medium">
                        {profile.department}
                      </p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Designation
                      </label>
                      <p className="mt-1 text-gray-900 font-medium">
                        {profile.designation}
                      </p>
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700">
                        Qualifications
                        <span className="text-red-500 ml-1">*</span>
                      </label>
                      <textarea
                        name="qualifications"
                        value={formData.qualifications || ""}
                        onChange={handleInputChange}
                        placeholder="Enter your qualifications (e.g., B.Tech, M.Tech, Ph.D)"
                        rows="3"
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700">
                        Bio
                      </label>
                      <textarea
                        name="bio"
                        value={formData.bio || ""}
                        onChange={handleInputChange}
                        placeholder="Tell us about yourself"
                        rows="3"
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </>
                )}

                {/* Club Organizer-Specific Fields */}
                {user.user_type === "club_organizer" && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">
                        Designation in Club
                        <span className="text-red-500 ml-1">*</span>
                      </label>
                      <input
                        type="text"
                        name="designation_in_club"
                        value={formData.designation_in_club || ""}
                        onChange={handleInputChange}
                        placeholder="e.g., President, Secretary, Treasurer"
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700">
                        Bio
                      </label>
                      <textarea
                        name="bio"
                        value={formData.bio || ""}
                        onChange={handleInputChange}
                        placeholder="Tell us about yourself"
                        rows="3"
                        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* Form Actions */}
            <div className="flex gap-4">
              <button
                type="submit"
                disabled={saving}
                className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition"
              >
                {saving ? "Saving..." : "Save Changes"}
              </button>
              <button
                type="button"
                onClick={fetchProfile}
                className="px-6 py-2 bg-gray-300 text-gray-800 font-semibold rounded-lg hover:bg-gray-400 transition"
              >
                Cancel
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ProfilePage;
