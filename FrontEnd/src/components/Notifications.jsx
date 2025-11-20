import React, { useEffect, useState } from "react";
import api from "../api";

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const fetchNotifications = async () => {
      const response = await api.get("/notifications");
      setNotifications(response.data);
    };

    fetchNotifications();
  }, []);

  const markAllRead = async () => {
    try {
      await api.post("/notifications/mark-all-read");
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
    } catch (error) {
      console.error("Failed to mark notifications as read:", error);
    }
  };

  return (
    <div>
      <h2>Notifications</h2>
      <button onClick={markAllRead}>Mark All as Read</button>
      <ul>
        {notifications.map((notification) => (
          <li
            key={notification.id}
            style={{ fontWeight: notification.is_read ? "normal" : "bold" }}
          >
            {notification.title} - {notification.message}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Notifications;
