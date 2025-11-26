# CertifyTrack Frontend

React 19.1 + Vite frontend for CertifyTrack platform - a comprehensive academic event management and certification system with AICTE activity point tracking.

## Overview

The frontend provides a modern, responsive web interface built with React 19, Vite, and Tailwind CSS. It features role-based dashboards, real-time notifications, intelligent hall booking, and comprehensive event management capabilities.

## Tech Stack

- **Framework**: React 19.1 with functional components and hooks
- **Build Tool**: Vite 7.1 for fast development and optimized builds
- **Styling**: Tailwind CSS 4.1 with responsive design
- **HTTP Client**: Axios 1.12 for API requests
- **Routing**: React Router 7.9 for client-side navigation
- **State Management**: React Context API for authentication
- **Icons**: React Icons for consistent iconography
- **Development**: pnpm for package management

## Prerequisites

- Node.js 18+ (recommended)
- pnpm 8+ (npm/yarn are alternatives)
- Git

## Quick Installation

```bash
# Navigate to frontend directory
cd CertifyTrack/FrontEnd

# Install dependencies
pnpm install

# Create environment configuration
cat > .env << EOF
VITE_API_BASE_URL=http://localhost:8000/api
VITE_DEBUG=false
EOF

# Start development server
pnpm dev

# Application will be available at http://localhost:5173
```

## Project Structure

```
src/
├── main.jsx                    # React 19 entry point with StrictMode
├── App.jsx                     # Main app with routing and layouts
├── index.css                   # Tailwind base styles and globals
├── api.js                      # Axios client with interceptors
│
├── components/                 # Reusable UI components
│   ├── EventManagement.jsx     # Complete event CRUD with lifecycle management
│   ├── HallBookingForm.jsx     # Smart hall booking with conflict detection
│   ├── AdminUserManagement.jsx # Bulk user creation and management
│   ├── AdminClubManagement.jsx # Club creation and organizer assignment
│   ├── AdminMenteeAssignment.jsx # Mentor-student relationships
│   ├── AdminAICTEConfig.jsx    # AICTE category configuration
│   ├── AdminReporting.jsx      # Analytics and reporting dashboard
│   ├── AdminHallBookings.jsx   # Admin hall booking approval system
│   ├── EventAttendanceForm.jsx # CSV/Excel attendance upload
│   ├── Navbar.jsx              # Role-based navigation
│   ├── Notifications.jsx       # Real-time notification center
│   ├── ErrorBoundary.jsx       # Error handling component
│   ├── EventCard.jsx           # Event display card
│   └── Reports.jsx             # Report generation interface
│
├── pages/                      # Page-level components
│   ├── LandingPage.jsx         # Welcome page with features overview
│   ├── LoginPage.jsx           # JWT-based authentication
│   ├── SignupPage.jsx          # Multi-role registration
│   ├── ProfilePage.jsx         # Role-specific profile management
│   ├── StudentDashboard.jsx    # Student event registration
│   ├── ClubDashboard.jsx       # Club organizer management (tabbed)
│   ├── MentorDashboard.jsx     # Mentor approval workflows
│   ├── AdminDashboard.jsx      # Admin control center (tabbed)
│   ├── EmailVerificationPage.jsx # Email verification
│   ├── ForgotPasswordPage.jsx  # OTP-based password reset
│   ├── NotificationsPage.jsx   # Full notification history
│   └── AssignMentees.jsx       # Bulk mentee assignment
│
├── context/
│   └── AuthContext.jsx         # Global authentication state
│
└── assets/
    ├── bell-exclamation.svg    # Notification icon
    └── bell.svg               # Bell icon
```

## Available Scripts

### Development

```bash
# Start dev server with hot module replacement
pnpm dev              # http://localhost:5173

# Build for production
pnpm build           # Creates optimized bundle in dist/

# Preview production build
pnpm preview         # Test production build locally

# Lint code with ESLint
pnpm lint

# Auto-fix linting issues
pnpm lint --fix
```

## Environment Configuration

Create `.env` file in the project root:

```env
# Required
VITE_API_BASE_URL=http://localhost:8000/api

# Optional configuration
VITE_APP_NAME=CertifyTrack
VITE_APP_VERSION=2.1.0
VITE_DEBUG=false
```

For production deployment:

```env
VITE_API_BASE_URL=https://api.certifytrack.com/api
VITE_DEBUG=false
```

