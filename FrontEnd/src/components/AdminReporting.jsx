import React, { useState, useEffect } from "react";
import api from "../api";

const AdminReporting = () => {
  const [reports, setReports] = useState({
    system_stats: null,
    user_activity: null,
    event_stats: null,
    hall_utilization: null,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [auditLogs, setAuditLogs] = useState([]);
  const [auditDays, setAuditDays] = useState(30);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      setLoading(true);
      const [systemRes, activityRes, eventsRes, hallRes, auditRes] =
        await Promise.all([
          api.get("/admin/reports/system_stats/"),
          api.get("/admin/reports/user_activity_report/"),
          api.get("/admin/reports/event_statistics/"),
          api.get("/admin/reports/hall_utilization_report/"),
          api.get(`/admin/reports/audit_logs/?days=${auditDays}`),
        ]);

      setReports({
        system_stats: systemRes.data,
        user_activity: activityRes.data,
        event_stats: eventsRes.data,
        hall_utilization: hallRes.data,
      });
      setAuditLogs(auditRes.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to load reports");
      setLoading(false);
    }
  };

  if (loading)
    return <div className="text-center py-10">Loading reports...</div>;

  return (
    <div className="space-y-6">
      {error && (
        <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* System Statistics */}
      {reports.system_stats && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-bold mb-4">System Statistics</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">
                {reports.system_stats.total_users}
              </div>
              <div className="text-gray-600 text-sm">Total Users</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">
                {reports.system_stats.total_students}
              </div>
              <div className="text-gray-600 text-sm">Students</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">
                {reports.system_stats.total_mentors}
              </div>
              <div className="text-gray-600 text-sm">Mentors</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-600">
                {reports.system_stats.total_clubs}
              </div>
              <div className="text-gray-600 text-sm">Clubs</div>
            </div>
          </div>
        </div>
      )}

      {/* User Activity Report */}
      {reports.user_activity && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-bold mb-4">User Activity Report</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="border rounded p-4 text-center">
              <div className="text-2xl font-bold text-green-600">
                {reports.user_activity.verified_users}
              </div>
              <div className="text-gray-600 text-sm">Verified Users</div>
            </div>
            <div className="border rounded p-4 text-center">
              <div className="text-2xl font-bold text-red-600">
                {reports.user_activity.unverified_users}
              </div>
              <div className="text-gray-600 text-sm">Unverified Users</div>
            </div>
            <div className="border rounded p-4 text-center">
              <div className="text-2xl font-bold text-blue-600">
                {reports.user_activity.active_users}
              </div>
              <div className="text-gray-600 text-sm">Active Users</div>
            </div>
            <div className="border rounded p-4 text-center">
              <div className="text-2xl font-bold text-yellow-600">
                {reports.user_activity.inactive_users}
              </div>
              <div className="text-gray-600 text-sm">Inactive Users</div>
            </div>
            <div className="border rounded p-4 text-center">
              <div className="text-2xl font-bold text-red-700">
                {reports.user_activity.locked_users}
              </div>
              <div className="text-gray-600 text-sm">Locked Users</div>
            </div>
          </div>
        </div>
      )}

      {/* Event Statistics */}
      {reports.event_stats && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-bold mb-4">Event Statistics</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="border rounded p-4">
              <div className="text-2xl font-bold text-indigo-600">
                {reports.event_stats.total_events}
              </div>
              <div className="text-gray-600 text-sm">Total Events</div>
            </div>
            <div className="border rounded p-4">
              <div className="text-2xl font-bold text-teal-600">
                {reports.event_stats.total_registrations}
              </div>
              <div className="text-gray-600 text-sm">Total Registrations</div>
            </div>
            <div className="border rounded p-4">
              <div className="text-2xl font-bold text-emerald-600">
                {reports.event_stats.attendance_rate.attended}
              </div>
              <div className="text-gray-600 text-sm">Attended</div>
            </div>
            <div className="border rounded p-4">
              <div className="text-2xl font-bold text-rose-600">
                {reports.event_stats.attendance_rate.absent}
              </div>
              <div className="text-gray-600 text-sm">Absent</div>
            </div>
          </div>
        </div>
      )}

      {/* Hall Utilization */}
      {reports.hall_utilization && reports.hall_utilization.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-bold mb-4">Hall Utilization Report</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-4 py-2 text-left">Hall Name</th>
                  <th className="px-4 py-2 text-center">Capacity</th>
                  <th className="px-4 py-2 text-center">Total Bookings</th>
                  <th className="px-4 py-2 text-center">Approved</th>
                  <th className="px-4 py-2 text-center">Pending</th>
                </tr>
              </thead>
              <tbody>
                {reports.hall_utilization.map((hall) => (
                  <tr key={hall.id} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-2">{hall.name}</td>
                    <td className="px-4 py-2 text-center">{hall.capacity}</td>
                    <td className="px-4 py-2 text-center">
                      {hall.total_bookings}
                    </td>
                    <td className="px-4 py-2 text-center">
                      <span className="px-2 py-1 bg-green-100 text-green-800 rounded">
                        {hall.approved_bookings}
                      </span>
                    </td>
                    <td className="px-4 py-2 text-center">
                      <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded">
                        {hall.pending_bookings}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Audit Logs */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">Audit Logs</h3>
          <select
            value={auditDays}
            onChange={(e) => {
              setAuditDays(parseInt(e.target.value));
              fetchReports();
            }}
            className="px-3 py-1 border rounded"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {auditLogs.length > 0 ? (
            auditLogs.map((log) => (
              <div
                key={log.id}
                className="p-3 border rounded hover:bg-gray-50 text-sm"
              >
                <div className="flex justify-between">
                  <span className="font-medium text-gray-900">
                    {log.user_username}
                  </span>
                  <span className="text-gray-500">
                    {new Date(log.timestamp).toLocaleString()}
                  </span>
                </div>
                <div className="text-gray-700 mt-1">{log.action}</div>
              </div>
            ))
          ) : (
            <p className="text-gray-500 text-center py-4">
              No audit logs found
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminReporting;
