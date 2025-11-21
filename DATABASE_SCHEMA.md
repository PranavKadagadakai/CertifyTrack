# CertifyTrack Database Schema Documentation

## Database Overview

CertifyTrack uses PostgreSQL (or SQLite for development) with the following table structure. All tables use `BigAutoField` as primary key by default.

---

## Core User Management Tables

### 1. auth_user (Extended via `User` model)

**Purpose**: Core authentication and user information

**Key Fields**:
- `id` (BigAutoField, PK)
- `username` (CharField, unique, max_length=150)
- `email` (EmailField, unique)
- `password` (CharField, hashed)
- `first_name`, `last_name` (CharField)
- `user_type` (CharField, choices: student/mentor/club_organizer/admin)
- `is_email_verified` (BooleanField, default=False)
- `email_verification_token` (CharField, nullable)
- `verification_sent_at` (DateTimeField, nullable)
- `password_reset_token` (CharField, nullable)
- `password_reset_expires` (DateTimeField, nullable)
- `failed_login_attempts` (IntegerField, default=0)
- `account_locked_until` (DateTimeField, nullable)
- `is_staff`, `is_superuser` (BooleanField)
- `date_joined` (DateTimeField, auto_now_add)
- `last_login` (DateTimeField, nullable)

**Indexes**: username, email, user_type

---

### 2. api_student

**Purpose**: Student profile and academic information

**Key Fields**:
- `id` (BigAutoField, PK)
- `user_id` (OneToOneField → User)
- `usn` (CharField, unique, max_length=20)
- `department` (CharField, max_length=100)
- `semester` (IntegerField, 1-8)
- `mentor_id` (ForeignKey → Mentor, nullable)
- `phone_number` (CharField, nullable)
- `date_of_birth` (DateField, nullable)
- `address` (TextField, nullable)
- `profile_photo` (ImageField, nullable)
- `emergency_contact_name` (CharField, nullable)
- `emergency_contact_phone` (CharField, nullable)
- `profile_completed` (BooleanField, default=False)
- `profile_completed_at` (DateTimeField, nullable)

**Indexes**: usn, mentor_id

---

### 3. api_mentor

**Purpose**: Mentor/Faculty profile and qualifications

**Key Fields**:
- `id` (BigAutoField, PK)
- `user_id` (OneToOneField → User)
- `employee_id` (CharField, unique, max_length=20)
- `department` (CharField, max_length=100)
- `designation` (CharField, max_length=100)
- `phone_number` (CharField, nullable)
- `date_of_birth` (DateField, nullable)
- `address` (TextField, nullable)
- `profile_photo` (ImageField, nullable)
- `qualifications` (TextField, nullable)
- `bio` (TextField, nullable)
- `profile_completed` (BooleanField, default=False)
- `profile_completed_at` (DateTimeField, nullable)

**Indexes**: employee_id

---

## Club Management Tables

### 4. api_club

**Purpose**: Club organization structure

**Key Fields**:
- `id` (BigAutoField, PK)
- `name` (CharField, unique, max_length=100)
- `description` (TextField, nullable)
- `faculty_coordinator_id` (ForeignKey → Mentor, nullable)
- `club_head_id` (ForeignKey → Student, nullable)
- `established_date` (DateField, nullable)
- `is_active` (BooleanField, default=True)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)

**Indexes**: name, is_active

---

### 5. api_clubrole

**Purpose**: Define permissions for each club position

**Key Fields**:
- `id` (BigAutoField, PK)
- `name` (CharField, unique, choices: president/secretary/treasurer/coordinator/member)
- `can_create_events` (BooleanField)
- `can_edit_events` (BooleanField)
- `can_delete_events` (BooleanField)
- `can_start_events` (BooleanField)
- `can_end_events` (BooleanField)
- `can_mark_attendance` (BooleanField)
- `can_manage_bookings` (BooleanField)
- `can_upload_templates` (BooleanField)
- `can_generate_certificates` (BooleanField)
- `can_view_reports` (BooleanField)
- `can_manage_members` (BooleanField)

---

### 6. api_clubmember

**Purpose**: Membership mapping with roles

**Key Fields**:
- `id` (BigAutoField, PK)
- `club_id` (ForeignKey → Club)
- `student_id` (ForeignKey → Student)
- `role_id` (ForeignKey → ClubRole)
- `joined_date` (DateTimeField, default=now)
- `is_active` (BooleanField, default=True)

**Unique Constraint**: (club_id, student_id)
**Indexes**: club_id, student_id, role_id

---

## Event Management Tables

### 7. api_event

**Purpose**: Event information and lifecycle management

**Key Fields**:
- `id` (BigAutoField, PK)
- `club_id` (ForeignKey → Club)
- `name` (CharField, max_length=200)
- `description` (TextField, nullable)
- `event_date` (DateField)
- `start_time` (TimeField)
- `end_time` (TimeField, nullable)
- `max_participants` (IntegerField, nullable)
- `status` (CharField, choices: draft/scheduled/ongoing/completed/cancelled, default='draft')
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)
- `created_by_id` (ForeignKey → User, nullable)

