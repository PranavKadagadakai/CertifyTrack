import React, { useState, useEffect } from "react";
import api from "../api";
import EventAttendanceForm from "./EventAttendanceForm";

const EventManagement = ({ clubId, onEventCreated, onEventUpdated }) => {
  const [events, setEvents] = useState([]);
  const [categories, setCategories] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [showForm, setShowForm] = useState(false);
  const [editingEvent, setEditingEvent] = useState(null);

  // NEW: attendance upload modal
  const [showAttendanceUpload, setShowAttendanceUpload] = useState(false);
  const [attendanceEventId, setAttendanceEventId] = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    description: "",
    event_date: "",
    end_date: "",
    start_time: "",
    end_time: "",
    max_participants: "",
    needsVenueCampus: false,
    primary_hall: "",
    secondary_hall: "",
    awardsAictePoints: false,
    aicte_category: "",
    points_awarded: 0,
  });

  const [halls, setHalls] = useState([]);
  const [availableHalls, setAvailableHalls] = useState([]);

  useEffect(() => {
    fetchEvents();
    fetchCategories();
    fetchHalls();
  }, []);

  useEffect(() => {
    // Update available halls when date/time changes
    if (formData.event_date && formData.start_time) {
      fetchAvailableHalls();
    }
  }, [formData.event_date, formData.start_time, formData.end_time]);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const response = await api.get("/events/?club=true");
      setEvents(Array.isArray(response.data) ? response.data : []);
      setError("");
    } catch (err) {
      setError("Failed to load events");
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await api.get("/aicte-categories/");
      setCategories(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      console.error("Failed to fetch AICTE categories");
    }
  };

  const fetchHalls = async () => {
    try {
      const response = await api.get("/halls/");
      setHalls(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      console.error("Failed to fetch halls");
    }
  };

  const fetchAvailableHalls = async () => {
    if (!formData.event_date || !formData.start_time) return;

    const endTime = formData.end_time || formData.start_time;
    try {
      const response = await api.get(
        `/halls/available/?date=${formData.event_date}&start_time=${formData.start_time}&end_time=${endTime}`
      );
      setAvailableHalls(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      console.error("Failed to fetch available halls");
    }
  };

  const resetForm = () => {
    setFormData({
      name: "",
      description: "",
      event_date: "",
      end_date: "",
      start_time: "",
      end_time: "",
      max_participants: "",
      needsVenueCampus: false,
      primary_hall: "",
      secondary_hall: "",
      awardsAictePoints: false,
      aicte_category: "",
      points_awarded: 0,
    });
    setEditingEvent(null);
    setShowForm(false);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (
      formData.end_date &&
      new Date(formData.end_date) < new Date(formData.event_date)
    ) {
      setError("End date must be after start date");
      return;
    }

    if (
      formData.awardsAictePoints &&
      (!formData.aicte_category || !formData.points_awarded)
    ) {
      setError(
        "AICTE Category and Points Awarded are required when AICTE points are to be awarded"
      );
      return;
    }

    // Create a copy of formData and clear fields based on checkboxes
    const submitData = { ...formData };

    // If need venue is false, clear hall fields
    if (!formData.needsVenueCampus) {
      submitData.primary_hall = "";
      submitData.secondary_hall = "";
    }

    // If AICTE points is false, clear AICTE fields
    if (!formData.awardsAictePoints) {
      submitData.aicte_category = "";
      submitData.points_awarded = 0;
    }

    setLoading(true);
    try {
      if (editingEvent) {
        await api.patch(`/events/${editingEvent.id}/`, submitData);
        setSuccess("Event updated successfully!");
        onEventUpdated?.(submitData);
      } else {
        const response = await api.post("/events/", submitData);
        setSuccess("Event created successfully!");
        onEventCreated?.(response.data);
      }
      fetchEvents();
      resetForm();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          "Failed to save event"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (event) => {
    const hasVenue = !!(event.primary_hall || event.secondary_hall);
    const hasAicte = !!(event.aicte_category || event.points_awarded > 0);

    setFormData({
      name: event.name,
      description: event.description || "",
      event_date: event.event_date,
      end_date: event.end_date || "",
      start_time: event.start_time,
      end_time: event.end_time || "",
      max_participants: event.max_participants || "",
      needsVenueCampus: hasVenue,
      primary_hall: event.primary_hall || "",
      secondary_hall: event.secondary_hall || "",
      awardsAictePoints: hasAicte,
      aicte_category: event.aicte_category || "",
      points_awarded: event.points_awarded || 0,
    });
    setEditingEvent(event);
    setShowForm(true);
  };

  const handleDelete = async (eventId) => {
    if (!window.confirm("Are you sure you want to delete this event?")) return;

    try {
      await api.delete(`/events/${eventId}/`);
      setSuccess("Event deleted successfully!");
      fetchEvents();
    } catch (err) {
      setError("Failed to delete event");
    }
  };

  const handleGenerateCertificates = async (eventId) => {
    if (
      !window.confirm(
        "This will generate certificates for all attendees. Continue?"
      )
    )
      return;

    try {
      setSuccess("Generating certificates...");
      const res = await api.post(`/events/${eventId}/generate-certificates/`);

      const message =
        res.data.message ||
        `Successfully generated ${res.data.certificate_count} certificates.`;
      setSuccess(message);

      if (res.data.errors && res.data.errors.length > 0) {
        console.error("Certificate generation errors:", res.data.errors);
        setError(`${res.data.warning}\n\nCheck console for details.`);
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || "Failed to generate certificates");
    }
  };

  // NEW: detect complete → open attendance upload modal
  const handleStatusChange = async (eventId, newStatus) => {
    try {
      await api.patch(`/events/${eventId}/`, { status: newStatus });
      setSuccess(`Event status updated to ${newStatus}`);
      fetchEvents();

      if (newStatus === "scheduled") {
        // Auto-assign hall when scheduled
        setTimeout(() => fetchEvents(), 1000); // Refresh to see assigned hall
      } else if (newStatus === "completed") {
        setAttendanceEventId(eventId);
        setShowAttendanceUpload(true);
      }
    } catch (err) {
      setError("Failed to update event status");
    }
  };

  return (
    <div className="space-y-6">
      {error && (
        <div className="p-4 bg-red-100 text-red-700 rounded">{error}</div>
      )}
      {success && (
        <div className="p-4 bg-green-100 text-green-700 rounded">{success}</div>
      )}

      <div className="flex gap-4">
        <button
          onClick={() => {
            resetForm();
            setShowForm(!showForm);
          }}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          {showForm ? "Cancel" : "+ Create Event"}
        </button>

        <button
          onClick={fetchEvents}
          className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded"
        >
          Refresh
        </button>
      </div>

      {/* EVENT FORM */}
      {showForm && (
        <form
          onSubmit={handleSubmit}
          className="bg-white p-6 rounded-lg shadow space-y-4 border-l-4 border-blue-600"
        >
          <h3 className="text-lg font-semibold">
            {editingEvent ? "Edit Event" : "Create New Event"}
          </h3>

          <div>
            <label className="block text-sm mb-1 font-medium">
              Event Name *
            </label>
            <input
              type="text"
              name="name"
              required
              value={formData.name}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              placeholder="Enter event name"
            />
          </div>

          <div>
            <label className="block text-sm mb-1 font-medium">
              Description
            </label>
            <textarea
              name="description"
              rows="3"
              value={formData.description}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              placeholder="Event description"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm mb-1 font-medium">
                Event Date *
              </label>
              <input
                type="date"
                name="event_date"
                required
                value={formData.event_date}
                onChange={handleChange}
                className="w-full p-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm mb-1 font-medium">End Date</label>
              <input
                type="date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
                className="w-full p-2 border rounded"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm mb-1 font-medium">
                Start Time *
              </label>
              <input
                type="time"
                name="start_time"
                required
                value={formData.start_time}
                onChange={handleChange}
                className="w-full p-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm mb-1 font-medium">End Time</label>
              <input
                type="time"
                name="end_time"
                value={formData.end_time}
                onChange={handleChange}
                className="w-full p-2 border rounded"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm mb-1 font-medium">
              Max Participants
            </label>
            <input
              type="number"
              min="1"
              name="max_participants"
              value={formData.max_participants}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              placeholder="Optional"
            />
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="needsVenueCampus"
              name="needsVenueCampus"
              checked={formData.needsVenueCampus}
              onChange={handleChange}
            />
            <label htmlFor="needsVenueCampus" className="text-sm font-medium">
              Does this event need a venue in the college campus?
            </label>
          </div>

          {/* Hall Selection Section - Only show if needsVenueCampus is true */}
          {formData.needsVenueCampus && (
            <div className="bg-gray-50 p-4 rounded border">
              <h4 className="font-medium mb-3">Venue Selection</h4>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm mb-1 font-medium">
                    Primary Hall (Preferred)
                  </label>
                  <select
                    name="primary_hall"
                    value={formData.primary_hall}
                    onChange={handleChange}
                    className="w-full p-2 border rounded"
                  >
                    <option value="">Select Primary Hall</option>
                    {availableHalls.map((hall) => (
                      <option key={hall.id} value={hall.id}>
                        {hall.name} (Capacity: {hall.capacity})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm mb-1 font-medium">
                    Secondary Hall (Backup)
                  </label>
                  <select
                    name="secondary_hall"
                    value={formData.secondary_hall}
                    onChange={handleChange}
                    className="w-full p-2 border rounded"
                  >
                    <option value="">Select Secondary Hall</option>
                    {availableHalls.map((hall) => (
                      <option key={hall.id} value={hall.id}>
                        {hall.name} (Capacity: {hall.capacity})
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <p className="text-sm text-gray-500 mt-2">
                System will automatically assign available halls when event is
                scheduled.
              </p>
            </div>
          )}

          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="awardsAictePoints"
              name="awardsAictePoints"
              checked={formData.awardsAictePoints}
              onChange={handleChange}
            />
            <label htmlFor="awardsAictePoints" className="text-sm font-medium">
              Will AICTE points be awarded for this event?
            </label>
          </div>

          {/* AICTE Points Section - Only show if awardsAictePoints is true */}
          {formData.awardsAictePoints && (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm mb-1 font-medium">
                  AICTE Category *
                </label>
                <select
                  name="aicte_category"
                  value={formData.aicte_category}
                  onChange={handleChange}
                  className="w-full p-2 border rounded"
                >
                  <option value="">Select Category</option>
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm mb-1 font-medium">
                  Points Awarded *
                </label>
                <input
                  type="number"
                  name="points_awarded"
                  value={formData.points_awarded}
                  onChange={handleChange}
                  className="w-full p-2 border rounded"
                  placeholder="0"
                  min="0"
                />
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded"
          >
            {loading
              ? "Saving..."
              : editingEvent
              ? "Update Event"
              : "Create Event"}
          </button>
        </form>
      )}

      {/* EVENTS LIST */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 bg-gray-50 border-b">
          <h3 className="text-lg font-semibold">Your Events</h3>
        </div>

        {events.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            No events created yet.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100 border-b">
                <tr>
                  <th className="px-6 py-3 text-left">Name</th>
                  <th className="px-6 py-3 text-left">Date</th>
                  <th className="px-6 py-3 text-left">Time</th>
                  <th className="px-6 py-3 text-left">Venue</th>
                  <th className="px-6 py-3 text-left">Status</th>
                  <th className="px-6 py-3 text-left">Participants</th>
                  <th className="px-6 py-3 text-left">Actions</th>
                </tr>
              </thead>

              <tbody>
                {events.map((event) => (
                  <tr key={event.id} className="border-b">
                    <td className="px-6 py-3">{event.name}</td>
                    <td className="px-6 py-3">
                      {new Date(event.event_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-3">
                      {event.start_time} - {event.end_time || ""}
                    </td>
                    <td className="px-6 py-3">
                      {event.assigned_hall_name || "Not assigned"}
                    </td>
                    <td className="px-6 py-3">
                      <span className="px-3 py-1 text-xs rounded bg-blue-100 text-blue-800">
                        {event.status}
                      </span>
                    </td>
                    <td className="px-6 py-3">
                      {event.registrations?.length || 0} /{" "}
                      {event.max_participants || "∞"}
                    </td>
                    <td className="px-6 py-3 space-x-2">
                      {event.status === "draft" && (
                        <>
                          <button
                            onClick={() => handleEdit(event)}
                            className="px-3 py-1 bg-blue-600 text-white rounded text-xs"
                          >
                            Edit
                          </button>
                          <button
                            onClick={() =>
                              handleStatusChange(event.id, "scheduled")
                            }
                            className="px-3 py-1 bg-green-600 text-white rounded text-xs"
                          >
                            Schedule
                          </button>
                          <button
                            onClick={() => handleDelete(event.id)}
                            className="px-3 py-1 bg-red-600 text-white rounded text-xs"
                          >
                            Delete
                          </button>
                        </>
                      )}

                      {event.status === "scheduled" && (
                        <button
                          onClick={() =>
                            handleStatusChange(event.id, "ongoing")
                          }
                          className="px-3 py-1 bg-yellow-500 text-white rounded text-xs"
                        >
                          Start
                        </button>
                      )}

                      {event.status === "ongoing" && (
                        <button
                          onClick={() => {
                            handleStatusChange(event.id, "completed");
                            setAttendanceEventId(event.id);
                            setShowAttendanceUpload(true);
                          }}
                          className="px-3 py-1 bg-green-600 text-white rounded text-xs"
                        >
                          Complete
                        </button>
                      )}

                      {event.status === "completed" && (
                        <div className="flex gap-1">
                          <button
                            onClick={() => handleGenerateCertificates(event.id)}
                            className="px-3 py-1 bg-purple-600 text-white rounded text-xs hover:bg-purple-700"
                          >
                            🎓 Certificates
                          </button>
                          <button
                            onClick={() => {
                              setAttendanceEventId(event.id);
                              setShowAttendanceUpload(true);
                            }}
                            className="px-3 py-1 bg-blue-600 text-white rounded text-xs"
                          >
                            Attendance
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Attendance Upload Modal */}
        {showAttendanceUpload && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded shadow-xl w-[600px] max-h-[80vh] overflow-y-auto">
              <h2 className="text-xl font-semibold mb-4">
                Upload Attendance for Event #{attendanceEventId}
              </h2>

              <EventAttendanceForm eventId={attendanceEventId} />

              <button
                onClick={() => setShowAttendanceUpload(false)}
                className="mt-4 px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
              >
                Close
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EventManagement;
