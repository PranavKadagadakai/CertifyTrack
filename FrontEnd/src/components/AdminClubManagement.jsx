import React, { useState, useEffect } from "react";
import api from "../api";

const AdminClubManagement = () => {
  const [clubs, setClubs] = useState([]);
  const [mentors, setMentors] = useState([]);
  const [students, setStudents] = useState([]);
  const [organizers, setOrganizers] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [signatureUploading, setSignatureUploading] = useState(false);
  const [currentSignature, setCurrentSignature] = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    description: "",
    faculty_coordinator: null,
    established_date: "",
  });

  const handlePrincipalSignatureUpload = async (e) => {
    e.preventDefault();
    const signatureFile = e.target.signature.files[0];
    if (!signatureFile) {
      setError("Please select a signature file");
      return;
    }

    setSignatureUploading(true);
    setError("");
    setSuccess("");

    try {
      const formData = new FormData();
      formData.append("signature_image", signatureFile);
      formData.append("notes", "Uploaded via admin panel");

      const response = await api.post(
        "/admin/clubs/upload_principal_signature/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setSuccess("Principal signature uploaded successfully!");
      setCurrentSignature(response.data.signature);
    } catch (err) {
      setError("Failed to upload principal signature");
    } finally {
      setSignatureUploading(false);
    }
  };

  const fetchCurrentSignature = async () => {
    try {
      const response = await api.get("/admin/clubs/principal_signature/");
      if (response.data) {
        setCurrentSignature(response.data);
      }
    } catch (err) {
      // No signature found, that's ok
    }
  };

  useEffect(() => {
    fetchData();
    fetchCurrentSignature();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);

      const [clubsRes, mentorsRes, studentsRes, organizersRes] =
        await Promise.all([
          api.get("/admin/clubs/"),
          api.get("/mentors/"),
          api.get("/students/"),
          api.get("/club-organizers/"),
        ]);

      setClubs(clubsRes.data.results || clubsRes.data);
      setMentors(mentorsRes.data.results || mentorsRes.data);
      setStudents(studentsRes.data.results || studentsRes.data);
      setOrganizers(organizersRes.data.results || organizersRes.data);

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
      setSuccess("");

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
      await api.post(`/admin/clubs/${clubId}/assign_coordinator/`, {
        mentor_id: mentorId,
      });
      setSuccess("Faculty coordinator assigned successfully");
      fetchData();
    } catch {
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
    } catch {
      setError("Failed to assign club head");
    }
  };

  const handleAssignOrganizer = async (clubId, organizerId) => {
    try {
      await api.post(`/admin/clubs/${clubId}/assign_organizer/`, {
        organizer_id: organizerId,
      });
      setSuccess("Organizer assigned successfully");
      fetchData();
    } catch {
      setError("Failed to assign organizer");
    }
  };

  if (loading) return <div className="text-center py-10">Loading clubs...</div>;

  return (
    <div className="space-y-6">
      {/* Principal Signature Section */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Principal Signature Management
        </h2>
        <div className="space-y-4">
          {currentSignature && (
            <div className="flex items-center space-x-4 p-4 bg-green-50 rounded-lg">
              <div>
                <p className="text-sm font-medium text-gray-700">
                  Current Signature
                </p>
                <p className="text-sm text-gray-600">
                  Uploaded on:{" "}
                  {new Date(currentSignature.uploaded_at).toLocaleDateString()}
                </p>
                {currentSignature.notes && (
                  <p className="text-sm text-gray-600">
                    Notes: {currentSignature.notes}
                  </p>
                )}
              </div>
              <div className="ml-auto">
                <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
                  Active
                </span>
              </div>
            </div>
          )}

          <form onSubmit={handlePrincipalSignatureUpload} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Upload Principal Signature
              </label>
              <input
                type="file"
                name="signature"
                accept="image/*"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                required
              />
              <p className="text-xs text-gray-500 mt-1">
                Accepted formats: PNG, JPG, JPEG. This signature will be used on
                all certificates.
              </p>
            </div>

            <button
              type="submit"
              disabled={signatureUploading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {signatureUploading ? "Uploading..." : "Upload Signature"}
            </button>
          </form>
        </div>
      </div>

      {/* Alerts */}
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
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          ➕ Create Club
        </button>
      </div>

      {/* Create Club Form */}
      {showCreateForm && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Create New Club</h3>

          <form onSubmit={handleCreateClub} className="space-y-4">
            <div>
              <label className="block text-sm font-medium">Club Name</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
                required
                className="w-full px-4 py-2 border rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium">
                Club Description
              </label>
              <textarea
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                className="w-full px-4 py-2 border rounded-lg"
                rows="4"
              ></textarea>
            </div>

            <div>
              <label className="block text-sm font-medium">
                Established Date
              </label>
              <input
                type="date"
                value={formData.established_date}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    established_date: e.target.value,
                  })
                }
                className="w-full px-4 py-2 border rounded-lg"
              />
            </div>

            <div>
              <label className="block text-sm font-medium">
                Faculty Coordinator (Optional)
              </label>
              <select
                value={formData.faculty_coordinator || ""}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    faculty_coordinator: e.target.value,
                  })
                }
                className="w-full px-4 py-2 border rounded-lg"
              >
                <option value="">Select Faculty Coordinator</option>
                {mentors.map((mentor) => (
                  <option key={mentor.id} value={mentor.id}>
                    {mentor.user_details?.first_name}{" "}
                    {mentor.user_details?.last_name}
                  </option>
                ))}
              </select>
            </div>

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

            <div className="space-y-4">
              {/* Faculty Coordinator */}
              <div>
                <label className="text-sm font-medium text-gray-700">
                  Faculty Coordinator
                </label>
                <select
                  value={club.faculty_coordinator || ""}
                  onChange={(e) =>
                    handleAssignCoordinator(club.id, e.target.value)
                  }
                  className="w-full px-3 py-2 border rounded"
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

              {/* Club Head */}
              <div>
                <label className="text-sm font-medium text-gray-700">
                  Club Head
                </label>
                <select
                  value={club.club_head || ""}
                  onChange={(e) => handleAssignHead(club.id, e.target.value)}
                  className="w-full px-3 py-2 border rounded"
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

              {/* Assign Organizer */}
              <div>
                <label className="text-sm font-medium text-gray-700">
                  Assign Organizer
                </label>
                <select
                  defaultValue=""
                  onChange={(e) => {
                    if (e.target.value) {
                      handleAssignOrganizer(club.id, e.target.value);
                      e.target.value = "";
                    }
                  }}
                  className="w-full px-3 py-2 border rounded"
                >
                  <option value="">Select Organizer</option>
                  {organizers.map((org) => (
                    <option key={org.id} value={org.id}>
                      {org.user_details?.first_name}{" "}
                      {org.user_details?.last_name}
                    </option>
                  ))}
                </select>

                {/* Show current organizers */}
                <div className="mt-2">
                  <p className="text-sm font-medium">Current Organizers:</p>
                  {club.organizers && club.organizers.length > 0 ? (
                    <ul className="text-sm list-disc ml-4">
                      {club.organizers.map((org) => (
                        <li key={org.id}>
                          {org.user?.first_name ||
                            org.user_details?.first_name ||
                            ""}{" "}
                          {org.user?.last_name ||
                            org.user_details?.last_name ||
                            ""}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-sm text-gray-500">
                      No organizers assigned
                    </p>
                  )}
                </div>
              </div>

              {/* Additional Info */}
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
