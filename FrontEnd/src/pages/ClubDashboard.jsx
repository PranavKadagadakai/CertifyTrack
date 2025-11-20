import React, { useEffect, useState } from "react";
import api from "../api";
import HallBookingForm from "../components/HallBookingForm";
import Notifications from "../components/Notifications";

const ClubDashboard = () => {
  const [events, setEvents] = useState([]);
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const eventsResponse = await api.get("/events?club=true");
      const bookingsResponse = await api.get("/hall-bookings?club=true");
      setEvents(eventsResponse.data);
      setBookings(bookingsResponse.data);
    };

    fetchData();
  }, []);

  const handleEventStatus = async (eventId, status) => {
    try {
      await api.patch(`/events/${eventId}`, { status });
      alert(`Event marked as ${status}!`);
      setEvents((prev) =>
        prev.map((event) =>
          event.id === eventId ? { ...event, status } : event
        )
      );
    } catch (error) {
      console.error("Failed to update event status:", error);
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Club Organizer Dashboard</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Events Section */}
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">Your Events</h2>
          <ul className="space-y-4">
            {events.map((event) => (
              <li
                key={event.id}
                className="flex justify-between items-center border-b pb-2"
              >
                <span>
                  {event.name} - {event.status}
                </span>
                {event.status === "draft" && (
                  <button
                    className="bg-blue-500 text-white px-4 py-1 rounded"
                    onClick={() => handleEventStatus(event.id, "scheduled")}
                  >
                    Schedule
                  </button>
                )}
              </li>
            ))}
          </ul>
        </div>

        {/* Hall Bookings Section */}
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">Your Hall Bookings</h2>
          <ul className="space-y-4">
            {bookings.map((booking) => (
              <li key={booking.id} className="border-b pb-2">
                {booking.hall.name} - {booking.booking_date}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Hall Booking Form */}
      <div className="mt-6 bg-white p-4 rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Create a Hall Booking</h2>
        <HallBookingForm
          onBookingCreated={(newBooking) =>
            setBookings((prev) => [...prev, newBooking])
          }
        />
      </div>

      {/* Notifications */}
      <div className="mt-6">
        <Notifications />
      </div>
    </div>
  );
};

export default ClubDashboard;
