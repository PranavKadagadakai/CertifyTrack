// FrontEnd/src/components/AdminHallBookings.jsx
import React, { useState, useEffect } from "react";
import api from "../api";

const AdminHallBookings = () => {
  const [pendingBookings, setPendingBookings] = useState([]);
  const [loadingBookings, setLoadingBookings] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchPendingBookings();
  }, []);

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

  const handleReject = async (bookingId) => {
    const reason = prompt("Enter rejection reason (min 5 characters):");
    if (!reason || reason.length < 5) {
      alert("Please enter a valid rejection reason.");
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

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Pending Hall Bookings</h2>

      {error && <div className="text-red-600 mb-3">{error}</div>}

      {loadingBookings ? (
        <div>Loading pending bookings...</div>
      ) : pendingBookings.length === 0 ? (
        <div className="text-gray-600">No pending bookings.</div>
      ) : (
        <div className="space-y-4">
          {pendingBookings.map((b) => (
            <div
              key={b.id}
              className="p-4 border rounded flex items-center justify-between bg-gray-50"
            >
              <div>
                <div className="text-lg font-semibold">
                  {b.hall?.name || "Hall"}
                </div>
                <div className="text-sm mt-1 text-gray-700">
                  {b.booking_date} • {b.start_time} — {b.end_time}
                </div>
                <div className="text-sm text-gray-600">
                  Requested by: {b.created_by?.username || b.created_by?.email}
                </div>
                {b.event && (
                  <div className="text-sm text-gray-700">
                    Event: {b.event.name}
                  </div>
                )}
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => handleApprove(b.id)}
                  disabled={actionLoading}
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                  Approve
                </button>
                <button
                  onClick={() => handleReject(b.id)}
                  disabled={actionLoading}
                  className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                >
                  Reject
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AdminHallBookings;
