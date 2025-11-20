import React from "react";

const EventCard = ({ event, onRegister }) => {
  return (
    <div className="border p-4 rounded shadow">
      <h3 className="text-lg font-bold">{event.name}</h3>
      <p>{event.description}</p>
      <p>
        <strong>Date:</strong> {event.event_date}
      </p>
      <p>
        <strong>Time:</strong> {event.start_time} - {event.end_time}
      </p>
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded mt-2"
        onClick={() => onRegister(event.id)}
      >
        Register
      </button>
    </div>
  );
};

export default EventCard;