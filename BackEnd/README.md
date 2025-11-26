# CertifyTrack Backend

Django REST API backend for CertifyTrack platform - a comprehensive academic event management and certification system with AICTE activity point tracking.

## Overview

The backend provides a robust REST API with role-based access control for managing users, events, hall bookings, certificates, and AICTE points. Built with Django REST Framework, it features comprehensive authentication, audit logging, real-time notifications, and automated workflow management.

## Tech Stack

- **Framework**: Django 5.2.6 with Django REST Framework 3.16.1
- **Authentication**: JWT tokens (djangorestframework-simplejwt)
- **Database**: PostgreSQL preferred, SQLite supported for development
- **File Handling**: QR code generation, PDF processing
- **Email**: SMTP-based notifications with customization
- **Security**: Role-based permissions, audit logging, account lockout
- **Development**: uv for dependency management

## Prerequisites

- Python 3.12+
- PostgreSQL 15+ (recommended) or SQLite3
- Git

## Quick Installation

```bash
# Clone repository
git clone https://github.com/PranavKadagakai/CertifyTrack.git
cd CertifyTrack/BackEnd

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Environment setup
cp .env.example .env
# Edit .env with your database and email settings

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Seed sample data
python manage.py seed_halls

# Start development server
python manage.py runserver
```

## Project Structure

```
api/
├── models.py              # Database models with relationships
├── views.py               # ViewSets, API views, and business logic
├── serializers.py         # DRF serializers for API responses
├── permissions.py         # Custom permission classes for role-based access
├── urls.py                # URL routing configuration
├── email_utils.py         # Email sending utilities with templates
├── signals.py             # Django signals for automated workflows
├── admin.py               # Django admin configuration
├── management/commands/
│   ├── seed_halls.py          # Populates sample hall data
│   ├── set_admin_email.py     # Configures admin email settings
│   ├── verify_all_admins.py   # Verifies admin user emails
│   └── update_superuser_user_types.py  # Updates superuser roles
├── migrations/            # Database migrations
└── tests.py               # Unit tests

CertifyTrack/
├── settings.py            # Django configuration with security
├── urls.py                # Main URL routing
├── asgi.py                # ASGI config for async support
└── wsgi.py                # WSGI config for production

media/                    # Uploaded files (certificates, profiles)
templates/                # Django templates (if needed)

requirements.txt           # Python dependencies
pyproject.toml            # Project metadata and dependencies
uv.lock                   # Dependency lock file
manage.py                # Django CLI management
```

## Database Models

### Core Models

#### User Management

- **User**: Custom Django user model with email authentication and role-based access
  - Roles: `student`, `mentor`, `club_organizer`, `admin`
  - Features: email verification, account lockout, password reset
- **Student**: Profile with USN, department, semester, AICTE point tracking
- **Mentor**: Faculty profile with employee ID, qualifications, mentee management
- **ClubOrganizer**: Club organizer profile with club association

#### Organization

- **Club**: Student clubs with hierarchical structure (President, Secretary, etc.)
- **ClubRole**: Permission-based roles within clubs
- **ClubMember**: Club membership with role assignments

### Event Management

- **Event**: Comprehensive event model with lifecycle states
  - States: `draft`, `scheduled`, `ongoing`, `completed`, `cancelled`
  - Features: multi-day support, capacity limits, AICTE integration
- **EventRegistration**: Student event registrations with status tracking
- **EventAttendance**: Real-time attendance marking with QR integration

### Hall Booking System

- **Hall**: Venue management with capacity, facilities, and availability
- **HallBooking**: Smart booking with conflict detection and approval workflow
  - Automatic conflict checking for overlapping bookings
  - Admin approval system for conflict resolution

### Certificate Management

- **CertificateTemplate**: Versioned global certificate templates
- **Certificate**: Generated certificates with QR code verification
  - Features: SHA256 file hashing for integrity, automatic QR generation

