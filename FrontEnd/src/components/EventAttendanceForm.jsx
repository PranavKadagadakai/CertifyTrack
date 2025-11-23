import React, { useState, useEffect } from "react";
import api from "../api";

const EventAttendanceForm = () => {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [registrations, setRegistrations] = useState([]);
  const [attendance, setAttendance] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await api.get("/events/?club=true");
      setEvents(
        response.data.filter(
          (e) => e.status === "ongoing" || e.status === "completed"
        )
      );
    } catch (err) {
      setError("Failed to fetch events");
    }
  };

  const handleEventSelect = async (eventId) => {
    setSelectedEvent(eventId);
    setAttendance({});
    setSuccess("");

    try {
      const response = await api.get(`/events/${eventId}/`);
      setRegistrations(response.data.registrations || []);
    } catch (err) {
      setError("Failed to fetch registrations");
    }
  };

  const handleAttendanceChange = (studentId) => {
    setAttendance((prev) => ({
      ...prev,
      [studentId]: !prev[studentId],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const attendanceData = registrations.map((reg) => ({
        student_id: reg.student,
        is_present: attendance[reg.student] || false,
      }));

      const response = await api.post(
        `/events/${selectedEvent}/mark_attendance/`,
        { attendance: attendanceData }
      );

      setSuccess(
        `Attendance marked! ${response.data.created_count} records created, ` +
          `${response.data.aicte_transactions_created} AICTE transactions allocated.`
      );
      setAttendance({});
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to mark attendance");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-6">Mark Event Attendance</h2>

      {error && (
        <div className="mb-4 p-4 bg-red-100 text-red-700 rounded">{error}</div>
      )}
      {success && (
        <div className="mb-4 p-4 bg-green-100 text-green-700 rounded">
          {success}
        </div>
      )}

      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">Select Event:</label>
        <select
          value={selectedEvent || ""}
          onChange={(e) => handleEventSelect(parseInt(e.target.value))}
          className="w-full p-2 border rounded"
        >
          <option value="">Choose an event</option>
          {events.map((event) => (
            <option key={event.id} value={event.id}>
              {event.name} - {new Date(event.event_date).toLocaleDateString()}
            </option>
          ))}
        </select>
      </div>

      {selectedEvent && registrations.length > 0 && (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-4">
              Mark Attendance ({registrations.length} registered)
            </h3>

            <div className="max-h-96 overflow-y-auto border rounded p-4 space-y-2">
              {registrations.map((reg) => (
                <label
                  key={reg.id}
                  className="flex items-center p-2 hover:bg-gray-100 rounded"
                >
                  <input
                    type="checkbox"
                    checked={attendance[reg.student] || false}
                    onChange={() => handleAttendanceChange(reg.student)}
                    className="mr-3"
                  />
                  <span className="text-sm">{reg.student_usn}</span>
                </label>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading
              ? "Marking Attendance..."
              : "Mark Attendance & Allocate Points"}
          </button>
        </form>
      )}

      {selectedEvent && registrations.length === 0 && (
        <p className="text-gray-600">No registrations for this event</p>
      )}
    </div>
  );
};

export default EventAttendanceForm;
