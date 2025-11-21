# CertifyTrack - Unified Platform for AICTE Points, Certificates, Events & Hall Bookings

![Version](https://img.shields.io/badge/version-2.1-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![Node](https://img.shields.io/badge/node-16+-green)
![Django](https://img.shields.io/badge/Django-5.2+-darkgreen)
![React](https://img.shields.io/badge/React-19.1+-blue)

## Overview

CertifyTrack is a comprehensive web-based platform designed to automate and streamline academic event management, institutional hall booking, digital certificate generation, and AICTE activity point tracking for technical educational institutions.

### Key Features

✨ **Multi-Role User Management** - Support for students, mentors, club organizers, and administrators
📅 **Event Lifecycle Management** - Full event creation, scheduling, execution, and completion workflow
🏛️ **Smart Hall Booking System** - Real-time availability checking with conflict prevention
📜 **Digital Certificate Generation** - Automated certificate creation with QR code verification
🎯 **AICTE Point Tracking** - Activity point allocation, approval, and audit trails
📊 **Comprehensive Reporting** - Analytics, attendance reports, and point distribution views
⚡ **Real-time Notifications** - Email/in-app alerts for critical events
🔐 **Role-Based Access Control** - Granular permissions for each user type

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Database Management](#database-management)
- [API Documentation](#api-documentation)
- [User Roles & Permissions](#user-roles--permissions)
- [Features Guide](#features-guide)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## Tech Stack

### Backend
- **Framework**: Django 5.2+
- **API**: Django REST Framework 3.16+
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL 15+ (or SQLite for development)
- **CORS**: django-cors-headers
- **PDF Generation**: ReportLab, PyPDF2
- **Task Queue**: Celery (optional for background tasks)
- **Cache**: Redis (optional)

### Frontend
- **Framework**: React 19.1+
- **Build Tool**: Vite 5+
- **Styling**: Tailwind CSS 4.1+
- **HTTP Client**: Axios 1.12+
- **Routing**: React Router 7.9+
- **Authentication**: JWT tokens
- **State Management**: React Context API

### Development Tools
- **Version Control**: Git
- **Package Manager**: pip (Python), pnpm (Node.js)
- **Code Quality**: ESLint, Black (optional)
- **Testing**: pytest (backend), Jest (frontend)

---

## Project Structure

```
CertifyTrack/
├── BackEnd/
│   ├── api/
│   │   ├── models.py              # Django models (User, Event, Hall, etc.)
│   │   ├── views.py               # API ViewSets and Views
│   │   ├── serializers.py         # DRF Serializers
│   │   ├── permissions.py         # Custom permission classes
│   │   ├── urls.py                # API URL routing
│   │   ├── email_utils.py         # Email utilities
│   │   ├── signals.py             # Django signals
│   │   ├── admin.py               # Django admin configuration
│   │   └── management/
│   │       └── commands/
│   │           ├── seed_halls.py           # Seed hall data
│   │           ├── set_admin_email.py      # Configure admin email
│   │           └── verify_all_admins.py    # Verify admin accounts
│   ├── CertifyTrack/
│   │   ├── settings.py            # Django settings
│   │   ├── urls.py                # Main URL configuration
│   │   ├── asgi.py                # ASGI config
│   │   └── wsgi.py                # WSGI config
│   ├── manage.py                  # Django CLI
│   ├── requirements.txt           # Python dependencies
│   ├── db.sqlite3                 # SQLite database (development)
│   └── README.md
│
├── FrontEnd/
│   ├── src/
│   │   ├── api.js                 # Axios API client
│   │   ├── App.jsx                # Main app component
│   │   ├── main.jsx               # React entry point
│   │   ├── components/
│   │   │   ├── EventManagement.jsx        # Event CRUD
│   │   │   ├── HallBookingForm.jsx        # Hall booking
│   │   │   ├── AdminUserManagement.jsx    # Admin user management
│   │   │   ├── AdminClubManagement.jsx    # Admin club management
│   │   │   ├── AdminMenteeAssignment.jsx  # Admin mentee assignment
│   │   │   ├── Navbar.jsx                 # Navigation
│   │   │   ├── Notifications.jsx          # Notifications
│   │   │   └── ErrorBoundary.jsx          # Error handling
│   │   ├── pages/
│   │   │   ├── ClubDashboard.jsx          # Club organizer dashboard
│   │   │   ├── AdminDashboard.jsx         # Admin dashboard
│   │   │   ├── StudentDashboard.jsx       # Student dashboard
│   │   │   ├── MentorDashboard.jsx        # Mentor dashboard
│   │   │   ├── ProfilePage.jsx            # User profile
│   │   │   ├── LoginPage.jsx              # Login
│   │   │   ├── SignupPage.jsx             # Registration
│   │   │   ├── LandingPage.jsx            # Home page
│   │   │   └── ...
│   │   ├── context/
│   │   │   └── AuthContext.jsx    # Authentication context
│   │   ├── assets/                # Images, fonts, etc.
│   │   └── styles/                # Global styles
│   ├── vite.config.js             # Vite configuration
│   ├── tailwind.config.js         # Tailwind CSS config
│   ├── package.json               # Node dependencies
│   ├── index.html                 # HTML entry point
│   └── README.md
│
├── CertifyTrack_SRSv2.1.md        # Software Requirements Specification
├── DATABASE_SCHEMA.md             # Database schema documentation
└── README.md                       # This file
```

---

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 22.04+), macOS, or Windows with WSL2
- **RAM**: Minimum 4GB, recommended 8GB+
- **Storage**: Minimum 2GB free space

### Required Software

#### Backend
- Python 3.12 or higher
- pip (Python package manager)
- PostgreSQL 15+ (optional, SQLite works for development)
- Git

#### Frontend
- Node.js 16+ (recommend 18+ LTS)
- pnpm 8+ (npm or yarn also work)
- Git

### Installation Commands

**Ubuntu/Debian:**
```bash
# Python and pip
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip

# Node.js (using NodeSource repository)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# pnpm
npm install -g pnpm

# PostgreSQL (optional)
sudo apt install postgresql postgresql-contrib
```

**macOS (using Homebrew):**
```bash
# Python
brew install python@3.12

# Node.js
brew install node

# pnpm
npm install -g pnpm

# PostgreSQL (optional)
brew install postgresql
```

---

## Installation & Setup

### Backend Setup

#### Step 1: Clone Repository
```bash
git clone https://github.com/PranavKadagadakai/CertifyTrack.git
cd CertifyTrack/BackEnd
```

#### Step 2: Create Virtual Environment
```bash
# Using venv
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate          # On Linux/macOS
# or
venv\Scripts\activate             # On Windows
```

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Environment Configuration
```bash
# Copy sample environment file
cp .env.sample .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

**Sample .env file:**
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Or PostgreSQL
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=certifytrack
# DB_USER=postgres
# DB_PASSWORD=your-password
# DB_HOST=localhost
# DB_PORT=5432

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Email Configuration (Gmail SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@certifytrack.com

# JWT Settings
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

#### Step 5: Database Migration
```bash
# Apply migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts to set username, email, and password
```

#### Step 6: Seed Sample Data
```bash
# Seed halls/venues
python manage.py seed_halls

# Output should show:
# ✓ Created hall: Auditorium A
# ✓ Created hall: Seminar Hall 1
# ... (more halls)
# ✓ Successfully seeded 8 new halls!
```

#### Step 7: Verify Installation
```bash
# Run development server
python manage.py runserver

# Should output:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

Navigate to http://localhost:8000/api in your browser. You should see the API root endpoint.

---

### Frontend Setup

#### Step 1: Navigate to Frontend Directory
```bash
cd ../FrontEnd
```

#### Step 2: Install Dependencies
```bash
# Using pnpm (recommended)
pnpm install

# Or using npm
npm install

# Or using yarn
yarn install
```

#### Step 3: Environment Configuration
```bash
# Create .env file for frontend
cat > .env << EOF
VITE_API_BASE_URL=http://localhost:8000/api
EOF
```

#### Step 4: Verify Installation
```bash
# Start development server
pnpm dev

# Output should show:
# > vite
# ➜  Local:   http://localhost:5173/
# ➜  press h to show help
```

Navigate to http://localhost:5173 in your browser. You should see the CertifyTrack landing page.

---

## Configuration

### Backend Configuration (`CertifyTrack/settings.py`)

**Important Settings to Review:**

```python
# Allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']

# CORS allowed origins
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:3000',
]

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # or sqlite3
        'NAME': 'certifytrack_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static and media files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Frontend Configuration (`.env`)

```env
# API Base URL
VITE_API_BASE_URL=http://localhost:8000/api

# Additional optional configs
VITE_APP_NAME=CertifyTrack
VITE_APP_VERSION=2.1.0
```

### Database Setup (PostgreSQL - Optional)

```bash
# Create database and user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE certifytrack;
CREATE USER certifytrack_user WITH PASSWORD 'your_secure_password';
ALTER ROLE certifytrack_user SET client_encoding TO 'utf8';
ALTER ROLE certifytrack_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE certifytrack_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE certifytrack TO certifytrack_user;
\q
```

---

## Running the Application

### Option 1: Development Mode (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd BackEnd
source venv/bin/activate          # Activate virtual environment
python manage.py runserver        # Runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd FrontEnd
pnpm dev                          # Runs on http://localhost:5173
```

Then open http://localhost:5173 in your browser.

### Option 2: Production Mode

**Backend:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn CertifyTrack.wsgi:application --bind 0.0.0.0:8000
```

**Frontend:**
```bash
# Build production bundle
pnpm build

# Preview (or serve with nginx)
pnpm preview
```

---

## Database Management

### Creating Backups

```bash
# SQLite
cp db.sqlite3 db.sqlite3.backup

# PostgreSQL
pg_dump certifytrack > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restoring from Backup

```bash
# PostgreSQL
psql certifytrack < backup_file.sql
```

### Resetting Database (Development Only)

```bash
# Delete migrations and database
rm db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Recreate database
python manage.py makemigrations
python manage.py migrate
python manage.py seed_halls
```

---

## API Documentation

### Authentication

All endpoints except `/auth/` require JWT authentication. Include token in header:

```bash
Authorization: Bearer <your_jwt_token>
```

### Key Endpoints

#### Authentication
- `POST /auth/register/` - Register new user
- `POST /auth/login/` - Login with credentials
- `POST /auth/token/refresh/` - Refresh JWT token
- `POST /auth/verify-email/` - Verify email
- `POST /auth/password-reset/request/` - Request password reset
- `POST /auth/password-reset/confirm/` - Confirm password reset

#### Events
- `GET /events/` - List all events
- `GET /events/?club=true` - List club's events
- `POST /events/` - Create event (club organizers)
- `PATCH /events/{id}/` - Update event
- `DELETE /events/{id}/` - Delete event
- `POST /events/{id}/register/` - Register for event (students)
- `POST /events/{id}/mark-attendance/` - Mark attendance

#### Hall Management
- `GET /halls/` - List all halls
- `GET /halls/available/?date=2025-11-22&start_time=10:00&end_time=11:00` - Get available halls
- `POST /hall-bookings/` - Create hall booking
- `GET /hall-bookings/` - List bookings
- `GET /hall-bookings/?club=true` - List club's bookings
- `PATCH /hall-bookings/{id}/` - Update booking

#### User Management (Admin)
- `POST /admin/users/create/` - Create user account
- `POST /admin/users/bulk-create/` - Bulk import users
- `GET /admin/users/` - List all users
- `PATCH /admin/users/{id}/` - Update user
- `DELETE /admin/users/{id}/` - Delete user

#### Profiles
- `GET /profile/` - Get current user profile
- `PATCH /profile/` - Update profile
- `GET /profile/student/` - Get student profile
- `GET /profile/mentor/` - Get mentor profile
- `GET /profile/club-organizer/` - Get club organizer profile

#### AICTE Points
- `GET /aicte-categories/` - List point categories
- `POST /aicte-transactions/` - Create point transaction
- `GET /aicte-transactions/` - List transactions
- `PATCH /aicte-transactions/{id}/` - Approve/reject points

### Example API Usage

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "user_type": "student",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'

# Get available halls
curl -X GET "http://localhost:8000/api/halls/available/?date=2025-11-22&start_time=10:00&end_time=11:00" \
  -H "Authorization: Bearer <token>"

# Create event
curl -X POST http://localhost:8000/api/events/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Workshop",
    "description": "Advanced Python Workshop",
    "event_date": "2025-11-23",
    "start_time": "10:00",
    "end_time": "12:00",
    "max_participants": 100
  }'
```

---

## User Roles & Permissions

### 1. **Student**
- Browse and register for events
- View registered events
- Download certificates
- Check AICTE point balance
- Update profile information
- View mentee reports

### 2. **Mentor**
- View assigned mentees
- Approve/reject AICTE points
- Generate mentee reports
- Monitor student engagement
- Manage mentee-mentor relationships

### 3. **Club Organizer**
- Create and manage club events
- Book halls/venues
- Mark event attendance
- Manage event registrations
- Generate certificates
- View event analytics

### 4. **Administrator**
- User account management (CRUD)
- Bulk user import
- Club management
- Mentor-mentee assignments
- AICTE point rule configuration
- Approve/reject hall bookings
- System monitoring and reporting
- Audit trail access

---

## Features Guide

### Event Management

**Creating an Event:**
1. Login as club organizer
2. Navigate to Club Dashboard → Events Management
3. Click "+ Create Event"
4. Fill in event details:
   - Event Name
   - Description
   - Date
   - Start/End Time
   - Max Participants
5. Click "Create Event"

**Updating Event Status:**
- **Draft → Scheduled**: Make event available for registration
- **Scheduled → Ongoing**: Start the event
- **Ongoing → Completed**: End event and generate certificates

### Hall Booking

**Booking a Hall:**
1. Navigate to Club Dashboard → Hall Bookings
2. Select date and time
3. System shows available halls for that slot
4. Select hall and click "Create Booking"
5. Wait for admin approval

**Conflict Prevention:**
- System automatically checks for overlapping bookings
- Only shows available halls in the dropdown
- Prevents double-booking of same venue

### AICTE Point Management

**Point Allocation:**
1. After event completion, system allocates points to attendees
2. Mentor reviews point allocations
3. Mentor approves or rejects with justification
4. Points reflected in student's account

**Point Tracking:**
- Students can view point transactions
- Detailed history with approval status
- Category-wise point breakdown

### Certificate Generation

**Automatic Workflow:**
1. Event is marked as completed
2. System generates PDF certificates for all attendees
3. Certificates include:
   - Student name
   - Event details
   - Issue date
   - QR code for verification
4. Certificates available for download

---

## Troubleshooting

### Common Issues and Solutions

#### Backend Issues

**Problem: `No module named 'django'`**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem: Database migration errors**
```bash
# Solution: Reset migrations (development only)
python manage.py migrate --fake api zero
python manage.py migrate
```

**Problem: `CORS error` from frontend**
```bash
# Solution: Add frontend URL to CORS_ALLOWED_ORIGINS in settings.py
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://yourdomain.com'
]
```

**Problem: `Port 8000 already in use`**
```bash
# Solution: Use different port
python manage.py runserver 8001
```

#### Frontend Issues

**Problem: `npm ERR! Cannot find module 'vite'`**
```bash
# Solution: Reinstall dependencies
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

**Problem: API requests failing (ECONNREFUSED)**
```bash
# Solution: Ensure backend is running
# Make sure VITE_API_BASE_URL in .env is correct
# Check if backend server is running on http://localhost:8000
```

**Problem: `Module not found` errors**
```bash
# Solution: Clear cache and rebuild
rm -rf .next dist
pnpm dev
```

#### Database Issues

**Problem: `PostgreSQL connection refused`**
```bash
# Solution: Check if PostgreSQL service is running
sudo service postgresql status
sudo service postgresql start
```

**Problem: `FATAL: Ident authentication failed`**
```bash
# Solution: Check pg_hba.conf authentication method
# Change to password authentication in /etc/postgresql/.../pg_hba.conf
```

### Debug Mode

**Enable Detailed Logging:**

Backend (`settings.py`):
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

Frontend (`.env`):
```env
VITE_DEBUG=true
```

---

## Development

### Project Setup for Contributors

```bash
# Fork and clone repository
git clone https://github.com/your-username/CertifyTrack.git
cd CertifyTrack

# Create feature branch
git checkout -b feature/your-feature-name

# Backend setup
cd BackEnd
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd ../FrontEnd
pnpm install

# Start development servers
# In separate terminals:
# Terminal 1: Backend
cd BackEnd && python manage.py runserver

# Terminal 2: Frontend
cd FrontEnd && pnpm dev
```

### Code Style Guidelines

**Python (Backend):**
- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Use type hints for function parameters
- Write docstrings for classes and functions

**JavaScript/React (Frontend):**
- Use 2 spaces for indentation
- Use functional components with hooks
- Use prop-types or TypeScript for type checking
- Write meaningful component names (PascalCase)

### Running Tests

**Backend:**
```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test api.tests.TestEventViewSet

# Run with coverage
coverage run --source='api' manage.py test
coverage report
```

**Frontend:**
```bash
# Run tests
pnpm test

# Run with coverage
pnpm test -- --coverage
```

### Making a Commit

```bash
# Stage changes
git add .

# Create meaningful commit message
git commit -m "feat(events): add event creation for club organizers

- Implement EventManagement component
- Add event CRUD endpoints
- Support event status lifecycle
- Add conflict detection for hall bookings

Fixes #123"

# Push to your branch
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>

Types: feat, fix, docs, style, refactor, perf, test, chore
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] Set `DEBUG=False` in settings.py
- [ ] Update `SECRET_KEY` to a secure random value
- [ ] Configure `ALLOWED_HOSTS` with actual domain
- [ ] Set up database (PostgreSQL recommended)
- [ ] Configure email backend
- [ ] Set up SSL/TLS certificates
- [ ] Configure static file serving (Nginx/Apache)
- [ ] Set up media file storage (S3/Cloud storage)
- [ ] Configure environment variables securely
- [ ] Run security checks

### Django Security Checklist

```bash
# Run Django security checks
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --noinput
```

### Nginx Configuration Example

```nginx
upstream certifytrack_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    redirect permanent https://yourdomain.com$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /api {
        proxy_pass http://certifytrack_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/certifytrack/staticfiles/;
    }

    location /media/ {
        alias /var/www/certifytrack/media/;
    }

    location / {
        proxy_pass http://localhost:3000;  # React app
    }
}
```

### Systemd Service File

Create `/etc/systemd/system/certifytrack.service`:

```ini
[Unit]
Description=CertifyTrack Application
After=network.target

[Service]
User=certifytrack
WorkingDirectory=/var/www/certifytrack/BackEnd
ExecStart=/var/www/certifytrack/venv/bin/gunicorn \
          --workers 4 \
          --bind 127.0.0.1:8000 \
          --error-logfile /var/log/certifytrack/error.log \
          --access-logfile /var/log/certifytrack/access.log \
          CertifyTrack.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable certifytrack
sudo systemctl start certifytrack
```

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Reporting Issues

When reporting issues, please include:
- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots/logs if applicable
- System information (OS, Python version, Node version, etc.)

---

## FAQ

**Q: Can I use SQLite for production?**
A: Not recommended. SQLite is suitable for development/testing only. Use PostgreSQL for production.

**Q: How do I update the certificate template?**
A: Contact your administrator. Certificate templates are managed globally and can only be updated by admin users.

**Q: Can students create events?**
A: No. Only club organizers and administrators can create events. Students can register for events.

**Q: How long are authentication tokens valid?**
A: JWT tokens are valid for 24 hours by default. Refresh tokens can be used to get new access tokens.

**Q: Is there a mobile app?**
A: Currently, only web application is available. Mobile app is planned for future releases.

---

## Support & Contact

- **Documentation**: See [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md) and [CertifyTrack_SRSv2.1.md](./CertifyTrack_SRSv2.1.md)
- **Issues**: GitHub Issues
- **Email**: support@certifytrack.com
- **Discord**: [Join Community](https://discord.gg/certifytrack)

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Acknowledgments

- AICTE Activity Point Guidelines (2024 Edition)
- Django REST Framework community
- React and Vite communities
- All contributors and testers

---

## Changelog

### Version 2.1.0 (Current)
- ✨ Added hall availability system with smart conflict detection
- ✨ Implemented complete event management for club organizers
- ✨ Enhanced club organizer dashboard with tab navigation
- 🔧 Fixed club organizer permissions and access control
- 🔧 Improved error handling and user feedback
- 📊 Added comprehensive reporting features
- 🐛 Fixed various UI/UX issues

### Version 2.0.0
- Initial release of CertifyTrack platform
- Multi-role user management
- Event and hall booking systems
- Certificate generation
- AICTE point tracking

---

**Last Updated**: November 22, 2025

For the latest updates, visit [CertifyTrack GitHub Repository](https://github.com/PranavKadagadakai/CertifyTrack)
