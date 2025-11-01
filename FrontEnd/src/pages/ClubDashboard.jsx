import React, { useState, useEffect } from "react";
import api from "../api";
import { useAuth } from "../context/AuthContext";

function ClubDashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [templateFile, setTemplateFile] = useState(null);

  const fetchData = async () => {
    try {
      const res = await api.get("/dashboard/");
      setData(res.data);
    } catch (err) {
      setError("Failed to fetch dashboard data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleGenerateCertificates = async (eventId) => {
    if (
      !confirm(
        "Are you sure you want to generate certificates for this event? This will mark the event as finished."
      )
    ) {
      return;
    }
    try {
      await api.post(`/events/${eventId}/generate-certificates/`);
      alert("Certificates are being generated!");
      fetchData();
    } catch (err) {
      alert(
        err.response?.data?.error || "Failed to start certificate generation."
      );
    }
  };

  const handleUploadTemplate = async (eventId) => {
    if (!templateFile) {
      alert("Please select a template file.");
      return;
    }
    const formData = new FormData();
    formData.append("template_file", templateFile);
    try {
      await api.post(`/events/${eventId}/upload-template/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("Template uploaded successfully!");
      setTemplateFile(null);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.error || "Failed to upload template.");
    }
  };

  if (loading) return <p>Loading dashboard...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Club Dashboard</h1>
      <p>Welcome, {data.club.name}!</p>

      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Your Events</h2>
        {data.events.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.events.map((event) => (
              <div
                key={event.id}
                className="p-4 bg-white rounded-lg shadow space-y-3"
              >
                <h3 className="text-xl font-bold">{event.name}</h3>
                <p>
                  <strong>Date:</strong> {event.date}
                </p>
                <p>
                  <strong>Status:</strong> {event.status}
                </p>
                <p>
                  <strong>Participants:</strong> {event.participants_count} /{" "}
                  {event.participant_limit}
                </p>

                {event.template_url ? (
                  <p className="text-green-600">Template Uploaded</p>
                ) : (
                  <div className="space-y-2">
                    <input
                      type="file"
                      onChange={(e) => setTemplateFile(e.target.files[0])}
                      className="text-sm"
                    />
                    <button
                      onClick={() => handleUploadTemplate(event.id)}
                      className="w-full text-sm px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600"
                    >
                      Upload Template
                    </button>
                  </div>
                )}

                <button
                  onClick={() => handleGenerateCertificates(event.id)}
                  disabled={!event.template_url || event.status === "finished"}
                  className="w-full px-4 py-2 text-white bg-blue-600 rounded disabled:bg-gray-400 hover:bg-blue-700"
                >
                  {event.status === "finished"
                    ? "Certificates Generated"
                    : "Generate Certificates"}
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p>You have not created any events yet.</p>
        )}
      </div>
    </div>
  );
}

export default ClubDashboard;
