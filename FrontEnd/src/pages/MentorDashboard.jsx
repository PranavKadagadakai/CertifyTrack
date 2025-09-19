import React, { useState, useEffect } from "react";
import api from "../api";

function MentorDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedMentee, setSelectedMentee] = useState(null);
  const [menteeCerts, setMenteeCerts] = useState([]);

  useEffect(() => {
    api
      .get("/dashboard/")
      .then((res) => {
        setData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to fetch dashboard data.");
        setLoading(false);
      });
  }, []);

  const fetchMenteeCertificates = async (menteeId) => {
    try {
      const res = await api.get(`/mentor/${menteeId}/certificates/`);
      setSelectedMentee(res.data.mentee);
      setMenteeCerts(res.data.certificates);
    } catch (err) {
      alert("Failed to fetch mentee certificates.");
    }
  };

  if (loading) return <p>Loading dashboard...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Mentor Dashboard</h1>
      <p>Welcome, {data.profile.profile.full_name}!</p>

      <div className="grid md:grid-cols-3 gap-8 mt-8">
        <div className="md:col-span-1">
          <h2 className="text-2xl font-semibold mb-4">Your Mentees</h2>
          {data.mentees.length > 0 ? (
            <ul className="space-y-2">
              {data.mentees.map((mentee) => (
                <li key={mentee.id}>
                  <button
                    onClick={() => fetchMenteeCertificates(mentee.id)}
                    className="w-full text-left p-2 rounded hover:bg-gray-200"
                  >
                    {mentee.profile.full_name || mentee.username}
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p>You have no assigned mentees.</p>
          )}
        </div>

        <div className="md:col-span-2">
          <h2 className="text-2xl font-semibold mb-4">Mentee Certificates</h2>
          {selectedMentee ? (
            <div>
              <h3 className="text-xl font-bold mb-2">
                Certificates for {selectedMentee.profile.full_name}
              </h3>
              {menteeCerts.length > 0 ? (
                <ul className="space-y-3">
                  {menteeCerts.map((cert) => (
                    <li
                      key={cert.id}
                      className="flex justify-between items-center p-3 bg-white rounded shadow"
                    >
                      <span>
                        {cert.event_name} - Generated on{" "}
                        {new Date(cert.generated_at).toLocaleDateString()}
                      </span>
                      <div className="flex items-center space-x-2">
                        <a
                          href={cert.certificate_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-sm px-3 py-1 bg-blue-500 text-white rounded"
                        >
                          View
                        </a>
                        <span
                          className={`text-sm font-bold ${
                            cert.verified ? "text-green-600" : "text-red-600"
                          }`}
                        >
                          {cert.verified ? "Verified" : "Not Verified"}
                        </span>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>This mentee has no certificates.</p>
              )}
            </div>
          ) : (
            <p>Select a mentee to view their certificates.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default MentorDashboard;