## Key Components

### Dashboard System

The application features tabbed dashboards tailored to each user role:

#### Admin Dashboard (`/admin-dashboard`)

- **Overview Tab**: System statistics and quick metrics
- **User Management**: Bulk user creation, account management
- **Club Management**: Club creation, organizer assignment
- **Mentee Assignment**: Bulk mentor-student relationships
- **AICTE Config**: Point categories and rules
- **Hall Bookings**: Admin approval for booking conflicts
- **Reports**: Comprehensive system analytics

#### Club Dashboard (`/club-dashboard`)

- **Events Tab**: Full CRUD operations with lifecycle management
- **Hall Bookings**: Smart booking with real-time availability
- **Reports**: Club-specific analytics and attendance data

#### Student Dashboard (`/student-dashboard`)

- **Events**: Browse and register for scheduled events
- **Certificates**: Download earned certificates
- **Profile**: Update personal and academic information

#### Mentor Dashboard (`/mentor-dashboard`)

- **Approvals**: Review and approve AICTE point transactions
- **Mentees**: View assigned students and their activities

### EventManagement Component

Comprehensive event lifecycle management for club organizers.

**Key Features:**

- Event creation with AICTE category selection
- Hall preference assignment (primary/secondary)
- Status transitions (Draft → Scheduled → Ongoing → Completed)
- Automated hall assignment on scheduling
- Attendance upload via CSV/Excel
- Certificate generation for attendees

**Usage:**

```jsx
<EventManagement onEventCreated={handleEventCreation} />
```

### HallBookingForm Component

Intelligent hall booking with conflict prevention.

**Key Features:**

- Real-time availability checking
- Dynamic hall filtering based on date/time
- Conflict detection and prevention
- Auto-approval for non-conflicting bookings
- Admin approval workflow for conflicts

**Usage:**

```jsx
<HallBookingForm onBookingCreated={handleBooking} />
```

### AdminUserManagement Component

Bulk user creation and account management interface.

**Key Features:**

- CSV upload for bulk user creation
- Role-specific profile generation
- Account status management (enable/disable/unlock)
- Password reset capabilities
- Email verification status tracking

## API Integration

### Axios Client Setup

```javascript
import api from "../api";

// All requests include JWT authentication headers
const events = await api.get("/events/");
const newEvent = await api.post("/events/", eventData);
```

### Error Handling

```javascript
try {
  const response = await api.get("/events/");
  setEvents(response.data);
} catch (error) {
  const message =
    error.response?.data?.detail ||
    error.response?.data?.error ||
    "Network error occurred";
  setError(message);
}
```

### Authentication Context

```jsx
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

function MyComponent() {
  const {
    user, // Current user object
    token, // JWT access token
    isAuthenticated,
    login, // (credentials) => Promise
    logout, // () => void
    isAdmin, // Boolean helpers
    isMentor,
    isClubOrganizer,
    isStudent,
  } = useContext(AuthContext);

  return <div>Welcome, {user?.username}!</div>;
}
```

## Styling with Tailwind CSS

The application uses Tailwind CSS v4 with a custom design system.

### Common Patterns

```jsx
// Layout grids
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

// Status badges
<span className="px-3 py-1 text-xs rounded bg-green-100 text-green-800">

// Form styling
<input className="w-full px-4 py-2 border border-gray-300 rounded-lg
                   focus:ring-2 focus:ring-blue-500 focus:border-transparent">

// Button variants
<button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg
                   transition-colors duration-200 disabled:opacity-50">
```

### Responsive Design

All components are fully responsive with mobile-first approach:

- Mobile: Single column layout
- Tablet: 2-column grids where appropriate
- Desktop: Multi-column layouts with sidebar navigation

## State Management

### Local Component State

```jsx
function EventList() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const response = await api.get("/events/");
      setEvents(response.data);
    } catch (err) {
      setError("Failed to load events");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-8">Loading events...</div>;
  if (error) return <div className="text-red-600 p-4 rounded">{error}</div>;

  return events.map((event) => <EventCard key={event.id} event={event} />);
}
```

### Global Authentication State

The `AuthContext` provides authentication state throughout the application:

```jsx
function App() {
  return (
    <AuthContext.Provider
      value={{
        user: currentUser,
        token: accessToken,
        isAuthenticated: !!token,
        // ... other auth methods
      }}
    >
      <AppRoutes />
    </AuthContext.Provider>
  );
}
```

