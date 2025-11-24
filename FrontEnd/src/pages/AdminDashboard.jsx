// FrontEnd/src/pages/AdminDashboard.jsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

import AdminUserManagement from "../components/AdminUserManagement";
import AdminClubManagement from "../components/AdminClubManagement";
import AdminMenteeAssignment from "../components/AdminMenteeAssignment";
import AdminAICTEConfig from "../components/AdminAICTEConfig";
import AdminReporting from "../components/AdminReporting";
import AdminHallBookings from "../components/AdminHallBookings";

const AdminDashboard = () => {
  const navigate = useNavigate();

  // Tabs
  const [activeTab, setActiveTab] = useState("overview");

  // Overview Stats
  const [stats, setStats] = useState(null);
  const [loadingStats, setLoadingStats] = useState(true);
  const [error, setError] = useState("");

  // Hall Booking Approval
  const [pendingBookings, setPendingBookings] = useState([]);
  const [loadingBookings, setLoadingBookings] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    fetchStats();
    fetchPendingBookings();
  }, []);

  // Fetch Main Dashboard Stats
  const fetchStats = async () => {
    try {
      const response = await api.get("/admin/reports/system_stats/");
      setStats(response.data);
    } catch (err) {
      setError("Failed to load dashboard stats");
    } finally {
      setLoadingStats(false);
    }
  };

  // Fetch Pending Bookings
  const fetchPendingBookings = async () => {
    try {
      setLoadingBookings(true);
      const res = await api.get("/hall-bookings/list_admin_pending/");
      setPendingBookings(res.data);
    } catch (err) {
      setError("Failed to load pending bookings");
    } finally {
      setLoadingBookings(false);
    }
  };

  // Approve Booking
  const handleApprove = async (bookingId) => {
    setActionLoading(true);
    try {
      await api.post(`/hall-bookings/${bookingId}/approve/`);
      setPendingBookings((prev) => prev.filter((b) => b.id !== bookingId));
    } catch (err) {
      alert(err?.response?.data?.error || "Failed to approve booking");
    } finally {
      setActionLoading(false);
    }
  };

  // Reject Booking
  const handleReject = async (bookingId) => {
    const reason = prompt("Enter rejection reason (min 5 characters):");
    if (!reason || reason.length < 5) {
      alert("Please provide a valid rejection reason.");
      return;
    }
    setActionLoading(true);
    try {
      await api.post(`/hall-bookings/${bookingId}/reject/`, { reason });
      setPendingBookings((prev) => prev.filter((b) => b.id !== bookingId));
    } catch (err) {
      alert(err?.response?.data?.error || "Failed to reject booking");
    } finally {
      setActionLoading(false);
    }
  };

  if (loadingStats) {
    return <div className="text-center py-10">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Manage users, clubs, events, hall bookings, and system configuration
          </p>
        </div>
      </div>

      {/* Main Container */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow mb-8 overflow-hidden">
          <div className="flex flex-wrap border-b">
            {[
              ["overview", "📊 Overview"],
              ["users", "👥 User Management"],
              ["clubs", "🎯 Club Management"],
              ["mentees", "🤝 Mentee Assignment"],
              ["aicte", "⭐ AICTE Config"],
              ["hall_bookings", "🏛 Hall Bookings"],
              ["reports", "📈 Reports"],
            ].map(([tabKey, label]) => (
              <button
                key={tabKey}
                onClick={() => setActiveTab(tabKey)}
                className={`px-6 py-4 font-medium border-b-2 transition ${
                  activeTab === tabKey
                    ? "border-blue-600 text-blue-600"
                    : "border-transparent text-gray-600 hover:text-gray-900"
                }`}
              >
                {label}
              </button>
            ))}
          </div>
        </div>

        {/* TAB CONTENT */}
        <div>
          {/* OVERVIEW TAB */}
          {activeTab === "overview" && stats && (
            <div>
              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="text-gray-600 text-sm">Total Users</div>
                  <div className="text-3xl font-bold text-blue-600 mt-2">
                    {stats.total_users}
                  </div>
                </div>

                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="text-gray-600 text-sm">Total Students</div>
                  <div className="text-3xl font-bold text-green-600 mt-2">
                    {stats.total_students}
                  </div>
                </div>

                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="text-gray-600 text-sm">Total Mentors</div>
                  <div className="text-3xl font-bold text-purple-600 mt-2">
                    {stats.total_mentors}
                  </div>
                </div>

                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="text-gray-600 text-sm">Total Clubs</div>
                  <div className="text-3xl font-bold text-orange-600 mt-2">
                    {stats.total_clubs}
                  </div>
                </div>
              </div>

              {/* Breakdown */}
              <div className="bg-white p-6 rounded-lg shadow">
                <h2 className="text-xl font-bold mb-6">User Breakdown</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {stats.user_breakdown.students}
                    </div>
                    <div className="text-gray-600 text-sm">Students</div>
                  </div>

                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">
                      {stats.user_breakdown.mentors}
                    </div>
                    <div className="text-gray-600 text-sm">Mentors</div>
                  </div>

                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">
                      {stats.user_breakdown.club_organizers}
                    </div>
                    <div className="text-gray-600 text-sm">Club Organizers</div>
                  </div>

                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600">
                      {stats.user_breakdown.admins}
                    </div>
                    <div className="text-gray-600 text-sm">Admins</div>
                  </div>
                </div>
              </div>

              {/* Quick Stats */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="text-gray-600 text-sm">Total Events</div>
                  <div className="text-3xl font-bold text-indigo-600 mt-2">
                    {stats.total_events}
                  </div>
                </div>

                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="text-gray-600 text-sm">
                    Certificates Issued
                  </div>
                  <div className="text-3xl font-bold text-teal-600 mt-2">
                    {stats.total_certificates_issued}
                  </div>
                </div>

                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="text-gray-600 text-sm">Active Bookings</div>
                  <div className="text-3xl font-bold text-pink-600 mt-2">
                    {stats.active_bookings}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* USER MANAGEMENT */}
          {activeTab === "users" && <AdminUserManagement />}

          {/* CLUB MANAGEMENT */}
          {activeTab === "clubs" && <AdminClubManagement />}

          {/* MENTEE ASSIGNMENT */}
          {activeTab === "mentees" && <AdminMenteeAssignment />}

          {/* AICTE CONFIG */}
          {activeTab === "aicte" && <AdminAICTEConfig />}

          {/* NEW TAB — HALL BOOKINGS */}
          {activeTab === "hall_bookings" && <AdminHallBookings />}

          {/* REPORTS */}
          {activeTab === "reports" && <AdminReporting />}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
