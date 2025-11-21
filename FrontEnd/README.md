# CertifyTrack Frontend

React + Vite frontend for CertifyTrack platform - an academic event management and certification system.

## Quick Start

### Prerequisites

- Node.js 16+ (recommend 18+ LTS)
- npm, yarn, or pnpm
- Git

### Installation

```bash
# Navigate to frontend directory
cd CertifyTrack/FrontEnd

# Install dependencies
pnpm install  # or npm install / yarn install

# Create environment configuration
cat > .env << EOF
VITE_API_BASE_URL=http://localhost:8000/api
EOF

# Start development server
pnpm dev

# Application will be available at http://localhost:5173
```

---

## Project Structure

```
src/
├── main.jsx                    # React entry point
├── App.jsx                     # Main app component
├── App.css                     # Global styles
├── index.css                   # Global CSS
├── api.js                      # Axios API client
│
├── components/                 # Reusable components
│   ├── EventManagement.jsx     # Event CRUD operations
│   ├── HallBookingForm.jsx     # Hall booking form
│   ├── AdminUserManagement.jsx # Admin user management
│   ├── AdminClubManagement.jsx # Admin club management
│   ├── AdminMenteeAssignment.jsx # Mentor-mentee assignment
│   ├── AdminAICTEConfig.jsx    # AICTE configuration
│   ├── AdminReporting.jsx      # Admin reporting
│   ├── Navbar.jsx              # Navigation bar
│   ├── Notifications.jsx       # Notification center
│   ├── ErrorBoundary.jsx       # Error boundary wrapper
│   ├── EventCard.jsx           # Event card component
│   └── Reports.jsx             # Reports component
│
├── pages/                      # Page components
│   ├── LandingPage.jsx         # Home page
│   ├── LoginPage.jsx           # Login page
│   ├── SignupPage.jsx          # Registration page
│   ├── ProfilePage.jsx         # User profile
│   ├── StudentDashboard.jsx    # Student dashboard
│   ├── ClubDashboard.jsx       # Club organizer dashboard
│   ├── MentorDashboard.jsx     # Mentor dashboard
│   ├── AdminDashboard.jsx      # Admin dashboard
│   ├── EmailVerificationPage.jsx # Email verification
│   ├── ForgotPasswordPage.jsx  # Password reset
│   ├── AssignMentees.jsx       # Mentee assignment
│   └── ...
│
├── context/                    # React Context
│   └── AuthContext.jsx         # Authentication context
│
├── assets/                     # Images, icons, etc.
│
└── styles/                     # Component-specific styles
```

---

## Available Scripts

### Development

```bash
# Start development server with HMR
pnpm dev

# Build for production
pnpm build

# Preview production build locally
pnpm preview

# Run linter
pnpm lint

# Fix linting issues
pnpm lint --fix
```

### Environment Configuration

Create `.env` file in project root:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api

# App Configuration (optional)
VITE_APP_NAME=CertifyTrack
VITE_APP_VERSION=2.1.0
VITE_DEBUG=false
```

For production:

```env
VITE_API_BASE_URL=https://api.yourdomain.com/api
VITE_DEBUG=false
```

---

## Components Guide

### EventManagement Component

Full event CRUD for club organizers with status management.

```jsx
import EventManagement from "../components/EventManagement";

function ClubDashboard() {
  return (
    <EventManagement
      onEventCreated={(event) => console.log("Event created:", event)}
      onEventUpdated={(event) => console.log("Event updated:", event)}
    />
  );
}
```

**Features:**

- Create new events
- Edit existing events
- Delete draft events
- Update event status (draft → scheduled → ongoing → completed)
- View event registrations
- Real-time success/error notifications

### HallBookingForm Component

Smart hall booking with real-time availability checking.

```jsx
import HallBookingForm from "../components/HallBookingForm";

function ClubDashboard() {
  return (
    <HallBookingForm
      onBookingCreated={(booking) => console.log("Booking created:", booking)}
    />
  );
}
```

**Features:**

- Dynamic hall availability based on date/time
- Conflict prevention
- Real-time availability feedback
- Hall capacity and location display
- Error handling for conflicts

### Navbar Component

Navigation and user menu.

```jsx
import Navbar from "../components/Navbar";

function App() {
  return (
    <>
      <Navbar />
      {/* Page content */}
    </>
  );
}
```

**Features:**

- Navigation links by user role
- User profile menu
- Logout functionality
- Responsive design

### ErrorBoundary Component

Error handling wrapper for components.

```jsx
import ErrorBoundary from "../components/ErrorBoundary";

