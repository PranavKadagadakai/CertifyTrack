import React, { useState, useEffect } from "react";
import api from "../api";
import EventCard from "../components/EventCard";

const StudentDashboard = () => {
  const [stats, setStats] = useState(null);
  const [events, setEvents] = useState([]);
  const [certificates, setCertificates] = useState([]);
  const [points, setPoints] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchDashboardData();
    fetchAICTEPoints();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, eventsRes, certRes] = await Promise.all([
        api.get("/dashboard/stats/"),
        api.get("/events/"),
        api.get("/certificates/"),
      ]);

      setStats(statsRes.data);
      setEvents(eventsRes.data);
      setCertificates(certRes.data);
    } catch (err) {
      setError("Failed to load dashboard data");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAICTEPoints = async () => {
    try {
      const res = await api.get("/aicte-transactions/");
      const totalPoints = res.data.reduce((sum, tx) => {
        if (tx.status === "APPROVED") return sum + (tx.points || 0);
        return sum;
      }, 0);
      setPoints(totalPoints);
    } catch (err) {
      if (err.response?.status === 404) {
        setPoints(0);
      } else {
        console.error(err);
      }
    }
  };

  const handleRegister = async (eventId) => {
    try {
      await api.post(`/events/${eventId}/register/`);
      alert("Registered successfully!");
      fetchDashboardData();
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
      console.error(err);
    }
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Student Dashboard</h1>

      {error && (
        <div className="mb-4 p-4 bg-red-100 text-red-700 rounded">{error}</div>
      )}

      {stats && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-6 rounded shadow">
            <p className="text-gray-600">AICTE Points</p>
            <p className="text-3xl font-bold text-blue-600">{points}</p>
          </div>
          <div className="bg-white p-6 rounded shadow">
            <p className="text-gray-600">Events Registered</p>
            <p className="text-3xl font-bold text-green-600">
              {stats.events_registered}
            </p>
          </div>
          <div className="bg-white p-6 rounded shadow">
            <p className="text-gray-600">Certificates Earned</p>
            <p className="text-3xl font-bold text-purple-600">
              {stats.certificates_earned}
            </p>
          </div>
          <div className="bg-white p-6 rounded shadow">
            <p className="text-gray-600">Pending Approvals</p>
            <p className="text-3xl font-bold text-orange-600">
              {stats.pending_approvals}
            </p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">Available Events</h2>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {events
              .filter((e) => e.status === "scheduled")
              .slice(0, 5)
              .map((event) => (
                <EventCard
                  key={event.id}
                  event={event}
                  onRegister={handleRegister}
                />
              ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">Recent Certificates</h2>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {certificates.slice(0, 5).map((cert) => (
              <div key={cert.id} className="p-4 border rounded">
                <h3 className="font-bold">{cert.event_name}</h3>
                <p className="text-sm text-gray-600">
                  Issued: {new Date(cert.issue_date).toLocaleDateString()}
                </p>
                <a
                  href={cert.file}
                  download
                  className="mt-2 inline-block px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                >
                  Download
                </a>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;
