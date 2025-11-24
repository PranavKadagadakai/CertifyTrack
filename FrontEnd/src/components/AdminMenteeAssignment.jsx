import React, { useState, useEffect } from "react";
import api from "../api";

const AdminMenteeAssignment = () => {
  const [mentorMenteeData, setMentorMenteeData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [csvFile, setCsvFile] = useState(null);

  useEffect(() => {
    fetchMenteeAssignments();
  }, []);

  const fetchMenteeAssignments = async () => {
    try {
      setLoading(true);
      const response = await api.get("/admin/mentees/");
      setMentorMenteeData(response.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to load mentee assignments");
      setLoading(false);
    }
  };

  const handleBulkUpload = async (e) => {
    e.preventDefault();
    if (!csvFile) {
      setError("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("csv_file", csvFile);

    try {
      setError("");
      const response = await api.post("/admin/mentees/bulk_assign/", formData);
      setSuccess(
        `Assigned ${response.data.assigned} mentees. Errors: ${response.data.errors.length}`
      );
      setCsvFile(null);
      fetchMenteeAssignments();
    } catch (err) {
      setError(err.response?.data?.error || "Failed to process CSV");
    }
  };

  if (loading)
    return (
      <div className="text-center py-10">Loading mentee assignments...</div>
    );

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

      {/* Bulk Upload */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-bold mb-4">Bulk Assign Mentees from CSV</h3>
        <form onSubmit={handleBulkUpload} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Upload CSV (Format: mentor_employee_id, student_usn)
            </label>
            <input
              type="file"
              accept=".csv"
              onChange={(e) => setCsvFile(e.target.files[0])}
              className="block w-full text-sm text-gray-500
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-md file:border-0
                      file:text-sm file:font-semibold
                      file:bg-blue-50 file:text-blue-700
                      hover:file:bg-blue-100"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Upload & Assign
          </button>
        </form>
      </div>

      {/* Assignments List */}
      <div className="bg-white rounded-lg shadow overflow-x-auto">
        <div className="p-6">
          <h3 className="text-lg font-bold mb-4">Mentor-Mentee Assignments</h3>
          <div className="space-y-6">
            {mentorMenteeData.map((mentor) => (
              <div key={mentor.mentor_id} className="border rounded-lg p-4">
                <div className="font-bold text-lg text-blue-600 mb-2">
                  {mentor.mentor_name} (ID: {mentor.mentor_employee_id})
                </div>
                <div className="text-sm text-gray-600 mb-3">
                  Total Mentees:{" "}
                  <span className="font-bold">{mentor.mentee_count}</span>
                </div>
                {mentor.mentees.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-gray-50 border-b">
                        <tr>
                          <th className="px-4 py-2 text-left">USN</th>
                          <th className="px-4 py-2 text-left">Name</th>
                        </tr>
                      </thead>
                      <tbody>
                        {mentor.mentees.map((student) => (
                          <tr
                            key={student.id}
                            className="border-b hover:bg-gray-50"
                          >
                            <td className="px-4 py-2">{student.usn}</td>
                            <td className="px-4 py-2">{student.name}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className="text-gray-500 text-sm">No mentees assigned</p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CSV Format Help */}
      <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
        <h4 className="font-bold mb-2">CSV Format Instructions</h4>
        <p className="text-sm text-gray-700 mb-3">
          Your CSV file should have two columns with the following format:
        </p>
        <pre className="bg-white border p-4 rounded text-sm overflow-x-auto">
          mentor_employee_id,student_usn 1,USN001 1,USN002 2,USN003
        </pre>
      </div>
    </div>
  );
};

export default AdminMenteeAssignment;
