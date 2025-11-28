import React, { useState, useEffect } from "react";
import api from "../api";
import { useAuth } from "../context/AuthContext";

const ClubCoordinatorDashboard = () => {
  const [clubs, setClubs] = useState([]);
  const [selectedClub, setSelectedClub] = useState(null);
  const [clubEvents, setClubEvents] = useState([]);
  const [clubMembers, setClubMembers] = useState([]);
  const user = useAuth().user;
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [stats, setStats] = useState({
    totalEvents: 0,
    pendingApprovals: 0,
    totalMembers: 0,
    activeEvents: 0,
  });

  useEffect(() => {
    fetchCoordinatedClubs();
  }, []);

  useEffect(() => {
    if (selectedClub) {
      fetchClubData();
    }
  }, [selectedClub]);

  const fetchCoordinatedClubs = async () => {
    try {
      setLoading(true);
      const response = await api.get("/clubs/");

      const allClubs = response.data.results || response.data || [];
      const currentUserId = getCurrentUserId();

      // Filter clubs where current user is club head (handle both int and string IDs)
      const userClubs = allClubs.filter(
        (club) => parseInt(club.faculty_coordinator) === parseInt(currentUserId)
      );

      setClubs(userClubs);

      // Auto-select first club if available
      if (userClubs.length > 0) {
        setSelectedClub(userClubs[0]);
      }

      setLoading(false);
    } catch (err) {
      setError("Failed to load clubs");
      setLoading(false);
    }
  };

  const fetchClubData = async () => {
    if (!selectedClub) return;

    try {
      // Fetch club events and members
      const [eventsResponse, membersResponse] = await Promise.all([
        api.get(`/events/?club=${selectedClub.id}`),
        api.get("/club-members/"),
      ]);

      const events = eventsResponse.data.results || eventsResponse.data;
      const allMembers = membersResponse.data.results || membersResponse.data;
      const clubMembers = allMembers.filter(
        (member) => member.club === selectedClub.id
      );

      // Calculate stats
      const totalEvents = events.length;
      const activeEvents = events.filter((event) =>
        ["scheduled", "ongoing"].includes(event.status)
      ).length;

      // Count pending AICTE approvals for club members
      let pendingApprovals = 0;
      for (const member of clubMembers) {
        try {
          const studentId = member.student;
          const pointsResponse = await api.get(
            `/aicte-transactions/?student=${studentId}&status=PENDING`
          );
          pendingApprovals +=
            pointsResponse.data.count || pointsResponse.data.length || 0;
        } catch (err) {
          // Continue if there's an error
        }
      }

      setClubEvents(events);
      setClubMembers(clubMembers);
      setStats({
        totalEvents,
        pendingApprovals,
        totalMembers: clubMembers.length,
        activeEvents,
      });
    } catch (err) {
      console.error("Failed to fetch club data:", err);
    }
  };

  const getCurrentUserId = () => {
    // This should be obtained from auth context
    return user?.id || user?.user?.id;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const approvePoints = async (transactionId) => {
    try {
      await api.post(`/aicte-transactions/${transactionId}/approve/`);
      // Refresh data
      fetchClubData();
    } catch (err) {
      console.error("Failed to approve points:", err);
      alert("Failed to approve points");
    }
  };

  const rejectPoints = async (transactionId) => {
    const reason = prompt("Enter rejection reason:");
    if (!reason) return;

    try {
      await api.post(`/aicte-transactions/${transactionId}/reject/`, {
        reason,
      });
      // Refresh data
      fetchClubData();
    } catch (err) {
      console.error("Failed to reject points:", err);
      alert("Failed to reject points");
    }
  };

  if (loading)
    return <div className="text-center py-10">Loading dashboard...</div>;

  if (clubs.length === 0) {
    return (
      <div className="text-center py-10">
        <h2 className="text-2xl font-bold text-gray-700 mb-4">
          Club Coordinator Dashboard
        </h2>
        <p className="text-gray-600">
          You are not assigned as a faculty coordinator for any clubs.
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Contact an administrator to assign you as a club coordinator.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h1 className="text-3xl font-bold text-gray-900">
          Club Coordinator Dashboard
        </h1>
        <p className="text-gray-600 mt-2">
          Oversee club activities and approve student points
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
                className="h-8 w-8 text-yellow-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">
                Pending Approvals
              </p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats.pendingApprovals}
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
              <p className="text-sm font-medium text-gray-600">Active Events</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats.activeEvents}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Pending AICTE Approvals */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Pending AICTE Point Approvals
        </h2>
        <div className="space-y-4">
          {/* Note: This would need to be implemented with real pending transactions */}
          <div className="text-center py-8 text-gray-600">
            <svg
              className="mx-auto h-12 w-12 text-gray-400 mb-4"
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
            <p className="text-lg">
              Point approval system would be implemented here
            </p>
            <p className="text-sm mt-2">
              This feature requires backend implementation of student point
              tracking
            </p>
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
                    Points: {event.points_awarded} AICTE points
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

      {/* Club Members Overview */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Club Members</h2>
        <div className="space-y-4">
          {clubMembers.length > 0 ? (
            clubMembers.slice(0, 5).map((member) => (
              <div
                key={member.id}
                className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
              >
                <div>
                  <h3 className="text-lg font-medium text-gray-900">
                    {member.student_usn}
                  </h3>
                  <p className="text-sm text-gray-600">
                    Role: {member.role_name}
                  </p>
                  <p className="text-sm text-gray-600">
                    Joined: {formatDate(member.joined_date)}
                  </p>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    member.is_active
                      ? "bg-green-100 text-green-800"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {member.is_active ? "Active" : "Inactive"}
                </span>
              </div>
            ))
          ) : (
            <p className="text-gray-600">No members found for this club.</p>
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
                Club Head
              </label>
              <p className="text-gray-900">
                {selectedClub.club_head_name || "Not assigned"}
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

export default ClubCoordinatorDashboard;
