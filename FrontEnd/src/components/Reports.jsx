import React, { useEffect, useState } from "react";
import api from "../api";

const Reports = () => {
  const [eventStats, setEventStats] = useState([]);

  useEffect(() => {
    const fetchEventStats = async () => {
      const response = await api.get("/reports/event-statistics");
      setEventStats(response.data);
    };

    fetchEventStats();
  }, []);

  return (
    <div>
      <h2>Event Statistics</h2>
      <ul>
        {eventStats.map((stat) => (
          <li key={stat.id}>
            {stat.name}: {stat.total_registrations} registrations
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Reports;
