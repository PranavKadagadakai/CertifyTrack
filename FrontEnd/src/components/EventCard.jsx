import React, { useState } from "react";

const EventCard = ({ event, onRegister, onCancelRegistration }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [isCancelling, setIsCancelling] = useState(false);

  const handleRegister = async () => {
    setIsRegistering(true);
    try {
      await onRegister(event.id);
    } catch (error) {
      console.error("Registration failed:", error);
    } finally {
      setIsRegistering(false);
    }
  };

  const handleCancel = async () => {
    setIsCancelling(true);
    try {
      await onCancelRegistration(event.id);
    } catch (error) {
      console.error("Cancellation failed:", error);
    } finally {
      setIsCancelling(false);
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
        <div className="flex gap-2 mt-2">
          <span className="inline-block text-xs font-semibold px-2 py-1 bg-blue-100 text-blue-800 rounded">
            {event.status || "Scheduled"}
          </span>
          {event.registration_status && (
            <span
              className={`inline-block text-xs font-semibold px-2 py-1 rounded ${
                event.registration_status === "ATTENDED"
                  ? "bg-green-100 text-green-800"
                  : event.registration_status === "REGISTERED"
                  ? "bg-yellow-100 text-yellow-800"
                  : event.registration_status === "CANCELLED"
                  ? "bg-red-100 text-red-800"
                  : "bg-gray-100 text-gray-800"
              }`}
            >
              {event.registration_status === "ATTENDED"
                ? "✓ Attended"
                : event.registration_status === "REGISTERED"
                ? "✓ Registered"
                : event.registration_status === "CANCELLED"
                ? "✗ Cancelled"
                : event.registration_status}
            </span>
          )}
        </div>
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
      {/* Action Buttons */}
      {!event.registration_status ? (
        /* Not registered - show register button */
        <button
          className={`w-full px-4 py-2 rounded font-medium transition-colors ${
            isRegistering
              ? "bg-blue-400 text-white cursor-wait"
              : "bg-blue-600 text-white hover:bg-blue-700"
          }`}
          onClick={handleRegister}
          disabled={isRegistering}
        >
          {isRegistering ? "Registering..." : "Register"}
        </button>
      ) : event.registration_status === "REGISTERED" ? (
        /* Registered - show cancel button */
        <button
          className={`w-full px-4 py-2 rounded font-medium transition-colors ${
            isCancelling
              ? "bg-red-400 text-white cursor-wait"
              : "bg-red-600 text-white hover:bg-red-700"
          }`}
          onClick={handleCancel}
          disabled={isCancelling}
        >
          {isCancelling ? "Cancelling..." : "Cancel Registration"}
        </button>
      ) : event.registration_status === "ATTENDED" ? (
        /* Attended - show attended message */
        <div className="w-full px-4 py-2 rounded font-medium bg-green-600 text-white text-center">
          ✓ Event Attended
        </div>
      ) : event.registration_status === "CANCELLED" ? (
        /* Cancelled - show re-register option if still available */
        event.status === "scheduled" ? (
          <button
            className={`w-full px-4 py-2 rounded font-medium transition-colors ${
              isRegistering
                ? "bg-blue-400 text-white cursor-wait"
                : "bg-gray-600 text-white hover:bg-gray-700"
            }`}
            onClick={handleRegister}
            disabled={isRegistering}
          >
            {isRegistering ? "Re-registering..." : "Re-register"}
          </button>
        ) : (
          <div className="w-full px-4 py-2 rounded font-medium bg-gray-400 text-white text-center">
            Registration Cancelled
          </div>
        )
      ) : (
        /* Other statuses - show status message */
        <div className="w-full px-4 py-2 rounded font-medium bg-gray-400 text-white text-center">
          {event.registration_status}
        </div>
      )}
    </div>
  );
};

export default EventCard;
