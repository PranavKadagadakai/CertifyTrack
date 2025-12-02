import React, { useEffect, useState } from "react";
import api from "../api";
import HallBookingForm from "../components/HallBookingForm";
import EventManagement from "../components/EventManagement";

const ClubDashboard = () => {
  const [bookings, setBookings] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("events"); // 'events' or 'bookings'

  const fetchData = async () => {
    try {
      const [bookingsResponse, eventsResponse] = await Promise.all([
        api.get("/hall-bookings/"),
        api.get("/events/"),
      ]);
      setBookings(bookingsResponse.data);
      setEvents(eventsResponse.data);
    } catch (error) {
      console.error("Failed to fetch data:", error);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      try {
        await fetchData();
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Check if hall booking is handled automatically through events
  const hasAutomaticHallBookings = events.some(
    (event) => event.assigned_hall || event.primary_hall || event.secondary_hall
  );

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-2 text-gray-900">
          Club Organizer Dashboard
        </h1>
        <p className="text-gray-600 mb-6">
          Manage your club events and hall bookings
        </p>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 border-b border-gray-300">
          <button
            onClick={() => setActiveTab("events")}
            className={`px-4 py-3 font-medium transition ${
              activeTab === "events"
                ? "border-b-2 border-blue-500 text-blue-600"
                : "text-gray-600 hover:text-gray-900"
            }`}
          >
            📅 Events Management
          </button>
          <button
            onClick={() => setActiveTab("bookings")}
            className={`px-4 py-3 font-medium transition ${
              activeTab === "bookings"
                ? "border-b-2 border-blue-500 text-blue-600"
                : "text-gray-600 hover:text-gray-900"
            }`}
          >
            🏛️ Hall Bookings
          </button>
        </div>

        {/* Events Tab */}
        {activeTab === "events" && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <EventManagement
              onEventCreated={(event) => {
                if (event && event.id) {
                  fetchData();
                }
              }}
              onEventUpdated={(event) => {
                fetchData();
              }}
            />
          </div>
        )}

        {/* Bookings Tab */}
        {activeTab === "bookings" && (
          <div
            className={`grid gap-6 ${
              hasAutomaticHallBookings
                ? "grid-cols-1 max-w-4xl mx-auto"
                : "grid-cols-1 lg:grid-cols-2"
            }`}
          >
            {/* Hall Bookings List */}
            <div
              className={`bg-white p-6 rounded-lg shadow-lg ${
                hasAutomaticHallBookings ? "col-span-full" : ""
              }`}
            >
              <h2 className="text-2xl font-semibold mb-4 text-gray-800">
                {hasAutomaticHallBookings
                  ? "Hall Booking Status"
                  : "Your Hall Bookings"}
              </h2>

              {hasAutomaticHallBookings && (
                <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                  <p className="text-sm text-blue-800">
                    📝 Hall bookings are managed automatically when scheduling
                    events. Use the Events Management tab to assign halls during
                    event creation.
                  </p>
                </div>
              )}

              {loading ? (
                <div className="text-center py-8 text-gray-500">
                  Loading bookings...
                </div>
              ) : bookings.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  {hasAutomaticHallBookings
                    ? "No hall bookings yet. Assign halls when scheduling events."
                    : "No bookings yet. Create your first booking!"}
                </div>
              ) : (
                <div className="space-y-4">
                  {bookings.map((booking) => (
                    <div
                      key={booking.id}
                      className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition"
                    >
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h3 className="font-semibold text-gray-900">
                            {booking.hall?.name}
                          </h3>
                          {booking.event && (
                            <p className="text-sm text-gray-600">
                              Event: {booking.event.name}
                            </p>
                          )}
                        </div>
                        <span
                          className={`px-2 py-1 rounded text-xs font-semibold ${
                            booking.booking_status === "APPROVED"
                              ? "bg-green-100 text-green-800"
                              : booking.booking_status === "PENDING"
                              ? "bg-yellow-100 text-yellow-800"
                              : booking.booking_status === "REJECTED"
                              ? "bg-red-100 text-red-800"
                              : "bg-gray-100 text-gray-800"
                          }`}
                        >
                          {booking.booking_status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">
                        📍 {booking.hall?.location}
                      </p>
                      <p className="text-sm text-gray-600">
                        📅 {new Date(booking.booking_date).toLocaleDateString()}
                      </p>
                      <p className="text-sm text-gray-600">
                        🕐 {booking.start_time} - {booking.end_time}
                      </p>
                      <p className="text-sm text-gray-600 mt-2">
                        Capacity: {booking.hall?.capacity} seats
                      </p>
                      {booking.booking_status === "REJECTED" &&
                        booking.rejection_reason && (
                          <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-xs text-red-700">
                            Reason: {booking.rejection_reason}
                          </div>
                        )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Manual Hall Booking Form - Only show if no automatic bookings */}
            {!hasAutomaticHallBookings && (
              <div className="bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-2xl font-semibold mb-4 text-gray-800">
                  Create Hall Booking
                </h2>
                <HallBookingForm
                  onBookingCreated={(newBooking) => {
                    setBookings((prev) => [...prev, newBooking]);
                  }}
                />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ClubDashboard;
