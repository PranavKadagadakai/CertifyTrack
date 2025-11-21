import { useEffect, useState } from "react";
import api from "../api";

export default function AssignMentees() {
  const [students, setStudents] = useState([]);
  const [success, setSuccess] = useState("");

  useEffect(() => {
    api.get("/students/all/").then((res) => setStudents(res.data));
  }, []);

  const assign = async (studentId) => {
    try {
      await api.post(`/mentor/assign/${studentId}/`);
      setSuccess("Mentee assigned successfully!");
    } catch {
      setSuccess("Failed to assign mentee.");
    }
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Assign Mentees</h2>
      {success && <p className="text-green-600">{success}</p>}

      <table className="w-full border">
        <thead>
          <tr>
            <th className="p-2 border">USN</th>
            <th className="p-2 border">Department</th>
            <th className="p-2 border">Action</th>
          </tr>
        </thead>
        <tbody>
          {students.map((s) => (
            <tr key={s.id}>
              <td className="border p-2">{s.usn}</td>
              <td className="border p-2">{s.department}</td>
              <td className="border p-2">
                <button
                  className="px-3 py-1 bg-blue-600 text-white rounded"
                  onClick={() => assign(s.id)}
                >
                  Assign
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
