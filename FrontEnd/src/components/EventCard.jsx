import React, { useState } from "react";

const EventCard = ({ event, onRegister }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [registered, setRegistered] = useState(false);

  const handleRegister = async () => {
    setIsRegistering(true);
    try {
      await onRegister(event.id);
      setRegistered(true);
    } catch (error) {
      console.error("Registration failed:", error);
    } finally {
      setIsRegistering(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    return new Date(dateString).toLocaleDateString("en-IN");
  };

  return (
    <div className="border border-gray-300 p-5 rounded-lg shadow-md hover:shadow-lg transition-shadow bg-white">
      <div className="mb-3">
        <h3 className="text-lg font-bold text-gray-800">{event.name}</h3>
        <span className="inline-block text-xs font-semibold px-2 py-1 bg-blue-100 text-blue-800 rounded mt-2">
          {event.status || "Scheduled"}
        </span>
      </div>
      <p className="text-gray-600 text-sm mb-3">{event.description}</p>
      <div className="space-y-1 text-sm text-gray-700 mb-4">
        <p>
          <strong>📅 Date:</strong> {formatDate(event.event_date)}
        </p>
        {event.start_time && event.end_time && (
          <p>
            <strong>🕐 Time:</strong> {event.start_time} - {event.end_time}
          </p>
        )}
        {event.location && (
          <p>
            <strong>📍 Location:</strong> {event.location}
          </p>
        )}
        {event.max_attendees && (
          <p>
            <strong>👥 Capacity:</strong> {event.max_attendees}
          </p>
        )}
      </div>
      <button
        className={`w-full px-4 py-2 rounded font-medium transition-colors ${
          registered
            ? "bg-green-500 text-white cursor-not-allowed"
            : isRegistering
            ? "bg-blue-400 text-white cursor-wait"
            : "bg-blue-600 text-white hover:bg-blue-700"
        }`}
        onClick={handleRegister}
        disabled={isRegistering || registered}
      >
        {registered
          ? "✓ Registered"
          : isRegistering
          ? "Registering..."
          : "Register"}
      </button>
    </div>
  );
};

export default EventCard;