## File Upload Handling

### CSV Upload for Attendance

```jsx
function AttendanceUpload({ eventId }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    try {
      const response = await api.post(
        `/events/${eventId}/upload-attendance/`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      console.log("Upload successful:", response.data);
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      setUploading(false);
    }
  };
}
```

### Supported File Formats

- **CSV**: Standard comma-separated values
- **Excel**: .xlsx and .xls formats for attendance data
- **Images**: Profile photos, club logos (PNG, JPG, GIF)

## Build & Deployment

### Production Build

```bash
# Create optimized production bundle
pnpm build

# This creates the dist/ directory with:
# - index.html
# - assets/ (JS, CSS, images)
# - Optimized chunks with hashing
```

### Environment-Specific Builds

The build process uses Vite's environment variable handling:

- Development: Hot module replacement, source maps
- Production: Minified assets, no source maps

### Deployment Options

#### Vercel (Frontend + API)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# For production domain
vercel --prod
```

#### Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy static files
netlify deploy --prod --dir=dist
```

#### Nginx Static Serving

```nginx
# Serve built files
location / {
    root /var/www/certifytrack/dist;
    try_files $uri $uri/ /index.html;
}
```

## Performance Optimization

### Code Splitting

Components are lazy-loaded for better initial page load:

```jsx
import { lazy, Suspense } from "react";

const AdminDashboard = lazy(() => import("./pages/AdminDashboard"));
const ClubDashboard = lazy(() => import("./pages/ClubDashboard"));

function App() {
  return (
    <Suspense fallback={<div className="text-center py-12">Loading...</div>}>
      <Routes>
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/club" element={<ClubDashboard />} />
      </Routes>
    </Suspense>
  );
}
```

### Asset Optimization

- **Image lazy loading** for profile photos
- **Font subset loading** for faster text rendering
- **CSS-in-JS extraction** for critical rendering path
- **Bundle analysis** for identifying optimization opportunities

## Testing Strategy

Run tests with:

```bash
# Unit tests (when implemented)
pnpm test

# E2E tests (when implemented)
pnpm test:e2e

# Coverage report
pnpm test -- --coverage
```

## Browser Support

- ✅ Chrome 90+ (recommended)
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari 14+, Chrome Android 90+)

## Development Guidelines

### Code Style

- Use functional components with hooks
- Prefer `useState` over class components
- Implement proper error boundaries
- Follow React naming conventions (PascalCase for components)
- Use meaningful variable names and comments

### File Organization

- One component per file
- Related utilities in separate modules
- Constants and configuration in dedicated files
- Tests co-located with components (future)

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-dashboard-component

# Commit changes
git add .
git commit -m "feat(dashboard): add new analytics component

- Add real-time statistics display
- Implement responsive chart components
- Add data refresh functionality

Closes #123"

# Create pull request
git push origin feature/new-dashboard-component
```

## Troubleshooting

### Common Development Issues

#### Port Conflicts

```bash
# Find process using port 5173
lsof -ti:5173 | xargs kill -9

# Or use different port
pnpm dev --port 5174
```

#### API Connection Issues

1. Verify `VITE_API_BASE_URL` in `.env`
2. Check backend CORS settings
3. Confirm backend is running (`http://localhost:8000/api/`)
4. Check browser network tab for request details

#### Build Issues

```bash
# Clear cache and rebuild
rm -rf node_modules/.vite
pnpm install
pnpm build
```

#### Tailwind CSS Issues

```bash
# Regenerate Tailwind classes
pnpm build  # This triggers CSS generation

# Check if classes are in final CSS
grep "bg-blue-600" dist/assets/index-*.css
```

## Contributing

1. **Setup**: Follow the installation guide above
2. **Branding**: Test changes across all user roles
3. **Responsiveness**: Verify mobile/tablet layouts
4. **Performance**: Test with real data loads
5. **PR**: Create descriptive pull request with screenshots

### Code Review Checklist

C[ ] Cmepnnowt fiplows]ex obing pitterns responsive design tested

- [c] Meblle respitcivs[d stgn tdsteu
  -p[t] Eerorrsaes hnded prl
- [ ]oadg statesimplemted
- [ ]-Accssibility onidrao(optoal)
- [ ]Performce ptimiz
- [ ]Tstsaddd/updatd(utu)

---

**Last Updated**: November 27, 2025
