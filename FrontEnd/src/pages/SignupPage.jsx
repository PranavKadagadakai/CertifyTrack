import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const SignupPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    password_confirm: "",
    firstName: "",
    lastName: "",
    role: "",
    usn: "",
    department: "",
    semester: 1,
    employee_id: "",
    designation: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const { register } = useAuth();

  const departments = [
    "CSE",
    "AIML",
    "ISE",
    "ECE",
    "EEE",
    "ME",
    "Civil",
    "Aero",
    "Arch",
  ];
  const roles = ["student", "mentor", "club_organizer"];

  const validatePassword = (pwd) => {
    if (pwd.length < 8) {
      return "Password must be at least 8 characters long.";
    }
    return "";
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });

    // Validate password on change
    if (name === "password") {
      setPasswordError(validatePassword(value));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    // Validate passwords match
    if (formData.password !== formData.password_confirm) {
      return setError("Passwords do not match.");
    }

    // Validate password strength
    const pwdError = validatePassword(formData.password);
    if (pwdError) {
      return setError(pwdError);
    }

    // Validate student fields
    if (formData.role === "student") {
      if (!formData.usn.trim())
        return setError("USN is required for students.");
      if (!formData.department)
        return setError("Please select a valid department.");
      if (formData.semester < 1 || formData.semester > 8)
        return setError("Semester must be between 1 and 8.");
    }

    // Validate mentor fields
    if (formData.role === "mentor") {
      if (!formData.employee_id.trim())
        return setError("Employee ID is required for mentors.");
      if (!formData.department)
        return setError("Please select a valid department.");
      if (!formData.designation.trim())
        return setError("Designation is required for mentors.");
    }

    try {
      await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        password_confirm: formData.password_confirm,
        user_type: formData.role,
        first_name: formData.firstName,
        last_name: formData.lastName,
        ...(formData.role === "student" && {
          usn: formData.usn,
          department: formData.department,
          semester: parseInt(formData.semester),
        }),
        ...(formData.role === "mentor" && {
          employee_id: formData.employee_id,
          department: formData.department,
          designation: formData.designation,
        }),
      });

      setSuccess(
        "Registration successful! Redirecting to email verification..."
      );
      setTimeout(() => navigate("/verify-email"), 1100);
    } catch (err) {
      const errorData = err.response?.data;
      if (errorData?.usn) {
        setError("USN already exists.");
      } else if (errorData?.email) {
        setError("Email already registered.");
      } else if (errorData?.error) {
        setError(errorData.error);
      } else if (typeof errorData === "object") {
        const firstError = Object.values(errorData)[0];
        setError(
          Array.isArray(firstError)
            ? firstError[0]
            : firstError || "Registration failed."
        );
      } else {
        setError("Registration failed. Please try again.");
      }
    }
  };

  return (
    <div className="flex items-center justify-center min-h-[90vh] bg-gray-100">
      <div className="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center">Create an Account</h2>
        {error && <p className="text-red-500 text-center text-sm">{error}</p>}
        {success && <p className="text-green-500 text-center">{success}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 mt-1 border rounded-md"
            />
          </div>
          <div className="grid grid-cols-2 gap-1">
            <div>
              <label className="block text-sm font-medium">First Name</label>
              <input
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                required
                className="w-45 px-1 py-2 mt-1 border rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Last Name</label>
              <input
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                required
                className="w-45 px-1 py-2 mt-1 border rounded-md"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 mt-1 border rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Minimum 8 characters"
              className="w-full px-3 py-2 mt-1 border rounded-md"
            />
            {passwordError && (
              <p className="text-red-500 text-sm mt-1">{passwordError}</p>
            )}
          </div>
          <div>
            <label className="block text-sm font-medium">
              Confirm Password
            </label>
            <input
              type="password"
              name="password_confirm"
              value={formData.password_confirm}
              onChange={handleChange}
              required
              placeholder="Re-enter your password"
              className="w-full px-3 py-2 mt-1 border rounded-md"
            />
            {formData.password &&
              formData.password_confirm &&
              formData.password !== formData.password_confirm && (
                <p className="text-red-500 text-sm mt-1">
                  Passwords do not match.
                </p>
              )}
          </div>
          <div>
            <label className="block text-sm font-medium">Role</label>
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              className="w-full px-3 py-2 mt-1 border rounded-md"
            >
              <option value="">Select Role</option>
              {roles.map((role) => (
                <option key={role} value={role}>
                  {role}
                </option>
              ))}
            </select>
          </div>

          {/* Student extra fields */}
          {formData.role === "student" && (
            <>
              <div>
                <label className="block text-sm font-medium">USN</label>
                <input
                  type="text"
                  name="usn"
                  value={formData.usn}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 mt-1 border rounded-md"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-sm font-medium">
                    Department
                  </label>
                  <select
                    name="department"
                    value={formData.department}
                    onChange={handleChange}
                    required
                    className="w-45 px-1 py-3 mt-1 border rounded-md"
                  >
                    <option value="">Select Department</option>
                    {departments.map((dep) => (
                      <option key={dep} value={dep}>
                        {dep}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium">Semester</label>
                  <input
                    type="number"
                    name="semester"
                    value={formData.semester}
                    onChange={handleChange}
                    min={1}
                    max={8}
                    required
                    className="w-45 px-1 py-2 mt-1 border rounded-md"
                  />
                </div>
              </div>
            </>
          )}

          {formData.role === "mentor" && (
            <>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-sm font-medium">
                    Employee ID
                  </label>
                  <input
                    type="text"
                    name="employee_id"
                    value={formData.employee_id}
                    onChange={handleChange}
                    required
                    className="w-45 px-3 py-2 mt-1 border rounded-md"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium">
                    Department
                  </label>
                  <select
                    name="department"
                    value={formData.department}
                    onChange={handleChange}
                    required
                    className="w-45 px-3 py-3 mt-1 border rounded-md"
                  >
                    <option value="">Select Department</option>
                    {departments.map((dep) => (
                      <option key={dep} value={dep}>
                        {dep}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium">Designation</label>
                <input
                  type="text"
                  name="designation"
                  value={formData.designation}
                  onChange={handleChange}
                  required
                  placeholder="e.g., Professor, Assistant Professor"
                  className="w-full px-3 py-2 mt-1 border rounded-md"
                />
              </div>
            </>
          )}

          {formData.role === "club_organizer" && (
            <p className="text-sm text-gray-600 bg-blue-50 p-3 rounded">
              You can complete your club organizer profile after email
              verification.
            </p>
          )}

          <button
            type="submit"
            className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700"
          >
            Sign Up
          </button>
        </form>
        <p className="text-sm text-center">
          Already have an account?{" "}
          <Link to="/login" className="text-blue-600 hover:underline">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default SignupPage;