### AICTE Points System

- **AICTECategory**: Configurable point categories with min/max limits
- **AICTEPointTransaction**: Point allocation with mentor approval workflow
  - States: `PENDING`, `APPROVED`, `REJECTED`

### System Features

- **Notification**: Comprehensive notification system with email integration
  - Types: event registrations, reminders, approvals, certificates, etc.
- **UserNotificationPreferences**: Granular notification control per user
- **AuditLog**: Complete audit trail for security and compliance

## API Endpoints

### Authentication & Registration

```
POST   /auth/register/              User registration with email verification
POST   /auth/login/                 JWT token authentication with account lockout
POST   /auth/verify-email/          Email verification
POST   /auth/resend-verification/   Resend verification email
POST   /auth/password-reset/request/  Request OTP-based password reset
POST   /auth/password-reset/confirm/ Confirm password reset with OTP
```

### Profile Management

```
GET    /profile/                    Get current user profile (role-specific)
PATCH  /profile/                    Update user profile and core fields
GET    /profile/student/            Student-specific profile data
PATCH  /profile/student/            Update student profile
GET    /profile/mentor/             Mentor-specific profile data
PATCH  /profile/mentor/             Update mentor profile
GET    /profile/club-organizer/     Organizer-specific profile data
PATCH  /profile/club-organizer/     Update organizer profile
```

### Student Management

```
GET    /students/                   List students (admin/mentor access)
GET    /students/mentees/           List mentor's assigned students
POST   /students/{id}/assign/       Assign student to mentor
```

### Mentor Management

```
GET    /mentors/                    List mentors (admin only)
GET    /mentors/{id}/mentees/       List students assigned to mentor
```

### Club Organizer Management

```
GET    /club-organizers/            List organizers (admin only)
POST   /club-organizers/{id}/assign-club/ Assign organizer to club
```

### Admin User Management

```
POST   /admin/users/create/         Create single user account
POST   /admin/users/bulk-create/    Bulk user creation from CSV
GET    /admin/users/                List all users with filtering
PATCH  /admin/users/{id}/           Update user account
POST   /admin/users/{id}/disable-account/ Disable user account
POST   /admin/users/{id}/enable-account/  Enable user account
POST   /admin/users/{id}/reset-password/ Reset user password
POST   /admin/users/{id}/unlock-account/ Unlock locked account
```

### Admin Club Management

```
GET    /admin/clubs/                List all clubs
POST   /admin/clubs/                Create new club with coordinator
PATCH  /admin/clubs/{id}/           Update club details
POST   /admin/clubs/{id}/assign-organizer/ Assign organizer to club
POST   /admin/clubs/{id}/assign-coordinator/ Change club coordinator
POST   /admin/clubs/{id}/assign-club-head/  Assign student club head
```

### Mentee Assignment Management

```
GET    /admin/mentees/              Get mentor-mentee assignments
POST   /admin/mentees/bulk-assign/  Bulk assignment from CSV
```

### Event Management

```
GET    /events/                     List events (with club filter)
POST   /events/                     Create new event (club organizer)
GET    /events/{id}/                Get event details
PATCH  /events/{id}/                Update event
DELETE /events/{id}/                Delete event
POST   /events/{id}/register/       Register for event (student)
POST   /events/{id}/upload-attendance/ Upload attendance via CSV/Excel
POST   /events/{id}/generate-certificates/ Generate certificates for attendees
GET    /events/{id}/participants/   Get participant list for attendance
```

### Hall & Booking Management

```
GET    /halls/                      List available halls
GET    /halls/available/            Get halls available for date/time
GET    /hall-bookings/              List club bookings
POST   /hall-bookings/              Create hall booking with conflict checking
GET    /hall-bookings/?club=true    List club's bookings
PATCH  /hall-bookings/{id}/         Update booking
POST   /hall-bookings/{id}/approve/ Approve pending booking (admin)
POST   /hall-bookings/{id}/reject/  Reject pending booking (admin)
GET    /hall-bookings/list_admin_pending/ List pending bookings (admin)
```

