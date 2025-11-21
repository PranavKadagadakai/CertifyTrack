import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import AdminUserManagement from "../components/AdminUserManagement";
import AdminClubManagement from "../components/AdminClubManagement";
import AdminMenteeAssignment from "../components/AdminMenteeAssignment";
import AdminAICTEConfig from "../components/AdminAICTEConfig";
import AdminReporting from "../components/AdminReporting";

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("overview");
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get("/admin/reports/system_stats/");
      setStats(response.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to load dashboard stats");
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-10">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Manage users, clubs, events, and system settings
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow mb-8 overflow-hidden">
          <div className="flex flex-wrap border-b">
            <button
              onClick={() => setActiveTab("overview")}
              className={`px-6 py-4 font-medium border-b-2 transition ${
                activeTab === "overview"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-600 hover:text-gray-900"
              }`}
            >
              📊 Overview
            </button>
            <button
              onClick={() => setActiveTab("users")}
              className={`px-6 py-4 font-medium border-b-2 transition ${
                activeTab === "users"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-600 hover:text-gray-900"
              }`}
            >
              👥 User Management
            </button>
            <button
              onClick={() => setActiveTab("clubs")}
              className={`px-6 py-4 font-medium border-b-2 transition ${
                activeTab === "clubs"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-600 hover:text-gray-900"
              }`}
            >
              🎯 Club Management
            </button>
            <button
              onClick={() => setActiveTab("mentees")}
              className={`px-6 py-4 font-medium border-b-2 transition ${
                activeTab === "mentees"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-600 hover:text-gray-900"
              }`}
            >
              🤝 Mentee Assignment
            </button>
            <button
              onClick={() => setActiveTab("aicte")}
              className={`px-6 py-4 font-medium border-b-2 transition ${
                activeTab === "aicte"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-600 hover:text-gray-900"
              }`}
            >
              ⭐ AICTE Config
            </button>
            <button
              onClick={() => setActiveTab("reports")}
              className={`px-6 py-4 font-medium border-b-2 transition ${
                activeTab === "reports"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-600 hover:text-gray-900"
              }`}
            >
              📈 Reports
            </button>
          </div>
        </div>

        {/* Tab Content */}
        <div>
          {activeTab === "overview" && stats && (
            <div>
              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="text-gray-600 text-sm font-medium">
                    Total Users
                  </div>
                  <div className="text-3xl font-bold text-blue-600 mt-2">
                    {stats.total_users}
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="text-gray-600 text-sm font-medium">
                    Total Students
                  </div>
                  <div className="text-3xl font-bold text-green-600 mt-2">
                    {stats.total_students}
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="text-gray-600 text-sm font-medium">
                    Total Mentors
                  </div>
                  <div className="text-3xl font-bold text-purple-600 mt-2">
                    {stats.total_mentors}
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
                  <div className="text-gray-600 text-sm font-medium">
                    Total Clubs
                  </div>
                  <div className="text-3xl font-bold text-orange-600 mt-2">
                    {stats.total_clubs}
                  </div>
                </div>
              </div>

              {/* User Breakdown */}
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
                  <div className="text-gray-600 text-sm font-medium">
                    Total Events
                  </div>
                  <div className="text-3xl font-bold text-indigo-600 mt-2">
                    {stats.total_events}
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="text-gray-600 text-sm font-medium">
                    Certificates Issued
                  </div>
                  <div className="text-3xl font-bold text-teal-600 mt-2">
                    {stats.total_certificates_issued}
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="text-gray-600 text-sm font-medium">
                    Active Bookings
                  </div>
                  <div className="text-3xl font-bold text-pink-600 mt-2">
                    {stats.active_bookings}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "users" && <AdminUserManagement />}
          {activeTab === "clubs" && <AdminClubManagement />}
          {activeTab === "mentees" && <AdminMenteeAssignment />}
          {activeTab === "aicte" && <AdminAICTEConfig />}
          {activeTab === "reports" && <AdminReporting />}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
