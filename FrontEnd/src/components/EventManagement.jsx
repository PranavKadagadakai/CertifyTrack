import React, { useState, useEffect } from "react";
import api from "../api";

const EventManagement = ({ clubId, onEventCreated, onEventUpdated }) => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingEvent, setEditingEvent] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    event_date: "",
    start_time: "",
    end_time: "",
    max_participants: "",
    status: "draft",
  });

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const response = await api.get("/events/?club=true");
      setEvents(response.data);
      setError("");
    } catch (err) {
      console.error("Failed to fetch events:", err);
      setError("Failed to load events");
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      name: "",
      description: "",
      event_date: "",
      start_time: "",
      end_time: "",
      max_participants: "",
      status: "draft",
    });
    setEditingEvent(null);
    setShowForm(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    if (!formData.name || !formData.event_date || !formData.start_time) {
      setError("Please fill in all required fields");
      setLoading(false);
      return;
    }

    try {
      if (editingEvent) {
        // Update event
        await api.patch(`/events/${editingEvent.id}/`, formData);
        setSuccess("Event updated successfully!");
        onEventUpdated?.(formData);
      } else {
        // Create new event
        const response = await api.post("/events/", formData);
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
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleEdit = (event) => {
    setFormData({
      name: event.name,
      description: event.description || "",
      event_date: event.event_date,
      start_time: event.start_time,
      end_time: event.end_time || "",
      max_participants: event.max_participants || "",
      status: event.status,
    });
    setEditingEvent(event);
    setShowForm(true);
  };

  const handleDelete = async (eventId) => {
    if (window.confirm("Are you sure you want to delete this event?")) {
      try {
        await api.delete(`/events/${eventId}/`);
        setSuccess("Event deleted successfully!");
        fetchEvents();
      } catch (err) {
        setError("Failed to delete event");
        console.error(err);
      }
    }
  };

  const handleStatusChange = async (eventId, newStatus) => {
    try {
      await api.patch(`/events/${eventId}/`, { status: newStatus });
      setSuccess(`Event status updated to ${newStatus}`);
      fetchEvents();
    } catch (err) {
      setError("Failed to update event status");
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Messages */}
      {error && (
        <div className="p-4 bg-red-100 text-red-700 rounded-lg border border-red-300">
          {error}
        </div>
      )}
      {success && (
        <div className="p-4 bg-green-100 text-green-700 rounded-lg border border-green-300">
          {success}
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-4">
        <button
          onClick={() => {
            resetForm();
            setShowForm(!showForm);
          }}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium transition"
        >
          {showForm ? "Cancel" : "+ Create Event"}
        </button>
        <button
          onClick={fetchEvents}
          className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg font-medium transition"
        >
          Refresh
        </button>
      </div>

      {/* Event Form */}
      {showForm && (
        <form
          onSubmit={handleSubmit}
          className="bg-white p-6 rounded-lg shadow-md space-y-4 border-l-4 border-blue-500"
        >
          <h3 className="text-lg font-semibold text-gray-800">
            {editingEvent ? "Edit Event" : "Create New Event"}
          </h3>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Event Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., Tech Conference 2025"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="3"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Event description..."
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Event Date <span className="text-red-500">*</span>
              </label>
              <input
                type="date"
                name="event_date"
                value={formData.event_date}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Participants
              </label>
              <input
                type="number"
                name="max_participants"
                value={formData.max_participants}
                onChange={handleChange}
                min="1"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., 100"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Start Time <span className="text-red-500">*</span>
              </label>
              <input
                type="time"
                name="start_time"
                value={formData.start_time}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                End Time
              </label>
              <input
                type="time"
                name="end_time"
                value={formData.end_time}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg font-medium transition"
          >
            {loading
              ? "Saving..."
              : editingEvent
              ? "Update Event"
              : "Create Event"}
          </button>
        </form>
      )}

      {/* Events List */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800">Your Events</h3>
        </div>

        {loading && events.length === 0 ? (
          <div className="px-6 py-8 text-center text-gray-500">
            Loading events...
          </div>
        ) : events.length === 0 ? (
          <div className="px-6 py-8 text-center text-gray-500">
            No events yet. Create your first event!
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                    Event Name
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                    Time
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                    Participants
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {events.map((event) => (
                  <tr
                    key={event.id}
                    className="border-b border-gray-200 hover:bg-gray-50 transition"
                  >
                    <td className="px-6 py-4 text-sm text-gray-900 font-medium">
                      {event.name}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {new Date(event.event_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {event.start_time} - {event.end_time || ""}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          event.status === "draft"
                            ? "bg-gray-100 text-gray-800"
                            : event.status === "scheduled"
                            ? "bg-blue-100 text-blue-800"
                            : event.status === "ongoing"
                            ? "bg-yellow-100 text-yellow-800"
                            : event.status === "completed"
                            ? "bg-green-100 text-green-800"
                            : "bg-red-100 text-red-800"
                        }`}
                      >
                        {event.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {event.registrations?.length || 0} /{" "}
                      {event.max_participants || "∞"}
                    </td>
                    <td className="px-6 py-4 text-sm space-x-2">
                      {event.status === "draft" && (
                        <>
                          <button
                            onClick={() => handleEdit(event)}
                            className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-xs font-medium transition"
                          >
                            Edit
                          </button>
                          <button
                            onClick={() =>
                              handleStatusChange(event.id, "scheduled")
                            }
                            className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-xs font-medium transition"
                          >
                            Schedule
                          </button>
                        </>
                      )}
                      {event.status === "scheduled" && (
                        <button
                          onClick={() =>
                            handleStatusChange(event.id, "ongoing")
                          }
                          className="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded text-xs font-medium transition"
                        >
                          Start
                        </button>
                      )}
                      {event.status === "ongoing" && (
                        <button
                          onClick={() =>
                            handleStatusChange(event.id, "completed")
                          }
                          className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-xs font-medium transition"
                        >
                          Complete
                        </button>
                      )}
                      {event.status === "draft" && (
                        <button
                          onClick={() => handleDelete(event.id)}
                          className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-xs font-medium transition"
                        >
                          Delete
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default EventManagement;
