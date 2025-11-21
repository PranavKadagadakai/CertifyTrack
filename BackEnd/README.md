# CertifyTrack Backend

Django REST API backend for CertifyTrack platform - an academic event management and certification system.

## Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL 15+ (optional, SQLite works for development)
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/PranavKadagadakai/CertifyTrack.git
cd CertifyTrack/BackEnd

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Environment setup
cp .env.sample .env
# Edit .env with your configuration

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Seed initial data
python manage.py seed_halls

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000/api/` in your browser.

---

## Project Structure

```
api/
├── models.py              # Database models
├── views.py               # API ViewSets and Views
├── serializers.py         # DRF Serializers
├── permissions.py         # Custom permission classes
├── urls.py                # URL routing
├── email_utils.py         # Email utilities
├── signals.py             # Django signals
├── admin.py               # Django admin
├── tests.py               # Unit tests
├── management/
│   └── commands/
│       ├── seed_halls.py           # Seed halls data
│       ├── set_admin_email.py      # Set admin email
│       └── verify_all_admins.py    # Verify admins
└── migrations/            # Database migrations

CertifyTrack/
├── settings.py            # Django settings
├── urls.py                # URL configuration
├── asgi.py                # ASGI config
└── wsgi.py                # WSGI config
```

---

## Database Models

### User Management
- **User**: Custom user model with email and role-based access
- **Student**: Student profile with AICTE point tracking
- **Mentor**: Faculty mentor profile with mentee management
- **ClubOrganizer**: Club organizer profile

### Organization
- **Club**: Student clubs with coordinator assignment
- **ClubRole**: Role permissions (President, Secretary, etc.)
- **ClubMember**: Club membership tracking

### Events & Hall Booking
- **Event**: Event details with status lifecycle
- **EventRegistration**: Student event registration
- **EventAttendance**: Attendance tracking
- **Hall**: Hall/venue information
- **HallBooking**: Hall booking with conflict detection

### Certificates & AICTE
- **CertificateTemplate**: Global certificate template
- **Certificate**: Generated certificates for events
- **AICTECategory**: AICTE point categories
- **AICTEPointTransaction**: Point allocation tracking

### System
- **Notification**: User notifications
- **AuditLog**: Activity audit trail

---

## API Endpoints

### Authentication
```
POST   /auth/register/              Register new user
POST   /auth/login/                 Login with credentials
POST   /auth/token/refresh/         Refresh JWT token
POST   /auth/verify-email/          Verify email address
POST   /auth/resend-verification/   Resend verification email
POST   /auth/password-reset/request/ Request password reset
POST   /auth/password-reset/confirm/ Confirm password reset
```

### User Management
```
GET    /students/                   List all students
GET    /students/{id}/              Get student details
GET    /profile/                    Get current user profile
PATCH  /profile/                    Update current user profile
GET    /profile/student/            Get student profile
GET    /profile/mentor/             Get mentor profile
GET    /profile/club-organizer/     Get club organizer profile
```

### Events
```
GET    /events/                     List all events
GET    /events/?club=true           List club's events
POST   /events/                     Create event
GET    /events/{id}/                Get event details
PATCH  /events/{id}/                Update event
DELETE /events/{id}/                Delete event
POST   /events/{id}/register/       Register for event
POST   /events/{id}/start/          Start event
POST   /events/{id}/end/            End event
POST   /events/{id}/mark-attendance/ Mark attendance
POST   /events/{id}/generate-certificates/ Generate certificates
```

### Hall Management
```
GET    /halls/                      List all halls
GET    /halls/available/            Get available halls
POST   /hall-bookings/              Create booking
GET    /hall-bookings/              List bookings
GET    /hall-bookings/?club=true    List club's bookings
PATCH  /hall-bookings/{id}/         Update booking
DELETE /hall-bookings/{id}/         Cancel booking
```

### Club Management
```
GET    /clubs/                      List all clubs
POST   /clubs/                      Create club (admin)
PATCH  /clubs/{id}/                 Update club (admin)
GET    /club-members/               List club members
POST   /club-members/               Add club member (admin)
GET    /club-roles/                 List available roles
```

### Admin Operations
```
POST   /admin/users/create/         Create user account
POST   /admin/users/bulk-create/    Bulk import users
GET    /admin/users/                List all users
PATCH  /admin/users/{id}/           Update user
DELETE /admin/users/{id}/           Delete user
GET    /admin/clubs/                List and manage clubs
POST   /admin/mentees/assign/       Assign mentee to mentor
POST   /admin/mentees/bulk-assign/  Bulk assign mentees
GET    /admin/aicte/                Manage AICTE categories
GET    /admin/reports/              Generate reports
```

### AICTE Points
```
GET    /aicte-categories/           List point categories
POST   /aicte-categories/           Create category (admin)
GET    /aicte-transactions/         List point transactions
POST   /aicte-transactions/         Create transaction
PATCH  /aicte-transactions/{id}/    Approve/reject points
```

### Other
```
GET    /certificates/               List certificates
POST   /certificates/               Create certificate
GET    /certificate-templates/      List templates
PATCH  /certificate-templates/      Update template (admin)
GET    /notifications/              List notifications
GET    /audit-logs/                 View audit logs (admin)
GET    /dashboard/stats/            Dashboard statistics
```

---

## Authentication

### JWT Token Flow

```
1. User Login (POST /auth/login/)
   ├─ Request: {username, password}
   └─ Response: {access, refresh}

