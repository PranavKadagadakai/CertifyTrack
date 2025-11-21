import React, { useState, useEffect } from "react";
import api from "../api";

const AdminClubManagement = () => {
  const [clubs, setClubs] = useState([]);
  const [mentors, setMentors] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    faculty_coordinator: null,
    established_date: "",
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [clubsRes, mentorsRes, studentsRes] = await Promise.all([
        api.get("/admin/clubs/"),
        api.get("/admin/users/?user_type=mentor"),
        api.get("/students/"),
      ]);
      setClubs(clubsRes.data.results || clubsRes.data);
      setMentors(mentorsRes.data.results || mentorsRes.data);
      setStudents(studentsRes.data.results || studentsRes.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to load data");
      setLoading(false);
    }
  };

  const handleCreateClub = async (e) => {
    e.preventDefault();
    try {
      setError("");
      const payload = {
        name: formData.name,
        description: formData.description,
        faculty_coordinator: formData.faculty_coordinator || null,
        established_date: formData.established_date || null,
      };
      await api.post("/admin/clubs/", payload);
      setSuccess("Club created successfully!");
      setFormData({
        name: "",
        description: "",
        faculty_coordinator: null,
        established_date: "",
      });
      setShowCreateForm(false);
      fetchData();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create club");
    }
  };

  const handleAssignCoordinator = async (clubId, mentorId) => {
    try {
      await api.post(`/admin/clubs/${clubId}/assign_faculty_coordinator/`, {
        mentor_id: mentorId,
      });
      setSuccess("Faculty coordinator assigned successfully");
      fetchData();
    } catch (err) {
      setError("Failed to assign coordinator");
    }
  };

  const handleAssignHead = async (clubId, studentId) => {
    try {
      await api.post(`/admin/clubs/${clubId}/assign_club_head/`, {
        student_id: studentId,
      });
      setSuccess("Club head assigned successfully");
      fetchData();
    } catch (err) {
      setError("Failed to assign club head");
    }
  };

  if (loading) return <div className="text-center py-10">Loading clubs...</div>;

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

      {/* Create Club Button */}
      <div className="bg-white p-6 rounded-lg shadow">
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          ➕ Create Club
        </button>
      </div>

      {/* Create Form */}
      {showCreateForm && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Create New Club</h3>
          <form onSubmit={handleCreateClub} className="space-y-4">
            <input
              type="text"
              placeholder="Club Name"
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
              required
              className="w-full px-4 py-2 border rounded-lg"
            />
            <textarea
              placeholder="Description"
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              className="w-full px-4 py-2 border rounded-lg"
              rows="4"
            />
            <input
              type="date"
              value={formData.established_date}
              onChange={(e) =>
                setFormData({ ...formData, established_date: e.target.value })
              }
              className="w-full px-4 py-2 border rounded-lg"
            />
            <select
              value={formData.faculty_coordinator}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  faculty_coordinator: e.target.value,
                })
              }
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="">Select Faculty Coordinator (optional)</option>
              {mentors.map((mentor) => (
                <option key={mentor.id} value={mentor.id}>
                  {mentor.user_details?.first_name}{" "}
                  {mentor.user_details?.last_name}
                </option>
              ))}
            </select>
            <div className="flex gap-4">
              <button
                type="submit"
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                Create Club
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

      {/* Clubs List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {clubs.map((club) => (
          <div key={club.id} className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-bold mb-2">{club.name}</h3>
            <p className="text-gray-600 mb-4">{club.description}</p>
            <div className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-700">
                  Faculty Coordinator
                </label>
                <select
                  value={club.faculty_coordinator || ""}
                  onChange={(e) =>
                    handleAssignCoordinator(club.id, e.target.value)
                  }
                  className="w-full px-3 py-1 border rounded text-sm"
                >
                  <option value="">Select Mentor</option>
                  {mentors.map((mentor) => (
                    <option key={mentor.id} value={mentor.id}>
                      {mentor.user_details?.first_name}{" "}
                      {mentor.user_details?.last_name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">
                  Club Head
                </label>
                <select
                  value={club.club_head || ""}
                  onChange={(e) => handleAssignHead(club.id, e.target.value)}
                  className="w-full px-3 py-1 border rounded text-sm"
                >
                  <option value="">Select Student</option>
                  {students.map((student) => (
                    <option key={student.id} value={student.id}>
                      {student.user_details?.first_name}{" "}
                      {student.user_details?.last_name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="text-sm text-gray-600">
                <p>👥 Members: {club.members?.length || 0}</p>
                <p>📅 Established: {club.established_date || "N/A"}</p>
                <p>
                  Status:{" "}
                  <span
                    className={`px-2 py-1 rounded text-xs ${
                      club.is_active
                        ? "bg-green-100 text-green-800"
                        : "bg-red-100 text-red-800"
                    }`}
                  >
                    {club.is_active ? "Active" : "Inactive"}
                  </span>
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminClubManagement;