### AICTE Management

```
GET    /aicte-categories/           List AICTE categories
POST   /aicte-categories/           Create category (admin)
PATCH  /aicte-categories/{id}/      Update category (admin)
GET    /aicte-transactions/         List point transactions
POST   /aicte-transactions/{id}/approve/ Approve points (mentor)
POST   /aicte-transactions/{id}/reject/ Reject points (mentor)
```

### Certificate Management

```
GET    /certificates/               List user certificates
POST   /certificates/               Generate certificate
GET    /certificates/verify/{hash}/ Verify certificate by hash
GET    /certificate-templates/      List templates (admin)
POST   /certificate-templates/      Upload template (admin)
```

### Notification System

```
GET    /notifications/              List user notifications
POST   /notifications/mark_all_read/ Mark all as read
POST   /notifications/{id}/mark_read/ Mark single as read
POST   /notifications/{id}/take_action/ Take action on notification
```

### System Administration

```
GET    /admin/reports/system_stats/  System-wide statistics
GET    /admin/reports/audit_logs/   Audit logs with filtering
GET    /admin/reports/user_activity_report/ User activity statistics
GET    /admin/reports/event_statistics/ Event and attendance stats
GET    /admin/reports/hall_utilization_report/ Hall booking statistics
```

### Utility Endpoints

```
GET    /dashboard/stats/            Role-specific dashboard data
GET    /audit-logs/                Audit log browsing (admin)
```

## Authentication

### JWT Workflow

```
1. POST /auth/login/ with credentials
   → Returns {access: token, refresh: token, user: data}

2. Use access token in Authorization header
   Authorization: Bearer <access_token>

3. Refresh access token when expired
   POST /auth/token/refresh/ with refresh token
```

### Account Security

- **Account Lockout**: 5 failed login attempts → 15-minute lockdown
- **Email Verification**: Required for non-admin users
- **Password Reset**: OTP-based secure reset via email
- **Session Management**: JWT tokens with configurable expiration

## Permissions & Access Control

### Permission Classes

- `IsClubAdmin`: Club organizers and admins
- `IsStudent`: Student role only
- `IsMentor`: Mentor role only
- `IsAdmin`: Admin role only

### Access Matrix

| Feature          | Student | Mentor | Club Org  | Admin |
| ---------------- | ------- | ------ | --------- | ----- |
| View Events      | ✅      | ✅     | ✅        | ✅    |
| Register Events  | ✅      | ✅     | ❌        | ❌    |
| Create Events    | ❌      | ❌     | ✅ (club) | ✅    |
| Mark Attendance  | ❌      | ❌     | ✅ (club) | ✅    |
| Book Halls       | ❌      | ❌     | ✅ (club) | ✅    |
| Approve Bookings | ❌      | ❌     | ❌        | ✅    |
| User Management  | ❌      | ❌     | ❌        | ✅    |
| System Config    | ❌      | ❌     | ❌        | ✅    |
| View Reports     | ❌      | ❌     | ✅ (club) | ✅    |

## Smart Features

### Hall Booking Intelligence

- **Conflict Detection**: Automatic checking of overlapping bookings
- **Auto-Approval**: Immediate approval for non-conflicting bookings
- **Preference Assignment**: Primary/secondary hall selection with fallback
- **Admin Resolution**: Manual approval workflow for conflicts

### Event Workflow Automation

- **Hall Assignment**: Automatic venue assignment when events are scheduled
- **Notification Triggers**: Automated alerts for registration, approvals, certificates
- **Status Lifecycle**: Guided event management from draft to completion
- **Certificate Generation**: Bulk PDF generation with QR verification

### AICTE Points Management