**Indexes**: status, event_date, club_id
**Ordering**: -event_date, -start_time

---

### 8. api_eventregistration

**Purpose**: Student registrations for events

**Key Fields**:
- `id` (BigAutoField, PK)
- `event_id` (ForeignKey → Event)
- `student_id` (ForeignKey → Student)
- `registration_date` (DateTimeField, default=now)
- `status` (CharField, choices: REGISTERED/ATTENDED/CANCELLED/NO_SHOW, default='REGISTERED')

**Unique Constraint**: (event_id, student_id)
**Indexes**: event_id & status, student_id & registration_date

---

### 9. api_eventattendance

**Purpose**: Attendance tracking for events

**Key Fields**:
- `id` (BigAutoField, PK)
- `event_id` (ForeignKey → Event)
- `student_id` (ForeignKey → Student)
- `marked_at` (DateTimeField, auto_now_add)
- `marked_by_id` (ForeignKey → User, nullable)
- `is_present` (BooleanField, default=True)

**Unique Constraint**: (event_id, student_id)
**Indexes**: event_id & student_id

---

## Hall/Venue Booking Tables

### 10. api_hall

**Purpose**: Physical venue/hall information

**Key Fields**:
- `id` (BigAutoField, PK)
- `name` (CharField, unique, max_length=100)
- `code` (CharField, unique, max_length=20)
- `location` (CharField, max_length=200, nullable)
- `capacity` (IntegerField)
- `facilities` (JSONField, nullable)
- `is_available` (BooleanField, default=True)

---

### 11. api_hallbooking

**Purpose**: Hall booking requests and approvals

**Key Fields**:
- `id` (BigAutoField, PK)
- `hall_id` (ForeignKey → Hall)
- `event_id` (ForeignKey → Event, nullable)
- `booked_by_id` (ForeignKey → ClubMember, nullable)
- `booking_date` (DateField)
- `start_time` (TimeField)
- `end_time` (TimeField)
- `booking_status` (CharField, choices: PENDING/APPROVED/REJECTED/CANCELLED, default='PENDING')
- `approved_by_id` (ForeignKey → User, nullable)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)
- `rejection_reason` (TextField, nullable)

**Indexes**: booking_date & hall_id, booking_status

---

## Certificate Tables

### 12. api_certificatetemplate

**Purpose**: Global institution certificate template

**Key Fields**:
- `id` (BigAutoField, PK)
- `name` (CharField, default='Global Certificate Template')
- `template_file` (FileField)
- `created_by_id` (ForeignKey → User, nullable)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)
- `is_active` (BooleanField, default=True)
- `version` (IntegerField, default=1)

**Note**: Single global template per institution. Version tracking for updates.

---

### 13. api_certificate

**Purpose**: Issued certificates for event attendees

**Key Fields**:
- `id` (BigAutoField, PK)
- `event_id` (ForeignKey → Event)
- `student_id` (ForeignKey → Student)
- `file` (FileField, upload_to='certificates/')
- `file_hash` (CharField, max_length=128, nullable)
- `issue_date` (DateTimeField, default=now)

**Indexes**: student_id, event_id
**Note**: file_hash used for verification endpoint

---

## AICTE Points Management Tables

### 14. api_aictecategory

**Purpose**: Define AICTE point categories and rules

**Key Fields**:
- `id` (BigAutoField, PK)
- `name` (CharField, unique, max_length=100)
- `description` (TextField, nullable)
- `min_points_required` (IntegerField, nullable)
- `max_points_allowed` (IntegerField, nullable)

**Validation**: min_points_required <= max_points_allowed

---

### 15. api_aictepointtransaction

**Purpose**: AICTE point allocation and approval workflow

**Key Fields**:
- `id` (BigAutoField, PK)
- `student_id` (ForeignKey → Student)
- `event_id` (ForeignKey → Event)
- `category_id` (ForeignKey → AICTECategory)
- `points_allocated` (IntegerField)
- `status` (CharField, choices: PENDING/APPROVED/REJECTED, default='PENDING')
- `approved_by_id` (ForeignKey → User, nullable)
- `approval_date` (DateTimeField, nullable)
- `rejection_reason` (TextField, nullable)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)

**Indexes**: student_id & status, event_id & category_id
**Ordering**: -created_at

---

## Notification & Audit Tables

### 16. api_notification

**Purpose**: User notifications (in-app, email, SMS)

**Key Fields**:
- `id` (BigAutoField, PK)
- `user_id` (ForeignKey → User)
- `title` (CharField, max_length=255)
- `message` (TextField)
- `created_at` (DateTimeField, auto_now_add)
- `expires_at` (DateTimeField, nullable)
- `is_read` (BooleanField, default=False)

