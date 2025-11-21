import React, { useEffect, useState } from "react";
import api from "../api";
import EventCard from "../components/EventCard";

const StudentDashboard = () => {
  const [events, setEvents] = useState([]);
  const [points, setPoints] = useState(0);

  useEffect(() => {
    api
      .get("/aicte-transactions/")
      .then((res) => {
        // Calculate total points from transactions
        const total = res.data.reduce((sum, tx) => {
          if (tx.status === "APPROVED") {
            return sum + (tx.points || 0);
          }
          return sum;
        }, 0);
        setPoints(total);
      })
      .catch((err) => {
        if (err.response?.status === 404) {
          setPoints(0);
          console.warn("Student profile missing — new account?");
        } else {
          console.error(err);
        }
      });
  }, []);

  const handleRegister = async (eventId) => {
    try {
      await api.post(`/events/${eventId}/register/`);
      alert("Registered successfully!");
    } catch (error) {
      console.error("Registration failed:", error);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">
        Welcome to the Student Dashboard
      </h1>
      <h2 className="text-xl mb-4">Your AICTE Points: {points}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {events.length > 0 ? (
          events.map((event) => (
            <EventCard
              key={event.id}
              event={event}
              onRegister={handleRegister}
            />
          ))
        ) : (
          <p>No events available at the moment.</p>
        )}
      </div>
    </div>
  );
};

export default StudentDashboard;