function App() {
  return (
    <ErrorBoundary>
      <YourComponent />
    </ErrorBoundary>
  );
}
```

---

## API Integration

### Using the API Client

```jsx
import api from "../api";

// GET request
const response = await api.get("/events/");

// POST request
const response = await api.post("/events/", {
  name: "Event Name",
  event_date: "2025-12-01",
  start_time: "10:00",
});

// PATCH request
const response = await api.patch(`/events/${id}/`, {
  status: "scheduled",
});

// DELETE request
await api.delete(`/events/${id}/`);

// With query parameters
const response = await api.get("/events/", {
  params: { club: true },
});
```

### Error Handling

```jsx
try {
  const response = await api.get("/events/");
  setEvents(response.data);
} catch (error) {
  const message = error.response?.data?.detail || "An error occurred";
  setError(message);
}
```

### Authentication

```jsx
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

function MyComponent() {
  const { user, token, login, logout } = useContext(AuthContext);

  if (!user) {
    return <div>Please login</div>;
  }

  return <div>Welcome, {user.username}</div>;
}
```

---

## Styling with Tailwind CSS

The project uses Tailwind CSS for styling. Common utilities:

```jsx
// Spacing
<div className="p-4 m-2">Padding and margin</div>

// Colors
<div className="bg-blue-500 text-white">Blue background</div>

// Responsive
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  Responsive grid
</div>

// Flexbox
<div className="flex justify-between items-center">
  Flex layout
</div>

// Forms
<input className="px-4 py-2 border border-gray-300 rounded-lg" />
<button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
  Click me
</button>
```

See [Tailwind CSS Documentation](https://tailwindcss.com/docs) for complete reference.

---

## State Management

### AuthContext

Manages authentication state globally.

```jsx
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

function MyComponent() {
  const { user, token, isAuthenticated, login, logout, isAdmin } =
    useContext(AuthContext);

  return (
    <>
      {isAuthenticated ? (
        <>
          <p>Welcome, {user.username}</p>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <p>Please login</p>
      )}
    </>
  );
}
```

### Local Component State

```jsx
import { useState, useEffect } from "react";

function EventList() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const response = await api.get("/events/");
      setEvents(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {events.map((e) => (
        <div key={e.id}>{e.name}</div>
      ))}
    </div>
  );
}
```

---

## React Router

The application uses React Router for navigation.

```jsx
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<StudentDashboard />} />
        <Route path="/404" element={<NotFound />} />
      </Routes>
    </Router>
  );
}
```

---

## Form Handling

Example of a controlled form component:

```jsx
import { useState } from "react";
import api from "../api";

function EventForm() {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    event_date: "",
    start_time: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/events/", formData);
      console.log("Event created:", response.data);
      // Reset form or redirect
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="text-red-600">{error}</div>}

      <input
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="Event Name"
        required
      />

      <button type="submit" disabled={loading}>
        {loading ? "Creating..." : "Create Event"}
      </button>
    </form>
  );
}
```

---

## Performance Optimization

### Code Splitting

```jsx
import { lazy, Suspense } from "react";

const AdminDashboard = lazy(() => import("./pages/AdminDashboard"));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <AdminDashboard />
    </Suspense>
  );
}
```

### Memoization

```jsx
import { memo } from "react";

const EventCard = memo(function EventCard({ event }) {
  return <div>{event.name}</div>;
});

export default EventCard;
```

---

## Build & Deployment

### Build for Production

```bash
# Build the project
pnpm build

# Output goes to dist/ folder
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# For production
vercel --prod
```

### Deploy to Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=dist
```

---

## Troubleshooting

### Port Already in Use

```bash
# On Linux/macOS
lsof -ti:5173 | xargs kill -9

# On Windows (PowerShell)
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Node Modules Issues

```bash
# Clear cache
pnpm store prune

# Reinstall dependencies
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### API Connection Issues

1. Check if backend is running: `http://localhost:8000/api/`
2. Verify VITE_API_BASE_URL in `.env`
3. Check CORS settings in Django backend
4. Check browser console for errors

---

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari 14+, Chrome Android)

---

## Contributing

1. Create a feature branch
2. Follow the existing code style
3. Test your changes
4. Create a pull request

### Code Style

- Use functional components
- Use hooks (useState, useEffect, etc.)
- Use meaningful variable names
- Add comments for complex logic
- Follow Prettier formatting

---

## Support

For issues and questions:

- Open an issue on GitHub
- Check existing documentation
- Review API integration guide

---

## License

MIT License - See LICENSE file for details

---

**Last Updated**: November 22, 2025