- **Approval Workflow**: Mentor review and approval system
- **Category Validation**: Configurable point limits per category
- **Audit Trail**: Complete tracking of all point transactions
- **Student Tracking**: Real-time point balance monitoring

## Management Commands

### Database Seeding

```bash
python manage.py seed_halls
```

Creates 8 sample halls with different capacities and facilities.

### Admin Configuration

```bash
python manage.py set_admin_email
```

Configures admin email settings for notifications.

### User Verification

```bash
python manage.py verify_all_admins
```

Marks all admin accounts as email-verified.

### Superuser Updates

```bash
python manage.py update_superuser_user_types
```

Updates Django superuser accounts with proper user types.

## Configuration

### Environment Variables (`BackEnd/.env`)

```env
# Django Core
DEBUG=True
SECRET_KEY=your-very-long-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=certifytrack_db
DB_USER=certifytrack_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,https://yourfrontend.com

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@certifytrack.com

# JWT Configuration
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### Production Settings

In `CertifyTrack/settings.py`:

```python
# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000

# Database Optimization
DATABASES = {
    'default': {
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

# Static & Media Files
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/certifytrack/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/certifytrack/media/'
```

## API Usage Examples

### Event Creation

```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Workshop",
    "description": "Advanced Python programming",
    "event_date": "2025-01-15",
    "start_time": "14:00",
    "max_participants": 50,
    "aicte_category": 1,
    "points_awarded": 5
  }'
```

### Bulk Attendance Upload

```bash
curl -X POST http://localhost:8000/api/events/123/upload-attendance/ \
  -H "Authorization: Bearer <token>" \
  -F "file=@attendance.csv"
```

### Certificate Verification

```bash
GET /api/certificates/verify/sha256hash123/
# Returns certificate details or 404
```

## Development

### Testing

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test api.tests.TestEventViewSet -v 2

# Coverage report
coverage run --source='api' manage.py test
coverage report -m
```

### API Documentation

The API is self-documenting via Django REST Framework's browsable interface:

```
http://localhost:8000/api/
```

### Code Style

- Follow PEP 8 conventions
- Use type hints where applicable
- Write comprehensive docstrings
- Use meaningful variable names

## Production Deployment

### Docker Deployment

```bash
# Build and run with Docker
docker-compose up -d
```

### Gunicorn Configuration

```bash
gunicorn CertifyTrack.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120
```

### Nginx Proxy Configuration

```nginx
upstream django_backend {
    server 127.0.0.1:8000;
}

location /api/ {
    proxy_pass http://django_backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Troubleshooting

### Common Issues

**1. Database Connection Errors**

```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Create database manually
createdb certifytrack_db
```

**2. Permission Denied Errors**

- Ensure proper user permissions in Django admin
- Check role assignments for club organizers and mentors

**3. Email Not Sending**

- Verify SMTP settings in `.env`
- Check email provider credentials
- Ensure app passwords are used for Gmail

**4. File Upload Issues**

- Verify `MEDIA_ROOT` and `MEDIA_URL` settings
- Check file permissions on upload directories

## Security Features

- ✅ **JWT-based Authentication** with role-based access
- ✅ **Account Lockout** after failed login attempts
- ✅ **Email Verification** for account activation
- ✅ **Audit Logging** for all critical operations
- ✅ **File Upload Security** with validation
- ✅ **CORS Protection** with origin restrictions
- ✅ **Rate Limiting** (recommended for production)
- ✅ **SQL Injection Prevention** via ORM
- ✅ **XSS Protection** with Django security middleware

## Performance Optimization

- **Database Indexing** on frequently queried fields
- **Query Optimization** with select_related and prefetch_related
- **Efficient Serialization** with custom fields
- **Background Processing** for email notifications
- **Caching Strategy** (Redis recommended for production)

## Contributing

1. Create a feature branch
2. Write tests for new functionality
3. Follow code style guidelines
4. Update documentation

**Last Updated**: November 27, 2025
