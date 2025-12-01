import React, { useEffect, useState } from "react";
import api from "../api";
import Reports from "../components/Reports";
import CertificateViewer from "../components/CertificateViewer";
import ApprovalModal from "../components/ApprovalModal";

const MentorDashboard = () => {
  const [mentees, setMentees] = useState([]);
  const [selectedMentee, setSelectedMentee] = useState(null);
  const [menteeStats, setMenteeStats] = useState(null);
  const [pendingTransactions, setPendingTransactions] = useState([]);
  const [viewingCertificate, setViewingCertificate] = useState(null);
  const [approvalModal, setApprovalModal] = useState({
    open: false,
    transaction: null,
  });

  useEffect(() => {
    fetchMenteesAndTransactions();
  }, []);

  const fetchMenteesAndTransactions = async () => {
    try {
      const menteesResponse = await api.get("/students/mentees/");
      const transactionsResponse = await api.get(
        "/aicte-transactions/?status=PENDING"
      );
      setMentees(menteesResponse.data);
      setPendingTransactions(transactionsResponse.data);
    } catch (error) {
      console.error("Failed to fetch data:", error);
    }
  };

  const fetchMenteeStats = async (menteeId) => {
    try {
      const response = await api.get(`/students/${menteeId}/`);
      setMenteeStats(response.data);
    } catch (error) {
      console.error("Failed to fetch mentee stats:", error);
    }
  };

  const handleMenteeSelect = (mentee) => {
    setSelectedMentee(mentee);
    fetchMenteeStats(mentee.id);
  };

  const handleApprovalWithVerification = (transaction) => {
    setApprovalModal({ open: true, transaction });
  };

  const handleApproval = async (
    transactionId,
    statusAction,
    verificationCode = null
  ) => {
    try {
      const data = {};
      if (verificationCode && statusAction === "approve") {
        data.verification_code = verificationCode;
      }
      if (statusAction === "reject") {
        // For reject, the reason is passed as verificationCode parameter from modal
        data.reason = verificationCode;
      }

      await api.post(
        `/aicte-transactions/${transactionId}/${statusAction}/`,
        data
      );
      alert(`Transaction ${statusAction.toLowerCase()}d successfully!`);

      // Refresh all pending transactions and mentee stats
      fetchMenteesAndTransactions();

      setApprovalModal({ open: false, transaction: null });

      // Refresh mentee stats if viewing one
      if (selectedMentee) {
        fetchMenteeStats(selectedMentee.id);
      }
    } catch (error) {
      console.error("Approval failed:", error);
      alert(error.response?.data?.error || "Approval failed");
    }
  };

  const openCertificateViewer = (certificateUrl) => {
    setViewingCertificate(certificateUrl);
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Mentor Dashboard</h1>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Mentees List */}
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">Your Mentees</h2>
          <ul className="space-y-2">
            {mentees.map((mentee) => (
              <li
                key={mentee.id}
                className={`p-2 border-b hover:bg-gray-50 cursor-pointer ${
                  selectedMentee?.id === mentee.id
                    ? "bg-blue-50 border-blue-200"
                    : ""
                }`}
                onClick={() => handleMenteeSelect(mentee)}
              >
                <div className="font-medium">{mentee.name}</div>
                <div className="text-sm text-gray-600">USN: {mentee.usn}</div>
              </li>
            ))}
          </ul>
        </div>

        {/* Selected Mentee Stats */}
        <div className="bg-white p-4 rounded shadow xl:col-span-2">
          {selectedMentee ? (
            <div>
              <h2 className="text-xl font-semibold mb-4">
                {selectedMentee.name} - Stats
              </h2>
              {menteeStats ? (
                <div className="space-y-4">
                  {/* AICTE Points */}
                  <div className="grid grid-cols-3 gap-4">
                    <div className="bg-blue-50 p-3 rounded">
                      <div className="text-sm text-gray-600">Total Points</div>
                      <div className="text-2xl font-bold text-blue-600">
                        {menteeStats.detailed_stats?.aicte_points
                          ?.total_earned || 0}
                      </div>
                    </div>
                    <div className="bg-green-50 p-3 rounded">
                      <div className="text-sm text-gray-600">
                        Required Points
                      </div>
                      <div className="text-2xl font-bold text-green-600">
                        {menteeStats.detailed_stats?.aicte_points?.required ||
                          0}
                      </div>
                    </div>
                    <div className="bg-purple-50 p-3 rounded">
                      <div className="text-sm text-gray-600">AICTE Status</div>
                      <div
                        className={`text-lg font-bold ${
                          menteeStats.detailed_stats?.aicte_points?.is_completed
                            ? "text-green-600"
                            : "text-red-600"
                        }`}
                      >
                        {menteeStats.detailed_stats?.aicte_points?.is_completed
                          ? "COMPLETED"
                          : "PENDING"}
                      </div>
                    </div>
                  </div>

                  {/* Events */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-indigo-50 p-3 rounded">
                      <div className="text-sm text-gray-600">
                        Events Registered
                      </div>
                      <div className="text-xl font-bold">
                        {menteeStats.detailed_stats?.events?.registered_count ||
                          0}
                      </div>
                    </div>
                    <div className="bg-orange-50 p-3 rounded">
                      <div className="text-sm text-gray-600">
                        Events Participated
                      </div>
                      <div className="text-xl font-bold">
                        {menteeStats.detailed_stats?.events
                          ?.participated_count || 0}
                      </div>
                    </div>
                  </div>

                  {/* Certificates */}
                  <div className="bg-white border rounded">
                    <h3 className="text-lg font-semibold p-4 border-b">
                      Certificates Earned
                    </h3>
                    {menteeStats.detailed_stats?.certificates?.list?.length >
                    0 ? (
                      <ul className="divide-y">
                        {menteeStats.detailed_stats.certificates.list.map(
                          (cert, index) => (
                            <li
                              key={index}
                              className="p-4 flex justify-between items-center"
                            >
                              <div>
                                <div className="font-medium">
                                  {cert.event_name}
                                </div>
                                <div className="text-sm text-gray-600">
                                  Issued:{" "}
                                  {new Date(
                                    cert.issue_date
                                  ).toLocaleDateString()}
                                </div>
                              </div>
                              <button
                                className="bg-blue-500 text-white px-3 py-1 rounded text-sm"
                                onClick={() =>
                                  openCertificateViewer(cert.file_url)
                                }
                              >
                                View
                              </button>
                            </li>
                          )
                        )}
                      </ul>
                    ) : (
                      <div className="p-4 text-gray-500">
                        No certificates earned yet.
                      </div>
                    )}
                  </div>

                  {/* Pending Approvals */}
                  <div className="bg-white border rounded">
                    <h3 className="text-lg font-semibold p-4 border-b">
                      Pending Approvals
                    </h3>
                    {menteeStats.detailed_stats?.approvals?.pending_list
                      ?.length > 0 ? (
                      <ul className="divide-y">
                        {menteeStats.detailed_stats.approvals.pending_list.map(
                          (transaction) => (
                            <li key={transaction.id} className="p-4">
                              <div className="flex justify-between items-start">
                                <div className="flex-1">
                                  <div className="font-medium">
                                    {transaction.event_name}
                                  </div>
                                  <div className="text-sm text-gray-600">
                                    Points: {transaction.points_allocated} |
                                    Category: {transaction.category_name}
                                  </div>
                                </div>
                                <div className="space-x-2">
                                  <button
                                    className="bg-green-500 text-white px-3 py-1 rounded text-sm"
                                    onClick={() =>
                                      handleApprovalWithVerification(
                                        transaction
                                      )
                                    }
                                  >
                                    Approve
                                  </button>
                                  <button
                                    className="bg-red-500 text-white px-3 py-1 rounded text-sm"
                                    onClick={() =>
                                      handleApproval(transaction.id, "reject")
                                    }
                                  >
                                    Reject
                                  </button>
                                </div>
                              </div>
                              {transaction.certificate_url && (
                                <div className="mt-2">
                                  <button
                                    className="bg-blue-500 text-white px-3 py-1 rounded text-sm"
                                    onClick={() =>
                                      openCertificateViewer(
                                        transaction.certificate_url
                                      )
                                    }
                                  >
                                    View Certificate
                                  </button>
                                </div>
                              )}
                            </li>
                          )
                        )}
                      </ul>
                    ) : (
                      <div className="p-4 text-gray-500">
                        No pending approvals.
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">Loading stats...</div>
              )}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              Select a mentee to view their detailed statistics and pending
              approvals.
            </div>
          )}
        </div>
      </div>

      {/* All Pending Approvals - Separate Section */}
      {pendingTransactions.length > 0 && (
        <div className="mt-6 bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">
            All Pending AICTE Transactions
          </h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Student
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Event
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Points
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {pendingTransactions.map((transaction) => (
                  <tr key={transaction.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-medium">
                        {transaction.student_name}
                      </div>
                      <div className="text-sm text-gray-600">
                        {transaction.student_usn}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {transaction.event_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {transaction.points_allocated}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap space-x-2">
                      <button
                        className="bg-green-500 text-white px-3 py-1 rounded text-sm"
                        onClick={() =>
                          handleApprovalWithVerification(transaction)
                        }
                      >
                        Approve
                      </button>
                      <button
                        className="bg-red-500 text-white px-3 py-1 rounded text-sm"
                        onClick={() => handleApproval(transaction.id, "reject")}
                      >
                        Reject
                      </button>
                      {transaction.student && (
                        <button
                          className="bg-blue-500 text-white px-2 py-1 rounded text-sm"
                          onClick={() => {
                            const mentee = mentees.find(
                              (m) => m.id === transaction.student.id
                            );
                            if (mentee) handleMenteeSelect(mentee);
                          }}
                        >
                          View Student
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Reports */}
      <div className="mt-6">
        <Reports />
      </div>

      {/* Modals */}
      {viewingCertificate && (
        <CertificateViewer
          certificateUrl={viewingCertificate}
          onClose={() => setViewingCertificate(null)}
        />
      )}

      {approvalModal.open && (
        <ApprovalModal
          transaction={approvalModal.transaction}
          onApprove={(verificationCode) =>
            handleApproval(
              approvalModal.transaction.id,
              "approve",
              verificationCode
            )
          }
          onReject={(reason) =>
            handleApproval(approvalModal.transaction.id, "reject", reason)
          }
          onClose={() => setApprovalModal({ open: false, transaction: null })}
        />
      )}
    </div>
  );
};

export default MentorDashboard;
