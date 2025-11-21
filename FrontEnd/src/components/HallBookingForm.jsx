import React, { useState, useEffect } from "react";
import api from "../api";

const HallBookingForm = ({ onBookingCreated }) => {
  const [halls, setHalls] = useState([]);
  const [availableHalls, setAvailableHalls] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [formData, setFormData] = useState({
    hall: "",
    booking_date: "",
    start_time: "",
    end_time: "",
    purpose: "",
  });

  useEffect(() => {
    // Fetch all halls on component mount
    const fetchHalls = async () => {
      try {
        const response = await api.get("/halls/");
        setHalls(response.data);
      } catch (err) {
        console.error("Failed to load halls:", err);
      }
    };

    fetchHalls();
  }, []);

  // Fetch available halls when date/time changes
  useEffect(() => {
    const fetchAvailableHalls = async () => {
      if (
        !formData.booking_date ||
        !formData.start_time ||
        !formData.end_time
      ) {
        setAvailableHalls(halls); // Show all halls if date/time not fully specified
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
        console.error("Failed to fetch available halls:", err);
        setAvailableHalls(halls); // Fallback to all halls
      }
    };

    fetchAvailableHalls();
  }, [formData.booking_date, formData.start_time, formData.end_time, halls]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    if (
      !formData.hall ||
      !formData.booking_date ||
      !formData.start_time ||
      !formData.end_time
    ) {
      setError("Please fill in all required fields");
      setLoading(false);
      return;
    }

    try {
      const response = await api.post("/hall-bookings/", formData);
      setSuccess("Booking created successfully!");
      onBookingCreated(response.data);
      setFormData({
        hall: "",
        booking_date: "",
        start_time: "",
        end_time: "",
        purpose: "",
      });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          "Failed to create booking. Please check for conflicts."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
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

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Booking Date <span className="text-red-500">*</span>
        </label>
        <input
          type="date"
          name="booking_date"
          onChange={handleChange}
          value={formData.booking_date}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Start Time <span className="text-red-500">*</span>
          </label>
          <input
            type="time"
            name="start_time"
            onChange={handleChange}
            value={formData.start_time}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            End Time <span className="text-red-500">*</span>
          </label>
          <input
            type="time"
            name="end_time"
            onChange={handleChange}
            value={formData.end_time}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Hall <span className="text-red-500">*</span>
        </label>
        {formData.booking_date && formData.start_time && formData.end_time ? (
          <>
            {availableHalls.length > 0 ? (
              <select
                name="hall"
                onChange={handleChange}
                value={formData.hall}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select an available hall</option>
                {availableHalls.map((hall) => (
                  <option key={hall.id} value={hall.id}>
                    {hall.name} (Capacity: {hall.capacity}) - {hall.location}
                  </option>
                ))}
              </select>
            ) : (
              <div className="w-full px-3 py-2 border border-red-300 rounded-lg bg-red-50 text-red-700 text-sm">
                No halls available for the selected date and time.
              </div>
            )}
          </>
        ) : (
          <select
            name="hall"
            onChange={handleChange}
            value={formData.hall}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">
              Select date and time first to see available halls
            </option>
            {halls.map((hall) => (
              <option key={hall.id} value={hall.id}>
                {hall.name} (Capacity: {hall.capacity}) - {hall.location}
              </option>
            ))}
          </select>
        )}
        {availableHalls.length > 0 && (
          <p className="text-xs text-green-600 mt-1">
            ✓ {availableHalls.length} hall(s) available for selected date/time
          </p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Purpose
        </label>
        <textarea
          name="purpose"
          onChange={handleChange}
          value={formData.purpose}
          placeholder="Describe the purpose of the booking"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          rows="3"
        />
      </div>

      <button
        type="submit"
        disabled={loading || availableHalls.length === 0}
        className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-400 transition-colors font-medium"
      >
        {loading ? "Creating Booking..." : "Create Booking"}
      </button>
    </form>
  );
};

export default HallBookingForm;