2. Use Access Token
   ├─ Header: Authorization: Bearer <access_token>
   └─ Valid for 24 hours

3. Token Expiration
   ├─ POST /auth/token/refresh/ with refresh token
   └─ Get new access token
```

### Example Login Request

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "user_type": "student"
  }
}
```

---

## Management Commands

### Seed Halls Data
```bash
python manage.py seed_halls
```
Creates 8 sample halls with different capacities and facilities.

### Set Admin Email
```bash
python manage.py set_admin_email
```
Configures admin email for notifications.

### Verify Admin Accounts
```bash
python manage.py verify_all_admins
```
Marks all admin accounts as email-verified.

---

## Configuration

### Environment Variables (`.env`)

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@certifytrack.com

# JWT
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### Settings for Production

In `CertifyTrack/settings.py`:

```python
# Security
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Database (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'certifytrack_db',
        'USER': 'certifytrack_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static and Media Files
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/certifytrack/staticfiles/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/certifytrack/media/'
```

---

## Permissions & Access Control

### User Types and Permissions

| Action | Student | Mentor | Club Org | Admin |
|--------|---------|--------|----------|-------|
| Register for events | ✅ | ✅ | ❌ | ❌ |
| Create events | ❌ | ❌ | ✅ | ✅ |
| Manage attendees | ❌ | ❌ | ✅ | ✅ |
| Book halls | ❌ | ❌ | ✅ | ✅ |
| Approve points | ❌ | ✅ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ❌ | ✅ |
| Configure system | ❌ | ❌ | ❌ | ✅ |

### Permission Classes

```python
# Custom permission classes in permissions.py
IsAdmin              # Only admins
IsClubAdmin          # Only club organizers
IsStudent            # Only students
IsMentor             # Only mentors
IsAdminOrReadOnly    # Admins can modify, others read-only
```

---

## Error Handling

### Common Error Responses

```json
{
  "detail": "Authentication credentials were not provided.",
  "code": "not_authenticated"
}
```

```json
{
  "detail": "You do not have permission to perform this action.",
  "code": "permission_denied"
}
```

```json
{
  "error": "Hall is not available for the selected time slot.",
  "conflicts": [...]
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Hall booking conflict |
| 500 | Server Error |

---

## Testing

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test api.tests.TestEventViewSet

# Run with verbosity
python manage.py test --verbosity=2

# Run with coverage
coverage run --source='api' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Writing Tests

```python
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import User, Event

class TestEventAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            user_type='club_organizer'
        )
        
    def test_create_event(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/events/', {
            'name': 'Test Event',
            'event_date': '2025-12-01',
            'start_time': '10:00',
        })
        self.assertEqual(response.status_code, 201)
```

---

## Deployment

### With Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run production server
gunicorn CertifyTrack.wsgi:application \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile /var/log/certifytrack/access.log \
  --error-logfile /var/log/certifytrack/error.log
```

### With Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "CertifyTrack.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## Troubleshooting

### Database Issues
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py seed_halls
```

### Migration Issues
```bash
# Create migrations
python manage.py makemigrations

# Show migration status
python manage.py showmigrations

# Revert migration
python manage.py migrate api 0001
```

### Import Errors
```bash
# Verify imports
python -c "import django; django.setup(); from api.models import *"
```

---

## Performance Optimization

### Query Optimization
```python
# Use select_related() and prefetch_related()
events = Event.objects.select_related('club', 'created_by').prefetch_related('registrations')

# Use only() and defer()
students = Student.objects.only('id', 'user_id', 'usn')
```

### Caching
```python
from django.core.cache import cache

# Cache hall availability
cache_key = f"halls_available_{date}_{start}_{end}"
available = cache.get(cache_key)
if not available:
    available = calculate_available_halls(date, start, end)
    cache.set(cache_key, available, 300)  # 5 minutes
```

### Database Indexing
Indexes are already configured in models for commonly queried fields.

---

## Security Best Practices

✅ **Implemented:**
- HTTPS/TLS enforcement
- CSRF protection
- XSS prevention
- SQL injection prevention (via ORM)
- Password hashing (bcrypt)
- JWT token validation
- CORS configuration
- Rate limiting (recommended: Django REST Throttling)

❗ **Recommendations:**
- Use environment variables for sensitive data
- Implement rate limiting on APIs
- Enable audit logging
- Regular security updates
- Use strong SECRET_KEY
- Implement API versioning

---

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Run tests: `python manage.py test`
5. Create pull request

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at `/api/` endpoint

---

## License

MIT License - See LICENSE file for details

---

**Last Updated**: November 22, 2025
