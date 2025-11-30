import React, { useState, useEffect } from "react";
import api from "../api";

const AICTEManagement = ({ userType = "mentor", menteeFilter = null }) => {
  const [transactions, setTransactions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [modalAction, setModalAction] = useState("");
  const [modalReason, setModalReason] = useState("");
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchData();
  }, [userType, menteeFilter]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [transactionsRes, categoriesRes] = await Promise.all([
        api.get("/aicte-transactions/"),
        api.get("/aicte-categories/"),
      ]);

      let filteredTransactions = transactionsRes.data;

      // Filter transactions based on user type and mentee filter
      if (userType === "mentor") {
        filteredTransactions = filteredTransactions.filter(
          (tx) => tx.status === "PENDING"
        );
      } else if (menteeFilter) {
        filteredTransactions = filteredTransactions.filter(
          (tx) =>
            tx.student_id === menteeFilter || tx.student_usn === menteeFilter
        );
      }

      setTransactions(filteredTransactions);
      setCategories(categoriesRes.data);

      // Calculate stats
      const approved = filteredTransactions.filter(
        (tx) => tx.status === "APPROVED"
      ).length;
      const pending = filteredTransactions.filter(
        (tx) => tx.status === "PENDING"
      ).length;
      const rejected = filteredTransactions.filter(
        (tx) => tx.status === "REJECTED"
      ).length;
      const totalPoints = filteredTransactions
        .filter((tx) => tx.status === "APPROVED")
        .reduce((sum, tx) => sum + (tx.points_allocated || 0), 0);

      setStats({
        total: filteredTransactions.length,
        approved,
        pending,
        rejected,
        totalPoints,
      });
    } catch (error) {
      console.error("Error fetching AICTE data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleTransactionAction = async (
    transactionId,
    action,
    reason = ""
  ) => {
    try {
      const endpoint = action === "approve" ? "approve" : "reject";
      const payload = action === "reject" ? { reason } : {};

      await api.post(
        `/aicte-transactions/${transactionId}/${endpoint}/`,
        payload
      );

      // Update local state
      setTransactions((prev) =>
        prev.map((tx) =>
          tx.id === transactionId
            ? { ...tx, status: action === "approve" ? "APPROVED" : "REJECTED" }
            : tx
        )
      );

      setSelectedTransaction(null);
      setModalAction("");
      setModalReason("");

      // Refresh stats
      fetchData();
    } catch (error) {
      console.error(`Error ${action}ing transaction:`, error);
      alert(`Failed to ${action} transaction. Please try again.`);
    }
  };

  const openModal = (transaction, action) => {
    setSelectedTransaction(transaction);
    setModalAction(action);
    if (action === "reject") {
      setModalReason("");
    }
  };

  const closeModal = () => {
    setSelectedTransaction(null);
    setModalAction("");
    setModalReason("");
  };

  const getCategoryMaxPoints = (categoryName) => {
    const category = categories.find((cat) => cat.name === categoryName);
    return category ? category.max_points_allowed : 20;
  };

  if (loading) return <div className="p-4">Loading AICTE data...</div>;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold">AICTE Points Management</h2>
        <button
          onClick={fetchData}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Refresh
        </button>
      </div>

      {/* Stats Summary */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          <div className="bg-blue-50 p-3 rounded">
            <div className="text-2xl font-bold text-blue-600">
              {stats.total}
            </div>
            <div className="text-sm text-gray-600">Total Transactions</div>
          </div>
          <div className="bg-green-50 p-3 rounded">
            <div className="text-2xl font-bold text-green-600">
              {stats.approved}
            </div>
            <div className="text-sm text-gray-600">Approved</div>
          </div>
          <div className="bg-yellow-50 p-3 rounded">
            <div className="text-2xl font-bold text-yellow-600">
              {stats.pending}
            </div>
            <div className="text-sm text-gray-600">Pending</div>
          </div>
          <div className="bg-red-50 p-3 rounded">
            <div className="text-2xl font-bold text-red-600">
              {stats.rejected}
            </div>
            <div className="text-sm text-gray-600">Rejected</div>
          </div>
          <div className="bg-purple-50 p-3 rounded">
            <div className="text-2xl font-bold text-purple-600">
              {stats.totalPoints}
            </div>
            <div className="text-sm text-gray-600">Points Awarded</div>
          </div>
        </div>
      )}

      {/* Transactions List */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium">
          {userType === "mentor" ? "Pending Approvals" : "Transaction History"}
        </h3>

        {transactions.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No transactions found.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full table-auto">
              <thead>
                <tr className="bg-gray-50">
                  <th className="px-4 py-2 text-left">Student</th>
                  <th className="px-4 py-2 text-left">Event</th>
                  <th className="px-4 py-2 text-left">Category</th>
                  <th className="px-4 py-2 text-center">Points</th>
                  <th className="px-4 py-2 text-center">Status</th>
                  <th className="px-4 py-2 text-center">Date</th>
                  {userType === "mentor" && (
                    <th className="px-4 py-2 text-center">Actions</th>
                  )}
                </tr>
              </thead>
              <tbody>
                {transactions.map((transaction) => (
                  <tr
                    key={transaction.id}
                    className="border-b hover:bg-gray-50"
                  >
                    <td className="px-4 py-2">
                      <div>
                        <div className="font-medium">
                          {transaction.student_usn}
                        </div>
                        <div className="text-sm text-gray-600">
                          {transaction.student_name}
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-2">{transaction.event_name}</td>
                    <td className="px-4 py-2">
                      <div>
                        <div className="font-medium">
                          {transaction.category_name}
                        </div>
                        <div className="text-sm text-gray-500">
                          Max: {getCategoryMaxPoints(transaction.category_name)}{" "}
                          pts
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-2 text-center font-semibold">
                      {transaction.points_allocated}
                    </td>
                    <td className="px-4 py-2 text-center">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${
                          transaction.status === "APPROVED"
                            ? "bg-green-100 text-green-800"
                            : transaction.status === "REJECTED"
                            ? "bg-red-100 text-red-800"
                            : "bg-yellow-100 text-yellow-800"
                        }`}
                      >
                        {transaction.status}
                      </span>
                    </td>
                    <td className="px-4 py-2 text-center text-sm">
                      {new Date(transaction.created_at).toLocaleDateString()}
                    </td>
                    {userType === "mentor" &&
                      transaction.status === "PENDING" && (
                        <td className="px-4 py-2 text-center space-x-2">
                          <button
                            onClick={() =>
                              handleTransactionAction(transaction.id, "approve")
                            }
                            className="px-3 py-1 bg-green-500 text-white text-sm rounded hover:bg-green-600"
                          >
                            Approve
                          </button>
                          <button
                            onClick={() => openModal(transaction, "reject")}
                            className="px-3 py-1 bg-red-500 text-white text-sm rounded hover:bg-red-600"
                          >
                            Reject
                          </button>
                        </td>
                      )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Rejection Modal */}
      {modalAction === "reject" && selectedTransaction && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold mb-4">
              Reject AICTE Transaction
            </h3>
            <p className="mb-4">
              Reject points for {selectedTransaction.student_usn} -{" "}
              {selectedTransaction.event_name}?
            </p>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">
                Reason for rejection:
              </label>
              <textarea
                value={modalReason}
                onChange={(e) => setModalReason(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded resize-none"
                rows="3"
                placeholder="Please provide a reason for rejection..."
                required
              />
            </div>
            <div className="flex justify-end space-x-3">
              <button
                onClick={closeModal}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
              >
                Cancel
              </button>
              <button
                onClick={() =>
                  handleTransactionAction(
                    selectedTransaction.id,
                    "reject",
                    modalReason
                  )
                }
                className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                disabled={!modalReason.trim()}
              >
                Reject
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AICTEManagement;
