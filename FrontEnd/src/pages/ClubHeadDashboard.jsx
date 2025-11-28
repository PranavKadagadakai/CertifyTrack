import React, { useState, useEffect } from "react";
import api from "../api";
import { useAuth } from "../context/AuthContext";

const ClubHeadDashboard = () => {
  const [clubs, setClubs] = useState([]);
  const [selectedClub, setSelectedClub] = useState(null);
  const [clubEvents, setClubEvents] = useState([]);
  const user = useAuth().user;
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [stats, setStats] = useState({
    totalEvents: 0,
    activeEvents: 0,
    totalMembers: 0,
    completedEvents: 0,
  });

  useEffect(() => {
    fetchClubs();
  }, []);

  useEffect(() => {
    if (selectedClub) {
      fetchClubData();
    }
  }, [selectedClub]);

  const fetchClubs = async () => {
    try {
      setLoading(true);
      const response = await api.get("/clubs/");

      // Handle both paginated and non-paginated responses
      const allClubs = response.data.results || response.data || [];
      const currentUserId = getCurrentUserId();

      // Filter clubs where current user is club head (handle both int and string IDs)
      const userClubs = allClubs.filter(
        (club) => parseInt(club.club_head) === parseInt(currentUserId)
      );

      setClubs(userClubs);

      // Auto-select first club if available
      if (userClubs.length > 0) {
        setSelectedClub(userClubs[0]);
      }

      setLoading(false);
    } catch (err) {
      console.error("Failed to load clubs:", err);
      setError("Failed to load clubs");
      setLoading(false);
    }
  };

  const fetchClubData = async () => {
    if (!selectedClub) return;

    try {
      // Fetch club events
      const eventsResponse = await api.get(`/events/?club=${selectedClub.id}`);
      const events = eventsResponse.data.results || eventsResponse.data;

      // Calculate stats
      const totalEvents = events.length;
      const activeEvents = events.filter((event) =>
        ["scheduled", "ongoing"].includes(event.status)
      ).length;
      const completedEvents = events.filter(
        (event) => event.status === "completed"
      ).length;

      setClubEvents(events);
      setStats({
        totalEvents,
        activeEvents,
        completedEvents,
        totalMembers: selectedClub.members?.length || 0,
      });
    } catch (err) {
      console.error("Failed to fetch club data:", err);
    }
  };

  const getCurrentUserId = () => {
    // Use user from AuthContext instead of localStorage
    return user?.id || user?.user?.id;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading)
    return <div className="text-center py-10">Loading dashboard...</div>;

  if (clubs.length === 0) {
    return (
      <div className="text-center py-10">
        <h2 className="text-2xl font-bold text-gray-700 mb-4">
          Club Head Dashboard
        </h2>
        <p className="text-gray-600">
          You are not assigned as a club head for any clubs.
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Contact an administrator to assign you as a club head.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h1 className="text-3xl font-bold text-gray-900">
          Club Head Dashboard
        </h1>
        <p className="text-gray-600 mt-2">
          Manage your club activities and oversee events
        </p>
      </div>

      {/* Club Selection */}
      <div className="bg-white p-6 rounded-lg shadow">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Club
        </label>
        <select
          value={selectedClub?.id || ""}
          onChange={(e) => {
            const club = clubs.find((c) => c.id === parseInt(e.target.value));
            setSelectedClub(club);
          }}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
        >
          {clubs.map((club) => (
            <option key={club.id} value={club.id}>
              {club.name}
            </option>
          ))}
        </select>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg
                className="h-8 w-8 text-blue-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Events</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats.totalEvents}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg
                className="h-8 w-8 text-green-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Events</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats.activeEvents}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg
                className="h-8 w-8 text-yellow-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"
                />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Club Members</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats.totalMembers}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg
                className="h-8 w-8 text-purple-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">
                Completed Events
              </p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats.completedEvents}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Events */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Events</h2>
        <div className="space-y-4">
          {clubEvents.length > 0 ? (
            clubEvents.slice(0, 5).map((event) => (
              <div
                key={event.id}
                className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
              >
                <div>
                  <h3 className="text-lg font-medium text-gray-900">
                    {event.name}
                  </h3>
                  <p className="text-sm text-gray-600">
                    Date: {formatDate(event.event_date)}
                  </p>
                  <p className="text-sm text-gray-600">
                    Status: {event.status}
                  </p>
                </div>
                <div
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    event.status === "scheduled"
                      ? "bg-blue-100 text-blue-800"
                      : event.status === "completed"
                      ? "bg-green-100 text-green-800"
                      : event.status === "ongoing"
                      ? "bg-yellow-100 text-yellow-800"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {event.status}
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-600">No events found for this club.</p>
          )}
        </div>
      </div>

      {/* Club Information */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Club Information
        </h2>
        {selectedClub && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Club Name
              </label>
              <p className="text-lg text-gray-900">{selectedClub.name}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Description
              </label>
              <p className="text-gray-600">
                {selectedClub.description || "No description available"}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Coordinator
              </label>
              <p className="text-gray-900">
                {selectedClub.faculty_coordinator_name || "Not assigned"}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Established
              </label>
              <p className="text-gray-900">
                {selectedClub.established_date
                  ? formatDate(selectedClub.established_date)
                  : "Not specified"}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClubHeadDashboard;