**Indexes**: user_id, created_at

---

### 17. api_auditlog

**Purpose**: Audit trail for all system actions

**Key Fields**:
- `id` (BigAutoField, PK)
- `user_id` (ForeignKey → User)
- `action` (CharField, max_length=255)
- `timestamp` (DateTimeField, auto_now_add)

**Retention**: Minimum 3 years (configurable)
**Indexes**: user_id, timestamp

---

## Data Relationships Diagram

```
User
├── Student (OneToOne)
│   ├── mentor_id → Mentor
│   ├── club_memberships → ClubMember
│   ├── event_registrations → EventRegistration
│   ├── aicte_transactions → AICTEPointTransaction
│   └── certificates → Certificate
│
├── Mentor (OneToOne)
│   ├── mentees → Student
│   └── coordinated_clubs → Club
│
└── Admin (via user_type)

Club
├── faculty_coordinator_id → Mentor
├── club_head_id → Student
├── members → ClubMember
└── events → Event

Event
├── club_id → Club
├── created_by_id → User
├── registrations → EventRegistration
├── attendance_records → EventAttendance
├── hall_bookings → HallBooking
├── certificates → Certificate
└── aicte_transactions → AICTEPointTransaction

Hall
└── bookings → HallBooking

HallBooking
├── hall_id → Hall
├── event_id → Event
├── booked_by_id → ClubMember
└── approved_by_id → User

Certificate
├── event_id → Event
├── student_id → Student
└── template → CertificateTemplate (implicit via template_file)

AICTEPointTransaction
├── student_id → Student
├── event_id → Event
├── category_id → AICTECategory
└── approved_by_id → User
```

---

## Database Indexes

**Performance-Critical Indexes**:

```sql
-- User lookups
CREATE INDEX idx_user_username ON auth_user(username);
CREATE INDEX idx_user_email ON auth_user(email);

-- Student/Mentor lookups
CREATE INDEX idx_student_usn ON api_student(usn);
CREATE INDEX idx_mentor_employee_id ON api_mentor(employee_id);

-- Event filtering
CREATE INDEX idx_event_status_date ON api_event(status, event_date);
CREATE INDEX idx_event_club_id ON api_event(club_id);

-- Hall booking conflict detection
CREATE INDEX idx_hallbooking_date_hall ON api_hallbooking(booking_date, hall_id);
CREATE INDEX idx_hallbooking_status ON api_hallbooking(booking_status);

-- AICTE transactions
CREATE INDEX idx_aicte_student_status ON api_aictepointtransaction(student_id, status);
CREATE INDEX idx_aicte_event_category ON api_aictepointtransaction(event_id, category_id);

-- Registrations
CREATE INDEX idx_registration_event_status ON api_eventregistration(event_id, status);
CREATE INDEX idx_registration_student_date ON api_eventregistration(student_id, registration_date);

-- Notifications
CREATE INDEX idx_notification_user_created ON api_notification(user_id, created_at);

-- Audit logs
CREATE INDEX idx_auditlog_timestamp ON api_auditlog(timestamp);
```

---

## Constraints & Validations

**Unique Constraints**:
- `User.username`, `User.email`
- `Student.usn`
- `Mentor.employee_id`
- `Club.name`, `Hall.name`, `Hall.code`
- `AICTECategory.name`
- `(EventRegistration.event_id, EventRegistration.student_id)`
- `(ClubMember.club_id, ClubMember.student_id)`
- `(EventAttendance.event_id, EventAttendance.student_id)`
- `ClubRole.name`

**Foreign Key Constraints**:
- All ForeignKeys use `CASCADE` deletion by default
- Some use `SET_NULL` for optional relationships

---

## Capacity & Scalability

**Expected Scale**:
- Students: 0-50,000 per institution
- Events: 100-10,000 per year
- Certificates: 1,000-100,000+ per year
- AICTE Transactions: 10,000-100,000+ per year

**Optimization Strategies**:
- Partitioning by academic year for historical data
- Archiving old audit logs (> 3 years)
- Read replicas for reporting queries
- Caching frequently accessed templates

---

## Backup & Recovery

**Daily Backups**:
```bash
# PostgreSQL dump
pg_dump -U postgres -d certifytrack > backup_$(date +%Y%m%d).sql

# Django fixture
python manage.py dumpdata > backup_$(date +%Y%m%d).json
```

**Retention**: Minimum 30 days of daily backups + weekly long-term storage

---

## Migration Notes

After model changes, always:

```bash
# 1. Create migration
python manage.py makemigrations

# 2. Review migration file
cat api/migrations/000X_*.py

# 3. Apply migration
python manage.py migrate

# 4. Verify data integrity
python manage.py shell
# Run queries to verify
```

---

**Last Updated**: November 21, 2025  
**Database Version**: PostgreSQL 15+  
**Django ORM**: Django 5.x
