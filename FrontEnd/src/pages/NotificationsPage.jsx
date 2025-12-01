import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

const NotificationsPage = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedNotification, setExpandedNotification] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const response = await api.get("/notifications/");
      setNotifications(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      setError("Failed to load notifications");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const markAllRead = async () => {
    try {
      await api.post("/notifications/mark_all_read/");
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
      // Notify other components (e.g., Navbar) about the update
      window.dispatchEvent(new CustomEvent("notificationRead"));
    } catch (error) {
      console.error("Failed to mark notifications as read:", error);
    }
  };

  const markSingleRead = async (notificationId) => {
    try {
      await api.post(`/notifications/${notificationId}/mark_read/`);
      setNotifications((prev) =>
        prev.map((n) => (n.id === notificationId ? { ...n, is_read: true } : n))
      );
      // Notify other components (e.g., Navbar) about the update
      window.dispatchEvent(new CustomEvent("notificationRead"));
    } catch (error) {
      console.error("Failed to mark notification as read:", error);
    }
  };

  const takeAction = async (notification, action) => {
    try {
      const response = await api.post(
        `/notifications/${notification.id}/take_action/`,
        { action }
      );

      if (response.data.type === "download" && response.data.file_url) {
        window.open(response.data.file_url, "_blank");
      } else if (response.data.type === "redirect" && response.data.url) {
        navigate(response.data.url);
      }

      // Mark as read after action
      setExpandedNotification(null);
      markSingleRead(notification.id);

      // Refresh notifications
      fetchNotifications();
    } catch (error) {
      console.error("Failed to handle notification action:", error);
      setError("Failed to handle action");
    }
  };

  const toggleExpand = (notification) => {
    setExpandedNotification(
      expandedNotification?.id === notification.id ? null : notification
    );
  };

  const getActionButton = (notification) => {
    switch (notification.notification_type) {
      case "certificate_generated":
        return {
          text: "Download Certificate",
          action: "download",
          color: "bg-green-500 hover:bg-green-600",
        };
      case "points_approved":
        return {
          text: "View Points",
          action: "view_approved",
          color: "bg-blue-500 hover:bg-blue-600",
        };
      case "points_rejected":
        return {
          text: "View Rejection",
          action: "view_rejected",
          color: "bg-red-500 hover:bg-red-600",
        };
      case "hall_booking_approved":
        return {
          text: "View Booking",
          action: "view_booking",
          color: "bg-green-500 hover:bg-green-600",
        };
      case "hall_booking_rejected":
        return {
          text: "View Rejection",
          action: "view_rejection",
          color: "bg-red-500 hover:bg-red-600",
        };
      case "event_registration":
      case "event_reminder":
        return {
          text: "View Event",
          action: "view_event",
          color: "bg-blue-500 hover:bg-blue-600",
        };
      default:
        return null;
    }
  };

  const renderNotificationContent = (notification) => {
    if (
      notification.message.length > 100 &&
      expandedNotification?.id !== notification.id
    ) {
      return (
        <p className={`text-sm text-gray-600 mt-1`}>
          {notification.message.substring(0, 100)}...
          <button
            onClick={() => toggleExpand(notification)}
            className="text-blue-500 hover:text-blue-700 ml-2 font-medium"
          >
            Read more
          </button>
        </p>
      );
    }

    return (
      <p className={`text-sm text-gray-600 mt-1`}>
        {notification.message}
        {notification.message.length > 100 && (
          <button
            onClick={() => toggleExpand(notification)}
            className="text-blue-500 hover:text-blue-700 ml-2 font-medium"
          >
            Read less
          </button>
        )}
      </p>
    );
  };

  const deleteNotification = async (notificationId) => {
    try {
      await api.delete(`/notifications/${notificationId}/`);
      setNotifications((prev) => prev.filter((n) => n.id !== notificationId));
      // Notify other components (e.g., Navbar) about the update
      window.dispatchEvent(new CustomEvent("notificationRead"));
    } catch (error) {
      console.error("Failed to delete notification:", error);
    }
  };

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="bg-white rounded-lg shadow-md p-8">
            <div className="text-center text-gray-600">
              Loading notifications...
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Notifications
          </h1>
          {unreadCount > 0 && (
            <p className="text-blue-600 font-medium">
              You have {unreadCount} unread notification
              {unreadCount !== 1 ? "s" : ""}
            </p>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-md">
          <div className="p-6 border-b border-gray-200 flex justify-between items-center">
            <div>
              <h2 className="text-xl font-bold text-gray-800">
                All Notifications
              </h2>
              {notifications.length > 0 && (
                <p className="text-sm text-gray-500 mt-1">
                  {notifications.length} notification
                  {notifications.length !== 1 ? "s" : ""} total
                </p>
              )}
            </div>
            {unreadCount > 0 && (
              <button
                onClick={markAllRead}
                className="text-sm px-4 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors font-medium"
              >
                Mark All Read
              </button>
            )}
          </div>

          {error && (
            <div className="p-6 border-b border-gray-200">
              <div className="text-red-600">{error}</div>
            </div>
          )}

          <div className="max-h-[600px] overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="p-12 text-center">
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 17h5l-5 5v-5zM4.868 12.683A17.925 17.925 0 0112 21c7.962 0 12-1.21 12-2.683m-12 2.683l-3-3H9l3-3h-3V9.5L10.5 12l.868.683z"
                  />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">
                  No notifications
                </h3>
                <p className="mt-1 text-sm text-gray-500">
                  We'll let you know when there's any activity.
                </p>
              </div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {notifications.map((notification) => (
                  <li
                    key={notification.id}
                    className={`p-6 transition-colors ${
                      notification.is_read
                        ? "bg-white hover:bg-gray-50"
                        : "bg-blue-50 hover:bg-blue-100"
                    }`}
                  >
                    <div className="flex justify-between items-start gap-4">
                      <div className="flex-1">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h3
                              className={`font-semibold ${
                                notification.is_read
                                  ? "text-gray-900"
                                  : "text-blue-900"
                              }`}
                            >
                              {notification.title}
                            </h3>
                            {renderNotificationContent(notification)}
                          </div>
                        </div>

                        <div className="flex items-center justify-between mt-3">
                          <p className="text-xs text-gray-500">
                            {new Date(notification.created_at).toLocaleString()}
                          </p>

                          <div className="flex gap-2">
                            {/* Action button */}
                            {!notification.is_read &&
                              getActionButton(notification) && (
                                <button
                                  onClick={() =>
                                    takeAction(
                                      notification,
                                      getActionButton(notification).action
                                    )
                                  }
                                  className={`text-xs px-3 py-1 text-white rounded-md font-medium transition-colors ${
                                    getActionButton(notification).color
                                  }`}
                                >
                                  {getActionButton(notification).text}
                                </button>
                              )}

                            {/* Mark as read button */}
                            {!notification.is_read && (
                              <button
                                onClick={() => markSingleRead(notification.id)}
                                className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors"
                                title="Mark as read"
                              >
                                ✓
                              </button>
                            )}

                            {/* Delete button */}
                            <button
                              onClick={() =>
                                deleteNotification(notification.id)
                              }
                              className="text-xs px-2 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
                              title="Delete"
                            >
                              ✕
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotificationsPage;
