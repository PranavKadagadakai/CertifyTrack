import React, { useState, useEffect } from "react";
import api from "../api";

function StudentDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/dashboard/")
      .then((res) => {
        setData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to fetch dashboard data.");
        setLoading(false);
      });
  }, []);

  const handleRegister = async (eventId) => {
    try {
      await api.post(`/events/${eventId}/register/`);
      // Refetch data to update lists
      const res = await api.get("/dashboard/");
      setData(res.data);
      alert("Successfully registered for the event!");
    } catch (err) {
      alert(err.response?.data?.error || "Failed to register for the event.");
    }
  };

  if (loading) return <p>Loading dashboard...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Student Dashboard</h1>
      <p>Welcome, {data.profile.profile.full_name}!</p>
      <p>AICTE Points: {data.profile.profile.aicte_points}</p>

      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Available Events</h2>
        {data.available_events.length > 0 ? (
          <ul className="space-y-4">
            {data.available_events.map((event) => (
              <li key={event.id} className="p-4 bg-white rounded-lg shadow">
                <h3 className="text-xl font-bold">{event.name}</h3>
                <p>Date: {event.date}</p>
                <p>{event.description}</p>
                <button
                  onClick={() => handleRegister(event.id)}
                  className="mt-2 px-4 py-2 text-white bg-blue-600 rounded hover:bg-blue-700"
                >
                  Register
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p>No new events available.</p>
        )}
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">
          Your Registered Events & Certificates
        </h2>
        {/* Logic to display registered events and certificates */}
      </div>
    </div>
  );
}

export default StudentDashboard;
