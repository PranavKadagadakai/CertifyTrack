import React, { useState, useEffect } from "react";
import api from "../api";

const EventAttendanceForm = ({ eventId }) => {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(eventId || null);
  const [participants, setParticipants] = useState([]);
  const [file, setFile] = useState(null);
  const [attendancePreview, setAttendancePreview] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generatingCertificates, setGeneratingCertificates] = useState(false);
  const [canGenerateCertificates, setCanGenerateCertificates] = useState(false);

  useEffect(() => {
    // Load club events only if eventId not provided (dropdown mode)
    if (!eventId) {
      fetchClubEvents();
    }

    // Auto-load participants if eventId provided (modal mode)
    if (eventId) {
      setSelectedEvent(eventId);
      loadParticipants(eventId);
    }
  }, [eventId]);

  const fetchClubEvents = async () => {
    try {
      const res = await api.get("/events/?club=true");
      setEvents(res.data.results || res.data);
    } catch (err) {
      console.error("Failed to fetch events", err);
    }
  };

  const loadParticipants = async (id) => {
    try {
      setLoading(true);
      const res = await api.get(`/events/${id}/participants/`);
      setParticipants(res.data.participants || []);
    } catch (err) {
      console.error(err);
      alert("Failed to load participants");
    } finally {
      setLoading(false);
    }
  };

  const handleEventChange = (e) => {
    const id = e.target.value;
    setSelectedEvent(id);
    setFile(null);
    setAttendancePreview([]);
    if (id) loadParticipants(id);
  };

  const handleFileChange = async (e) => {
    const f = e.target.files[0];
    setFile(f);
    setAttendancePreview([]);

    if (!f) return;

    const name = f.name.toLowerCase();

    if (name.endsWith(".csv")) {
      const text = await f.text();
      const lines = text.split(/\r?\n/).filter(Boolean);
      if (lines.length === 0) return;

      const headers = lines[0].split(",").map((h) => h.trim());
      const rows = lines.slice(1).map((line) => {
        const cells = line.split(",").map((c) => c.trim());
        const obj = {};
        headers.forEach((h, i) => (obj[h] = cells[i] || ""));
        return obj;
      });

      setAttendancePreview(rows.slice(0, 200));
    } else if (name.endsWith(".xlsx") || name.endsWith(".xls")) {
      setAttendancePreview([
        {
          note: "XLSX file selected — preview will be generated server-side.",
        },
      ]);
    } else {
      alert("Only CSV and XLSX files are supported");
      setFile(null);
    }
  };

  const submitAttendance = async () => {
    if (!selectedEvent) {
      alert("Select an event first");
      return;
    }

    if (!file) {
      alert("Please choose a CSV/XLSX file containing attendance.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await api.post(
        `/events/${selectedEvent}/upload-attendance/`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      alert(res.data.message || "Attendance uploaded successfully!");
      setCanGenerateCertificates(true);

      await loadParticipants(selectedEvent);

      setFile(null);
      setAttendancePreview([]);
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.error || "Failed to upload attendance");
    } finally {
      setLoading(false);
    }
  };

  const generateCertificates = async () => {
    if (!selectedEvent) {
      alert("Select an event first");
      return;
    }

    try {
      setGeneratingCertificates(true);
      const res = await api.post(
        `/events/${selectedEvent}/generate-certificates/`
      );

      const message =
        res.data.message ||
        `Successfully generated ${res.data.certificate_count} certificates.`;
      alert(message);

      if (res.data.errors && res.data.errors.length > 0) {
        console.error("Certificate generation errors:", res.data.errors);
        alert(`${res.data.warning}\n\nCheck console for details.`);
      }

      // Allow regenerating certificates even after successful generation
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.error || "Failed to generate certificates");
    } finally {
      setGeneratingCertificates(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow max-w-4xl mx-auto">
      <h2 className="text-xl font-semibold mb-4">Upload Attendance</h2>

      {/* DROPDOWN only if eventId not provided */}
      {!eventId && (
        <div className="mb-4">
          <label className="block mb-2 font-medium">Select Event</label>
          <select
            value={selectedEvent || ""}
            onChange={handleEventChange}
            className="border p-2 w-full rounded"
          >
            <option value="">-- Select Event --</option>
            {events.map((ev) => (
              <option key={ev.id} value={ev.id}>
                {ev.name} — {new Date(ev.event_date).toLocaleDateString()}
              </option>
            ))}
          </select>
        </div>
      )}

      {selectedEvent && (
        <>
          <div className="mb-4">
            <h3 className="font-medium mb-2">Participants</h3>

            {loading ? (
              <div>Loading participants...</div>
            ) : participants.length === 0 ? (
              <div className="text-gray-600">No registrations found.</div>
            ) : (
              <div className="overflow-auto max-h-56 border rounded">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50 sticky top-0">
                    <tr>
                      <th className="p-2 border">ID</th>
                      <th className="p-2 border">USN</th>
                      <th className="p-2 border">Name</th>
                    </tr>
                  </thead>
                  <tbody>
                    {participants.map((p) => (
                      <tr key={p.student_id}>
                        <td className="p-2 border">{p.student_id}</td>
                        <td className="p-2 border">{p.usn}</td>
                        <td className="p-2 border">{p.full_name}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            <p className="text-xs text-gray-500 mt-2">
              CSV format: <strong>student_id, usn, attendance</strong>
            </p>
          </div>

          <div className="mb-4">
            <label className="block mb-2 font-medium">Upload CSV/XLSX</label>
            <input
              type="file"
              accept=".csv, .xlsx, .xls"
              onChange={handleFileChange}
            />
          </div>

          {attendancePreview.length > 0 && (
            <div className="mb-4">
              <h4 className="font-medium mb-2">Preview</h4>
              <div className="overflow-auto max-h-44 border rounded">
                <table className="w-full text-sm">
                  <thead>
                    <tr>
                      {Object.keys(attendancePreview[0]).map((key) => (
                        <th key={key} className="p-1 border">
                          {key}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {attendancePreview.map((row, idx) => (
                      <tr key={idx}>
                        {Object.keys(attendancePreview[0]).map((key) => (
                          <td key={key} className="p-1 border">
                            {row[key]}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="flex gap-2">
            <button
              onClick={submitAttendance}
              disabled={loading}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded disabled:opacity-50"
            >
              {loading ? "Uploading..." : "Upload & Process Attendance"}
            </button>

            {canGenerateCertificates && (
              <button
                onClick={generateCertificates}
                disabled={generatingCertificates}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded disabled:opacity-50"
              >
                {generatingCertificates
                  ? "Generating..."
                  : "🎓 Generate Certificates"}
              </button>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default EventAttendanceForm;
