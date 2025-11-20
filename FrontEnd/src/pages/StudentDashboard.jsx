import React, { useEffect, useState } from "react";
import api from "../api";
import EventCard from "../components/EventCard";

const StudentDashboard = () => {
  const [events, setEvents] = useState([]);
  const [points, setPoints] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      const eventsResponse = await api.get("/events");
      const pointsResponse = await api.get("/aicte-points");
      setEvents(eventsResponse.data);
      setPoints(pointsResponse.data.total_points);
    };

    fetchData();
  }, []);

  const handleRegister = async (eventId) => {
    try {
      await api.post(`/events/${eventId}/register`);
      alert("Registered successfully!");
    } catch (error) {
      console.error("Registration failed:", error);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Welcome to the Student Dashboard</h1>
      <h2 className="text-xl mb-4">Your AICTE Points: {points}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {events.length > 0 ? (
          events.map((event) => <EventCard key={event.id} event={event} onRegister={handleRegister} />)
        ) : (
          <p>No events available at the moment.</p>
        )}
      </div>
    </div>
  );
};

export default StudentDashboard;
