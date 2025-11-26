import React, { useEffect, useState } from "react";
import api from "../api";
import Reports from "../components/Reports";

const MentorDashboard = () => {
  const [mentees, setMentees] = useState([]);
  const [pendingTransactions, setPendingTransactions] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const menteesResponse = await api.get("/students/mentees/");
      const transactionsResponse = await api.get(
        "/aicte-transactions/?status=PENDING"
      );
      setMentees(menteesResponse.data);
      setPendingTransactions(transactionsResponse.data);
    };

    fetchData();
  }, []);

  const handleApproval = async (transactionId, statusAction) => {
    try {
      // Use the custom actions: approve or reject
      await api.post(`/aicte-transactions/${transactionId}/${statusAction}/`);
      alert(`Transaction ${statusAction.toLowerCase()} successfully!`);
      setPendingTransactions((prev) =>
        prev.filter((transaction) => transaction.id !== transactionId)
      );
    } catch (error) {
      console.error("Approval failed:", error);
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Mentor Dashboard</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Mentees Section */}
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">Your Mentees</h2>
          <ul className="space-y-2">
            {mentees.map((mentee) => (
              <li key={mentee.id} className="border-b pb-2">
                {mentee.name} ({mentee.usn})
              </li>
            ))}
          </ul>
        </div>

        {/* Pending Transactions Section */}
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">
            Pending AICTE Transactions
          </h2>
          <ul className="space-y-4">
            {pendingTransactions.map((transaction) => (
              <li
                key={transaction.id}
                className="flex justify-between items-center border-b pb-2"
              >
                <span>
                  {transaction.student.name} - {transaction.points_allocated}{" "}
                  points
                </span>
                <div className="space-x-2">
                  <button
                    className="bg-green-500 text-white px-4 py-1 rounded"
                    onClick={() => handleApproval(transaction.id, "approve")}
                  >
                    Approve
                  </button>
                  <button
                    className="bg-red-500 text-white px-4 py-1 rounded"
                    onClick={() => handleApproval(transaction.id, "reject")}
                  >
                    Reject
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Reports */}
      <div className="mt-6">
        <Reports />
      </div>
    </div>
  );
};

export default MentorDashboard;
