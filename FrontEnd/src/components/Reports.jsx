import React, { useEffect, useState } from "react";
import api from "../api";

const Reports = () => {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchReportData = async () => {
      try {
        setLoading(true);
        const response = await api.get("/dashboard/stats/");
        setReportData(response.data);
      } catch (err) {
        setError("Failed to load report data");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchReportData();
  }, []);

  if (loading)
    return <div className="p-4 text-gray-600">Loading reports...</div>;

  if (error) return <div className="p-4 text-red-600">{error}</div>;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Reports & Statistics
      </h2>

      {reportData && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {reportData.total_events !== undefined && (
              <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                <p className="text-sm text-gray-600">Total Events</p>
                <p className="text-3xl font-bold text-blue-600">
                  {reportData.total_events}
                </p>
              </div>
            )}
            {reportData.total_registered !== undefined && (
              <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                <p className="text-sm text-gray-600">Total Registered</p>
                <p className="text-3xl font-bold text-green-600">
                  {reportData.total_registered}
                </p>
              </div>
            )}
            {reportData.total_attended !== undefined && (
              <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                <p className="text-sm text-gray-600">Total Attended</p>
                <p className="text-3xl font-bold text-purple-600">
                  {reportData.total_attended}
                </p>
              </div>
            )}
            {reportData.total_points !== undefined && (
              <div className="bg-orange-50 p-4 rounded-lg border-l-4 border-orange-500">
                <p className="text-sm text-gray-600">AICTE Points Earned</p>
                <p className="text-3xl font-bold text-orange-600">
                  {reportData.total_points}
                </p>
              </div>
            )}
          </div>

          {/* Detailed Statistics */}
          {reportData.event_breakdown && (
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Event Breakdown
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(reportData.event_breakdown).map(
                  ([status, count]) => (
                    <div key={status} className="bg-gray-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600 capitalize">
                        {status}
                      </p>
                      <p className="text-2xl font-bold text-gray-800">
                        {count}
                      </p>
                    </div>
                  )
                )}
              </div>
            </div>
          )}

          {/* Activity Metrics */}
          {reportData.pending_approvals !== undefined && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h3 className="font-semibold text-yellow-900 mb-2">
                Pending Approvals
              </h3>
              <p className="text-2xl font-bold text-yellow-700">
                {reportData.pending_approvals}
              </p>
              <p className="text-xs text-yellow-600 mt-2">
                Items awaiting your action
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Reports;
