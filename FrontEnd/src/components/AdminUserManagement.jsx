import React, { useState, useEffect } from "react";
import api from "../api";

const AdminUserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [filterType, setFilterType] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    user_type: "student",
    usn: "",
    semester: 1,
    department: "",
    employee_id: "",
    designation: "",
  });
  const [resetPasswordForm, setResetPasswordForm] = useState({
    userId: null,
    newPassword: "",
  });

  useEffect(() => {
    fetchUsers();
  }, [filterType, searchTerm]);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      let url = "/admin/users/";
      const params = new URLSearchParams();
      if (filterType) params.append("user_type", filterType);
      if (searchTerm) params.append("search", searchTerm);
      if (params.toString()) url += `?${params.toString()}`;

      const response = await api.get(url);
      setUsers(response.data.results || response.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to load users");
      setLoading(false);
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      setError("");
      setSuccess("");

      const payload = {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        first_name: formData.first_name,
        last_name: formData.last_name,
        user_type: formData.user_type,
      };

      if (formData.user_type === "student") {
        payload.usn = formData.usn;
        payload.semester = parseInt(formData.semester);
        payload.department = formData.department;
      } else if (formData.user_type === "mentor") {
        payload.employee_id = formData.employee_id;
        payload.designation = formData.designation;
        payload.department = formData.department;
      }

      await api.post("/admin/users/create/", payload);
      setSuccess("User created successfully!");
      setFormData({
        username: "",
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        user_type: "student",
        usn: "",
        semester: 1,
        department: "",
        employee_id: "",
        designation: "",
      });
      setShowCreateForm(false);
      fetchUsers();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create user");
    }
  };

  const handleDisableAccount = async (userId) => {
    if (window.confirm("Are you sure you want to disable this account?")) {
      try {
        await api.post(`/admin/users/${userId}/disable_account/`);
        setSuccess("Account disabled successfully");
        fetchUsers();
      } catch (err) {
        setError("Failed to disable account");
      }
    }
  };

  const handleEnableAccount = async (userId) => {
    try {
      await api.post(`/admin/users/${userId}/enable_account/`);
      setSuccess("Account enabled successfully");
      fetchUsers();
    } catch (err) {
      setError("Failed to enable account");
    }
  };

  const handleResetPassword = async (userId) => {
    if (
      !resetPasswordForm.newPassword ||
      resetPasswordForm.newPassword.length < 8
    ) {
      setError("Password must be at least 8 characters");
      return;
    }

    try {
      await api.post(`/admin/users/${userId}/reset_password/`, {
        new_password: resetPasswordForm.newPassword,
      });
      setSuccess("Password reset successfully");
      setResetPasswordForm({ userId: null, newPassword: "" });
      fetchUsers();
    } catch (err) {
      setError("Failed to reset password");
    }
  };

  const handleUnlockAccount = async (userId) => {
    try {
      await api.post(`/admin/users/${userId}/unlock_account/`);
      setSuccess("Account unlocked successfully");
      fetchUsers();
    } catch (err) {
      setError("Failed to unlock account");
    }
  };

  if (loading) return <div className="text-center py-10">Loading users...</div>;

  return (
    <div className="space-y-6">
      {error && (
        <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      {success && (
        <div className="p-4 bg-green-100 border border-green-400 text-green-700 rounded">
          {success}
        </div>
      )}

      {/* Controls */}
      <div className="bg-white p-6 rounded-lg shadow space-y-4">
        <div className="flex flex-wrap gap-4">
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            ➕ Create User
          </button>
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All User Types</option>
            <option value="student">Student</option>
            <option value="mentor">Mentor</option>
            <option value="club_organizer">Club Organizer</option>
            <option value="admin">Admin</option>
          </select>
          <input
            type="text"
            placeholder="Search by username or email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 min-w-[250px] px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Create Form */}
      {showCreateForm && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Create New User</h3>
          <form onSubmit={handleCreateUser} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Username"
                value={formData.username}
                onChange={(e) =>
                  setFormData({ ...formData, username: e.target.value })
                }
                required
                className="px-4 py-2 border rounded-lg"
              />
              <input
                type="email"
                placeholder="Email"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                required
                className="px-4 py-2 border rounded-lg"
              />
              <input
                type="password"
                placeholder="Password (min 8 chars)"
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
                required
                className="px-4 py-2 border rounded-lg"
              />
              <input
                type="text"
                placeholder="First Name"
                value={formData.first_name}
                onChange={(e) =>
                  setFormData({ ...formData, first_name: e.target.value })
                }
                className="px-4 py-2 border rounded-lg"
              />
              <input
                type="text"
                placeholder="Last Name"
                value={formData.last_name}
                onChange={(e) =>
                  setFormData({ ...formData, last_name: e.target.value })
                }
                className="px-4 py-2 border rounded-lg"
              />
              <select
                value={formData.user_type}
                onChange={(e) =>
                  setFormData({ ...formData, user_type: e.target.value })
                }
                className="px-4 py-2 border rounded-lg"
              >
                <option value="student">Student</option>
                <option value="mentor">Mentor</option>
                <option value="club_organizer">Club Organizer</option>
              </select>
            </div>

            {/* Conditional fields based on user type */}
            {formData.user_type === "student" && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="USN"
                  value={formData.usn}
                  onChange={(e) =>
                    setFormData({ ...formData, usn: e.target.value })
                  }
                  required
                  className="px-4 py-2 border rounded-lg"
                />
                <select
                  value={formData.department}
                  onChange={(e) =>
                    setFormData({ ...formData, department: e.target.value })
                  }
                  required
                  className="px-4 py-2 border rounded-lg"
                >
                  <option value="">Select Department</option>
                  <option value="CSE">CSE</option>
                  <option value="ECE">ECE</option>
                  <option value="ME">ME</option>
                </select>
                <input
                  type="number"
                  placeholder="Semester"
                  min="1"
                  max="8"
                  value={formData.semester}
                  onChange={(e) =>
                    setFormData({ ...formData, semester: e.target.value })
                  }
                  className="px-4 py-2 border rounded-lg"
                />
              </div>
            )}

            {formData.user_type === "mentor" && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="Employee ID"
                  value={formData.employee_id}
                  onChange={(e) =>
                    setFormData({ ...formData, employee_id: e.target.value })
                  }
                  required
                  className="px-4 py-2 border rounded-lg"
                />
                <input
                  type="text"
                  placeholder="Designation"
                  value={formData.designation}
                  onChange={(e) =>
                    setFormData({ ...formData, designation: e.target.value })
                  }
                  required
                  className="px-4 py-2 border rounded-lg"
                />
                <select
                  value={formData.department}
                  onChange={(e) =>
                    setFormData({ ...formData, department: e.target.value })
                  }
                  required
                  className="px-4 py-2 border rounded-lg"
                >
                  <option value="">Select Department</option>
                  <option value="CSE">CSE</option>
                  <option value="ECE">ECE</option>
                  <option value="ME">ME</option>
                </select>
              </div>
            )}

            <div className="flex gap-4">
              <button
                type="submit"
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                Create User
              </button>
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="px-6 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Users Table */}
      <div className="bg-white rounded-lg shadow overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-100 border-b">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-bold">
                Username
              </th>
              <th className="px-6 py-3 text-left text-sm font-bold">Email</th>
              <th className="px-6 py-3 text-left text-sm font-bold">Type</th>
              <th className="px-6 py-3 text-left text-sm font-bold">Status</th>
              <th className="px-6 py-3 text-left text-sm font-bold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-3">{user.username}</td>
                <td className="px-6 py-3">{user.email}</td>
                <td className="px-6 py-3">
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                    {user.user_type}
                  </span>
                </td>
                <td className="px-6 py-3">
                  <span
                    className={`px-3 py-1 rounded-full text-xs ${
                      user.is_active
                        ? "bg-green-100 text-green-800"
                        : "bg-red-100 text-red-800"
                    }`}
                  >
                    {user.is_active ? "Active" : "Inactive"}
                  </span>
                </td>
                <td className="px-6 py-3 space-x-2">
                  {user.is_active ? (
                    <button
                      onClick={() => handleDisableAccount(user.id)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Disable
                    </button>
                  ) : (
                    <button
                      onClick={() => handleEnableAccount(user.id)}
                      className="text-green-600 hover:text-green-800 text-sm"
                    >
                      Enable
                    </button>
                  )}
                  <button
                    onClick={() =>
                      setResetPasswordForm({
                        ...resetPasswordForm,
                        userId: user.id,
                      })
                    }
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    Reset Password
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Reset Password Modal */}
      {resetPasswordForm.userId && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
            <h3 className="text-lg font-bold mb-4">Reset Password</h3>
            <input
              type="password"
              placeholder="New Password (min 8 chars)"
              value={resetPasswordForm.newPassword}
              onChange={(e) =>
                setResetPasswordForm({
                  ...resetPasswordForm,
                  newPassword: e.target.value,
                })
              }
              className="w-full px-4 py-2 border rounded-lg mb-4"
            />
            <div className="flex gap-4">
              <button
                onClick={() => handleResetPassword(resetPasswordForm.userId)}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Reset
              </button>
              <button
                onClick={() =>
                  setResetPasswordForm({ userId: null, newPassword: "" })
                }
                className="flex-1 px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminUserManagement;
