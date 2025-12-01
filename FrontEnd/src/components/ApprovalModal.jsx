import React, { useState } from "react";

const ApprovalModal = ({ transaction, onApprove, onReject, onClose }) => {
  const [verificationCode, setVerificationCode] = useState("");
  const [showRejectionReason, setShowRejectionReason] = useState(false);
  const [rejectionReason, setRejectionReason] = useState("");

  const handleApprove = () => {
    if (!verificationCode.trim()) {
      alert("Please enter the verification code from the QR code.");
      return;
    }
    onApprove(verificationCode.trim());
  };

  const handleReject = () => {
    if (showRejectionReason) {
      if (!rejectionReason.trim()) {
        alert("Please enter a rejection reason.");
        return;
      }
      // For reject, we need to call a function that handles rejection
      onReject(rejectionReason.trim());
    } else {
      setShowRejectionReason(true);
    }
  };

  const handleCancelRejection = () => {
    setShowRejectionReason(false);
    setRejectionReason("");
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-semibold">
            Approve AICTE Points - {transaction?.event_name}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            &times;
          </button>
        </div>

        <div className="p-6 overflow-auto max-h-[70vh]">
          {/* Transaction Details */}
          <div className="mb-6 bg-gray-50 p-4 rounded">
            <h3 className="font-semibold mb-2">Transaction Details</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium">Student:</span>{" "}
                {transaction?.student?.name} ({transaction?.student?.usn})
              </div>
              <div>
                <span className="font-medium">Points:</span>{" "}
                {transaction?.points_allocated}
              </div>
              <div>
                <span className="font-medium">Category:</span>{" "}
                {transaction?.category}
              </div>
              <div>
                <span className="font-medium">Event:</span>{" "}
                {transaction?.event_name}
              </div>
            </div>
          </div>

          {/* Instructions */}
          <div className="mb-6 bg-blue-50 p-4 rounded border-l-4 border-blue-400">
            <h3 className="font-semibold text-blue-800 mb-2">
              📋 Approval Instructions
            </h3>
            <ol className="list-decimal list-inside text-blue-700 text-sm space-y-1">
              <li>View the certificate below to see the QR code</li>
              <li>Scan the QR code or zoom in to find the verification code</li>
              <li>Enter the verification code in the field below</li>
              <li>Click "Approve" to confirm the points</li>
            </ol>
          </div>

          {/* Certificate Display */}
          {transaction?.certificate_url && (
            <div className="mb-6">
              <h3 className="font-semibold mb-3">Certificate Preview</h3>
              <div className="border rounded-lg overflow-hidden bg-gray-100">
                <iframe
                  src={transaction.certificate_url}
                  className="w-full h-[400px] border-0"
                  title="Certificate for Verification"
                />
                <div className="p-2 text-center">
                  <a
                    href={transaction.certificate_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 text-sm underline"
                  >
                    Open in new tab for better view
                  </a>
                </div>
              </div>
            </div>
          )}

          {/* Verification Code Input */}
          {!showRejectionReason && (
            <div className="mb-6">
              <label className="block text-sm font-semibold mb-2">
                Verification Code (from QR code)
              </label>
              <input
                type="text"
                value={verificationCode}
                onChange={(e) =>
                  setVerificationCode(e.target.value.toUpperCase())
                }
                placeholder="Enter 8-character verification code"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent uppercase text-center text-lg font-mono"
                maxLength={8}
              />
            </div>
          )}

          {/* Rejection Reason Input */}
          {showRejectionReason && (
            <div className="mb-6">
              <label className="block text-sm font-semibold mb-2">
                Rejection Reason
              </label>
              <textarea
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
                placeholder="Please provide a reason for rejection..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                rows={3}
                maxLength={500}
              />
              <div className="text-right text-xs text-gray-500 mt-1">
                {rejectionReason.length}/500 characters
              </div>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end gap-3 p-4 border-t bg-gray-50">
          {showRejectionReason ? (
            <>
              <button
                onClick={handleCancelRejection}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-100"
              >
                Cancel
              </button>
              <button
                onClick={handleReject}
                className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium"
              >
                Confirm Rejection
              </button>
            </>
          ) : (
            <>
              <button
                onClick={onClose}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-100"
              >
                Cancel
              </button>
              <button
                onClick={handleReject}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium"
              >
                Reject
              </button>
              <button
                onClick={handleApprove}
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium"
                disabled={!verificationCode.trim()}
              >
                Approve with Code
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ApprovalModal;
