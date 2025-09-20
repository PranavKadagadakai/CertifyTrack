import React, { useState, useEffect } from "react";
import api from "../api";
import { useAuth } from "../context/AuthContext";

function ProfilePage() {
  const { user, setUser } = useAuth();
  const [profile, setProfile] = useState({ full_name: "", usn: "" });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      api
        .get("/profile/")
        .then((res) => {
          setProfile(res.data);
          setLoading(false);
        })
        .catch((err) => console.error(err));
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    api
      .patch("/profile/", { full_name: profile.full_name, usn: profile.usn })
      .then((res) => {
        setProfile(res.data);
        // Optionally update user context
        setUser((prev) => ({
          ...prev,
          profile: { ...prev.profile, ...res.data },
        }));
        alert("Profile updated successfully!");
      })
      .catch((err) => alert("Failed to update profile."));
  };

  if (loading) return <p>Loading profile...</p>;

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Your Profile</h1>
      <div className="p-6 bg-white rounded-lg shadow">
        <p className="mb-2">
          <strong>Username:</strong> {user.username}
        </p>
        <p className="mb-4">
          <strong>Email:</strong> {user.email}
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Full Name</label>
            <input
              type="text"
              name="full_name"
              value={profile.full_name || ""}
              onChange={handleChange}
              className="w-full px-3 py-2 mt-1 border rounded-md"
            />
          </div>
          {user.profile?.role === "student" && (
            <div>
              <label className="block text-sm font-medium">USN</label>
              <input
                type="text"
                name="usn"
                value={profile.usn || ""}
                onChange={handleChange}
                className="w-full px-3 py-2 mt-1 border rounded-md"
              />
            </div>
          )}
          <button
            type="submit"
            className="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700"
          >
            Save Changes
          </button>
        </form>
      </div>
    </div>
  );
}

export default ProfilePage;
