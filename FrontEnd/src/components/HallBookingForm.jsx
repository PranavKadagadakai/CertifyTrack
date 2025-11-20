import React, { useState, useEffect } from "react";
import api from "../api";

const HallBookingForm = ({ onBookingCreated }) => {
  const [halls, setHalls] = useState([]);
  const [formData, setFormData] = useState({
    hall: "",
    booking_date: "",
    start_time: "",
    end_time: "",
  });

  useEffect(() => {
    const fetchHalls = async () => {
      const response = await api.get("/halls");
      setHalls(response.data);
    };

    fetchHalls();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/hall-bookings", formData);
      alert("Booking created successfully!");
      onBookingCreated(response.data);
    } catch (error) {
      console.error("Failed to create booking:", error);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Hall:
        <select name="hall" onChange={handleChange} value={formData.hall}>
          <option value="">Select a hall</option>
          {halls.map((hall) => (
            <option key={hall.id} value={hall.id}>
              {hall.name}
            </option>
          ))}
        </select>
      </label>
      <label>
        Booking Date:
        <input type="date" name="booking_date" onChange={handleChange} value={formData.booking_date} />
      </label>
      <label>
        Start Time:
        <input type="time" name="start_time" onChange={handleChange} value={formData.start_time} />
      </label>
      <label>
        End Time:
        <input type="time" name="end_time" onChange={handleChange} value={formData.end_time} />
      </label>
      <button type="submit">Create Booking</button>
    </form>
  );
};

export default HallBookingForm;