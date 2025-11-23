import React, { useState, useEffect } from "react";
import api from "../api";

const HallBookingForm = ({ onBookingCreated }) => {
  const [halls, setHalls] = useState([]);
  const [availableHalls, setAvailableHalls] = useState([]);
  const [events, setEvents] = useState([]);
  const [bookings, setBookings] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [formData, setFormData] = useState({
    hall: "",
    event: "",
    booking_date: "",
    start_time: "",
    end_time: "",
    purpose: "",
  });

  // Load halls, events, bookings
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [hallsRes, eventsRes, bookingsRes] = await Promise.all([
          api.get("/halls/"),
          api.get("/events/?club=true"),
          api.get("/hall-bookings/?club=true"),
        ]);

        setHalls(hallsRes.data);
        setEvents(eventsRes.data);
        setBookings(bookingsRes.data);
      } catch (err) {
        setError("Failed to load initial data");
      }
    };

    loadInitialData();
  }, []);

  // Auto-fetch available halls
  useEffect(() => {
    const loadAvailability = async () => {
      if (
        !formData.booking_date ||
        !formData.start_time ||
        !formData.end_time
      ) {
        setAvailableHalls(halls);
        return;
      }

      try {
        const response = await api.get("/halls/available/", {
          params: {
            date: formData.booking_date,
            start_time: formData.start_time,
            end_time: formData.end_time,
          },
        });
        setAvailableHalls(response.data);
      } catch (err) {
        setAvailableHalls(halls);
      }
    };

    loadAvailability();
  }, [formData.booking_date, formData.start_time, formData.end_time, halls]);

  // Change handler
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    if (!formData.event) {
      setError("Event selection is required");
      setLoading(false);
      return;
    }

    try {
      const response = await api.post("/hall-bookings/", formData);

      setSuccess("Booking created successfully!");

      if (onBookingCreated) onBookingCreated(response.data);

      setFormData({
        hall: "",
        event: "",
        booking_date: "",
        start_time: "",
        end_time: "",
        purpose: "",
      });

      const bookingsRes = await api.get("/hall-bookings/?club=true");
      setBookings(bookingsRes.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          "Failed to create booking"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-6">Hall Booking</h2>

      {error && (
        <div className="p-4 bg-red-100 border border-red-300 text-red-700 rounded mb-4">
          {error}
        </div>
      )}

      {success && (
        <div className="p-4 bg-green-100 border border-green-300 text-green-700 rounded mb-4">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4 mb-8">
        {/* Event Selection */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Select Event <span className="text-red-500">*</span>
          </label>
          <select
            name="event"
            value={formData.event}
            onChange={handleChange}
            required
            className="w-full p-2 border rounded"
          >
            <option value="">Choose an event</option>
            {events
              .filter((e) => e.status === "draft" || e.status === "scheduled")
              .map((event) => (
                <option key={event.id} value={event.id}>
                  {event.name} —{" "}
                  {new Date(event.event_date).toLocaleDateString()}
                </option>
              ))}
          </select>
        </div>

        {/* Booking Date */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Booking Date <span className="text-red-500">*</span>
          </label>
          <input
            type="date"
            name="booking_date"
            value={formData.booking_date}
            onChange={handleChange}
            required
            className="w-full p-2 border rounded"
          />
        </div>

        {/* Time Inputs */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Start Time <span className="text-red-500">*</span>
            </label>
            <input
              type="time"
              name="start_time"
              value={formData.start_time}
              onChange={handleChange}
              required
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              End Time <span className="text-red-500">*</span>
            </label>
            <input
              type="time"
              name="end_time"
              value={formData.end_time}
              onChange={handleChange}
              required
              className="w-full p-2 border rounded"
            />
          </div>
        </div>

        {/* Hall Selection */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Hall <span className="text-red-500">*</span>
          </label>

          <select
            name="hall"
            value={formData.hall}
            onChange={handleChange}
            required
            className="w-full p-2 border rounded"
          >
            <option value="">
              {formData.booking_date && formData.start_time && formData.end_time
                ? "Select available hall"
                : "Select date/time to load availability"}
            </option>

            {availableHalls.map((hall) => (
              <option key={hall.id} value={hall.id}>
                {hall.name} (Capacity: {hall.capacity})
              </option>
            ))}
          </select>
        </div>

        {/* Purpose */}
        <div>
          <label className="block text-sm font-medium mb-2">Purpose</label>
          <textarea
            name="purpose"
            value={formData.purpose}
            onChange={handleChange}
            rows={3}
            placeholder="Describe the purpose of the booking"
            className="w-full p-2 border rounded"
          />
        </div>

        <button
          type="submit"
          disabled={loading || availableHalls.length === 0}
          className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-blue-400"
        >
          {loading ? "Booking..." : "Create Booking"}
        </button>
      </form>

      {/* My Bookings */}
      <div className="space-y-4">
        <h3 className="text-xl font-semibold">My Bookings</h3>

        {bookings.map((booking) => (
          <div key={booking.id} className="p-4 border rounded bg-gray-50">
            <h4 className="font-bold">
              {booking.hall_name} — {booking.event_name}
            </h4>
            <p className="text-sm text-gray-600">
              {new Date(booking.booking_date).toLocaleDateString()} |{" "}
              {booking.start_time} — {booking.end_time}
            </p>

            <span
              className={`px-3 py-1 rounded text-sm mt-2 inline-block ${
                booking.booking_status === "APPROVED"
                  ? "bg-green-200 text-green-800"
                  : booking.booking_status === "REJECTED"
                  ? "bg-red-200 text-red-800"
                  : "bg-yellow-200 text-yellow-800"
              }`}
            >
              {booking.booking_status}
            </span>

            {booking.rejection_reason && (
              <p className="text-sm text-red-600 mt-1">
                Reason: {booking.rejection_reason}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default HallBookingForm;
