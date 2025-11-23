# Software Requirements Specification (SRS)

## CertifyTrack - Unified Platform for AICTE Points, Certificates, Events & Hall Bookings

**Version:** 2.1  
**Date:** November 21, 2025  
**Prepared By:** Development Team  
**Document Standard:** IEEE 830-1998

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) document provides a comprehensive and detailed description of the functional and non-functional requirements for **CertifyTrack**. It serves as the primary reference for developers, testers, project managers, and stakeholders throughout the software development lifecycle.

The document aims to:

- Define system boundaries and capabilities
- Establish clear acceptance criteria for validation
- Serve as a contractual basis between stakeholders and development team
- Guide system architecture and design decisions
- Facilitate project planning and resource allocation

### 1.2 Scope

**System Name:** CertifyTrack

**System Overview:**  
CertifyTrack is a comprehensive web-based platform designed to automate and streamline academic event management, institutional hall booking, digital certificate generation, and AICTE activity point tracking for technical educational institutions.

**In Scope:**

- Multi-role user management (Students, Mentors, Club Organizers, Administrators)
- Event lifecycle management (creation, scheduling, execution, completion)
- Real-time hall/venue booking with conflict detection
- Single global template stored and maintained by administrators only. Template content (logos, layout, fonts) is fixed; only placeholder substitution is supported at run-time.
- AICTE activity point allocation, tracking, and validation
- Mentor approval workflow for student activity points
- Email/SMS notification system
- Comprehensive reporting and analytics
- Audit trails for all critical operations
- Role-based access control (RBAC)

**Out of Scope:**

- Integration with third-party LMS/ERP systems (future enhancement)
- Mobile native applications (future enhancement)
- Payment gateway integration
- External vendor management
- Inventory/asset management

**Benefits:**

- Elimination of manual spreadsheet-based tracking
- Zero venue double-booking through real-time availability checking
- Instant certificate generation with tamper-proof verification
- Transparent and auditable AICTE point allocation
- Reduced administrative overhead by 70%
- Improved student-mentor engagement
- Regulatory compliance assurance

### 1.3 Definitions, Acronyms, and Abbreviations

| Term        | Definition                                                                                                     |
| ----------- | -------------------------------------------------------------------------------------------------------------- |
| AICTE       | All India Council for Technical Education - regulatory body for technical education in India                   |
| API         | Application Programming Interface                                                                              |
| CRUD        | Create, Read, Update, Delete operations                                                                        |
| GDPR        | General Data Protection Regulation                                                                             |
| JWT         | JSON Web Token - authentication mechanism                                                                      |
| LMS         | Learning Management System                                                                                     |
| MVC         | Model-View-Controller architectural pattern                                                                    |
| OWASP       | Open Web Application Security Project                                                                          |
| PDF         | Portable Document Format                                                                                       |
| QR Code     | Quick Response Code - 2D barcode for verification                                                              |
| RBAC        | Role-Based Access Control                                                                                      |
| REST        | Representational State Transfer                                                                                |
| SPA         | Single Page Application                                                                                        |
| SRS         | Software Requirements Specification                                                                            |
| SMTP        | Simple Mail Transfer Protocol                                                                                  |
| SSL/TLS     | Secure Sockets Layer / Transport Layer Security                                                                |
| USN         | University Seat Number - unique student identifier                                                             |
| WCAG        | Web Content Accessibility Guidelines                                                                           |
| Placeholder | A named variable in the certificate template that will be substituted at generation time, e.g. {student_name}. |

### 1.4 References

1. IEEE Std 830-1998 - IEEE Recommended Practice for Software Requirements Specifications
2. AICTE Activity Point Guidelines (2024 Edition)
3. Django 5.x Official Documentation - https://docs.djangoproject.com
4. React 18 Documentation - https://react.dev
5. PostgreSQL 15 Documentation - https://www.postgresql.org/docs/15/
6. OWASP Top 10 Web Application Security Risks - https://owasp.org/www-project-top-ten/
7. WCAG 2.1 Level AA Guidelines - https://www.w3.org/WAI/WCAG21/quickref/

### 1.5 Document Overview

This SRS is organized into five major sections:

- **Section 1 (Introduction):** Provides context and overview
- **Section 2 (Overall Description):** Describes product perspective, user characteristics, and constraints
- **Section 3 (Specific Requirements):** Details functional and non-functional requirements
- **Section 4 (System Models):** Presents use cases, data models, and system architecture
- **Section 5 (Appendices):** Contains supplementary information

---

## 2. Overall Description

### 2.1 Product Perspective

CertifyTrack is a new, self-contained web application designed specifically for AICTE-affiliated technical educational institutions. The system architecture follows a modern three-tier model:

**Architecture Components:**

1. **Presentation Layer (Frontend)**

   - React 18-based Single Page Application (SPA)
   - Responsive Material-UI component library
   - Client-side routing and state management
   - Progressive Web App (PWA) capabilities

2. **Application Layer (Backend)**

   - Django 5.x framework with Django REST Framework
   - RESTful API design following OpenAPI 3.0 specification
   - Token-based authentication (JWT)
   - Business logic and validation layer
   - Background task processing (Celery)

3. **Data Layer**
   - PostgreSQL 15+ relational database
   - Redis for caching and session management
   - File storage for certificates and templates
   - Database connection pooling

**System Interfaces:**

- **User Interface:** Web-based responsive UI accessible via modern browsers
- **API Interface:** RESTful JSON APIs for frontend-backend communication
- **Email Interface:** SMTP/AWS SES for transactional emails
- **SMS Interface:** Third-party SMS gateway for notifications (optional)
- **Storage Interface:** Local/Cloud storage for PDF certificates and templates

**Deployment Model:**

- Containerized deployment using Docker
- Can be deployed on-premises or cloud (AWS, Azure, GCP)
- Horizontal scalability through load balancing
- Automated CI/CD pipeline support

### 2.2 Product Functions

The system provides the following major functional groups:

#### 2.2.1 User Management

- User registration and authentication
- Profile management with institutional details
- Password reset and recovery
- Role assignment and permission management
- User activity logging

#### 2.2.2 Event Management

- Event creation with detailed configuration
- Event scheduling with date/time selection
- Event status workflow (Draft → Scheduled → Ongoing → Completed/Cancelled)
- Event participant capacity management
- Event registration and waitlist management
- Event modification with audit trail

#### 2.2.3 Hall Booking System

- Real-time hall availability calendar
- Booking creation with time slot selection
- Conflict detection and prevention
- Booking approval workflow
- Booking modification and cancellation
- Hall resource allocation

#### 2.2.4 Certificate Generation

- Certificate template designer with WYSIWYG editor
- Bulk certificate generation upon event completion
- QR code embedding for verification
- PDF rendering with institutional branding
- Digital signature integration (optional)
- Certificate download and email delivery

#### 2.2.5 AICTE Points Management

- Activity point category configuration
- Rule-based point allocation
- Point credit upon event attendance
- Mentor validation workflow
- Point ledger with transaction history
- Point summary and reports

#### 2.2.6 Notification System

- Email notifications for critical events
- SMS notifications (optional)
- In-app notification center
- Configurable notification preferences
- Notification templates and scheduling

#### 2.2.7 Reporting and Analytics

- Student activity reports
- Event statistics and attendance reports
- Club performance analytics
- AICTE point distribution reports
- Hall utilization reports
- Export functionality (PDF, Excel, CSV)

### 2.3 User Classes and Characteristics

#### 2.3.1 Student

**Characteristics:**

- Primary end-users (500-5000 per institution)
- Age: 18-25 years
- Technical proficiency: Basic to Intermediate
- Access frequency: 2-5 times per week

**Key Tasks:**

- Browse and register for events
- View registered events and attendance
- Download certificates
- Check AICTE point balance
- Update personal profile

**Profile Management:**

- Students must complete comprehensive profile after first login
- Profile includes: personal details, contact info, emergency contact, photo
- Profile fields: full_name, phone_number, date_of_birth, address, emergency_contact_name, emergency_contact_phone, profile_photo
- Students can view and edit their complete profile
- Email verification required during registration

**Privileges (UPDATED):**

- View own complete profile and edit personal information
- View public events and registered events
- Register/unregister from events
- View own certificates and download them
- View AICTE point balance and transaction history
- Update profile information

#### 2.3.2 Mentor

**Characteristics:**

- Faculty members assigned to student groups
- Age: 30-60 years
- Technical proficiency: Intermediate
- Access frequency: 3-7 times per week

**Key Tasks:**

- Review mentee event registrations
- Validate AICTE points for assigned students
- Approve/reject point allocation
- Monitor student engagement
- Generate mentee reports

**Profile Management:**

- Mentors must complete comprehensive profile after first login
- Profile includes: personal/professional details, department, designation, qualifications
- Profile fields: full_name, phone_number, date_of_birth, address, employee_id (unique), designation, qualifications, bio, profile_photo
- Mentors can view and edit their complete profile
- Mentors can manage assigned mentees (student groups)

**Privileges (UPDATED):**

- View assigned mentees list and their profiles
- View all mentee activities and event attendance
- Approve/reject AICTE points for assigned students
- Override point allocation with justification
- Access mentee reports and activity history
- Assign/reassign mentees (if admin granted permission)
- View mentee certificates and verify them
- Generate mentee activity reports

#### 2.3.3 Club Organizer

**Characteristics:**

- Student club heads or faculty coordinators
- Technical proficiency: Intermediate to Advanced
- Access frequency: Daily

**Key Tasks:**

- Create and manage club events
- Book halls and venues
- Upload certificate templates
- Mark event attendance
- Manage event registrations
- Generate event reports

**Profile Management:**

- Club organizers must complete comprehensive profile after first login
- Profile fields: full_name, phone_number, date_of_birth, designation_in_club, bio, profile_photo
- Link to club coordination
- Can view and edit their profile

**Club Management (NEW):**

- Belong to exactly one club
- Club can have multiple members with different roles (President, Secretary, Treasurer, Coordinator, etc.)
- Club has one faculty coordinator (Mentor)
- Club members can create events, manage bookings

**Privileges (UPDATED):**

- Create/edit/delete club events
- Book and manage hall reservations
- Mark attendance for event participants
- View registration lists and manage participants
- Generate certificates upon event completion
- Access event analytics and reports
- Manage club members (if president)
- View and edit club details (if president)

#### 2.3.4 System Administrator

**Characteristics:**

- IT staff or designated super-users
- Technical proficiency: Advanced
- Access frequency: Daily

**Key Tasks:**

- Manage system-wide configurations
- Create and manage user accounts
- Resolve booking conflicts
- Configure AICTE point rules
- Monitor system health
- Manage roles and permissions

**User Management (NEW SECTION):**

- Create student accounts with bulk import capability
- Create mentor/faculty accounts
- Create club organizer accounts
- Enable/disable user accounts
- Reset user passwords
- View user activity logs
- Export user lists

**Club Management (NEW):**

- Create clubs with faculty coordinator assignment
- Assign club heads (student club presidents)
- View all clubs and their members
- Manage club members and their roles

**Mentor-Mentee Assignment (NEW):**

- Assign mentees to mentors manually or bulk
- Reassign mentees
- View mentor-mentee mapping
- Generate mentee assignment reports

**Privileges (UPDATED):**

- Full system access (superuser)
- User account management (CRUD) including batch creation
- Club and club member management
- Mentor-mentee assignment and management
- Role and permission assignment
- Configure AICTE point rules
- Approve hall bookings
- Monitor system health
- Database management
- Audit trail access
- Generate comprehensive system reports

### 2.4 Operating Environment

#### 2.4.1 Server Environment

- **Operating System:** Linux (Ubuntu 22.04 LTS or CentOS 8+)
- **Web Server:** Gunicorn with Nginx reverse proxy
- **Application Server:** Python 3.12+
- **Framework:** Django 5.x
- **Database:** PostgreSQL 15+
- **Cache:** Redis 7.x
- **Task Queue:** Celery with Redis broker

#### 2.4.2 Client Environment

- **Browsers:** Chrome 110+, Firefox 110+, Safari 15+, Edge 110+
- **Screen Resolutions:** 1366×768 minimum, responsive up to 4K
- **Network:** Broadband connection (minimum 2 Mbps)
- **Devices:** Desktop, Laptop, Tablet (iPad/Android)

#### 2.4.3 Development Environment

- **Version Control:** Git with GitHub/GitLab
- **IDE:** VS Code, PyCharm Professional
- **Package Management:** pip (Python), npm (Node.js)
- **Testing:** pytest, Jest, React Testing Library
- **CI/CD:** GitHub Actions, Jenkins

### 2.5 Design and Implementation Constraints

#### 2.5.1 Regulatory Constraints

- Must comply with AICTE activity point allocation guidelines
- GDPR-compliant data handling for EU users
- Data retention policies as per institutional guidelines
- Accessibility compliance (WCAG 2.1 Level AA)

#### 2.5.2 Technical Constraints

- Must use open-source technologies (Django, React, PostgreSQL)
- RESTful API architecture mandatory
- No vendor lock-in for cloud services
- Backward compatibility with PostgreSQL 15+
- Cross-browser compatibility required

#### 2.5.3 Business Constraints

- Project budget: To be determined by institution
- Development timeline: 6-9 months
- Deployment must not disrupt ongoing academic activities
- Training period of 2 weeks for administrators

#### 2.5.4 Security Constraints

- All data transmission must use HTTPS/TLS 1.3
- Password storage using bcrypt with minimum 12 rounds
- JWT tokens with 24-hour expiry
- SQL injection prevention through ORM
- XSS and CSRF protection mandatory
- Regular security audits required

#### 2.5.5 Data Constraints

- Certificates must be stored as immutable PDFs
- Certificate storage: Minimum 5 years
- Audit logs: Minimum 3 years retention
- Student records: Permanent storage
- Database backups: Daily automated backups

#### 2.5.6 Certificate Templates Constraints

- Certificate generation must rely on a single, institution-approved global template
- No club or event may override or customize appearance
- Audit logs: Minimum 3 years retention
- Dynamic placeholders only: participant and event fields

### 2.6 Assumptions and Dependencies

#### 2.6.1 Assumptions

- Institution has dedicated SMTP server or email service
- Each hall/venue has a unique identifier
- AICTE point allocation schema is provided by institution
- Users have basic computer literacy
- Institution provides server infrastructure or cloud budget
- Network connectivity is available in all campus areas
- Student USNs are unique and permanent
- Institutions prefer unified branding
- Template updates are rare

#### 2.6.2 Dependencies

- **External Services:**

  - Email delivery service (SMTP/AWS SES/SendGrid)
  - SMS gateway for notifications (optional - Twilio/AWS SNS)
  - QR code generation library (qrcode Python package)
  - PDF generation library (ReportLab/WeasyPrint)

- **Third-Party Libraries:**

  - Django REST Framework
  - Django CORS Headers
  - Celery for background tasks
  - Redis for caching
  - Pillow for image processing
  - PyJWT for token management

- **Infrastructure:**
  - PostgreSQL database server
  - Redis server
  - File storage system (local or S3-compatible)
  - Load balancer (for production)

---

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 User Management Module

**FR-UM-001: User Registration**

- **Priority:** High
- **Description:** System shall allow new users to register with institutional credentials
- **Input:** USN/Employee ID, email, password, personal details
- **Processing:** Validate unique identifiers, hash password, create user record
- **Output:** User account created, confirmation email sent
- **Acceptance Criteria:**
  - Email verification required before activation
  - Password must meet complexity requirements (min 8 chars, uppercase, lowercase, number, special char)
  - Support for three user types: Student, Mentor, Club Organizer
  - Username validation (unique)
  - User-type-specific field collection
  - Profile completion rate tracked

**FR-UM-002: User Authentication**

- **Priority:** High
- **Description:** System shall authenticate users using credentials and issue JWT tokens
- **Input:** Username/email and password
- **Processing:** Validate credentials, generate JWT token, create session
- **Output:** Authentication token, user role information
- **Acceptance Criteria:**
  - Maximum 5 failed login attempts before 15-minute lockout
  - Token expiry: 24 hours with automatic refresh
  - Password reset via email OTP (6 digits, 10-minute validity)

**FR-UM-003: Profile Management**

- **Priority:** Medium
- **Description:** Users shall create and update comprehensive personal profiles
- **Input:** Profile fields (name, phone, DOB, address, department, etc.)
- **Processing:** Validate data, store profile, update timestamp, log changes
- **Output:** Updated profile, success confirmation
- **Acceptance Criteria:**
  - Profile completion required within 48 hours of first login
  - All profile fields have validation rules
  - Phone number validation (10-15 digits)
  - Date of birth must be valid (18+ for students)
  - Address max 500 characters
  - Profile photo upload (max 2MB, JPG/PNG)
  - Email change requires verification
  - Profile edit history maintained for 1 year

**FR-UM-003A: View Full Profile (NEW)**

- **Description:** Users shall view their complete profile with all information
- **Input:** User ID
- **Processing:** Retrieve profile data, format for display
- **Output:** Complete profile view with editable fields
- **Acceptance Criteria:**
  - All fields displayed correctly
  - Profile completion status shown
  - Last updated timestamp visible
  - Profile photo displayed if exists

**FR-UM-003B: Edit Profile (NEW)**

- **Description:** Users shall edit their profile information
- **Input:** Updated profile fields
- **Processing:** Validate changes, update profile, log modification
- **Output:** Updated profile, confirmation message
- **Acceptance Criteria:**
  - Changes saved immediately
  - Audit trail maintained
  - Email change requires verification
  - Phone number format validated

**FR-UM-004: Role Management**

- **Priority:** High
- **Description:** Administrators shall manage user roles with bulk operations support
- **Input:** User ID(s), role assignment, effective date
- **Processing:** Validate permissions, update role, log assignment, notify user
- **Output:** Role updated, notification sent
- **Acceptance Criteria:**
  - Only admins can assign roles
  - Role changes logged in audit trail
  - User notified within 5 minutes
  - Support bulk role assignment (50+ users)

**FR-UM-005: Admin User Creation (NEW)**

- **Priority:** High
- **Description:** Administrators shall create student, mentor, and club organizer accounts
- **Input:** User details, role, role-specific fields
- **Processing:** Validate inputs, create user, send welcome email, generate temporary password
- **Output:** User created, welcome email sent, credentials provided
- **Acceptance Criteria:**
  - User creation for all three roles
  - Bulk import from CSV supported
  - Temporary password generated and sent
  - Email verification required
  - Admin receives creation confirmation
  - Student USN must be unique
  - Mentor employee ID must be unique

**FR-UM-006: Mentor-Mentee Assignment (NEW)**

- **Priority:** High
- **Description:** Administrators shall assign mentees to mentors
- **Input:** Mentor ID, Student ID(s)
- **Processing:** Validate mentor and students, create assignment, log action
- **Output:** Assignment created, notification sent to both
- **Acceptance Criteria:**
  - One-to-many assignment (1 mentor : N mentees)
  - Bulk assignment supported (50+ students)
  - Reassignment possible
  - Assignment history maintained
  - Both mentor and student notified
  - Cannot assign students without valid mentor

**FR-UM-007: Club Member Management (NEW)**

- **Priority:** High
- **Description:** System shall manage club members and their roles
- **Input:** Club ID, Student ID, Member Role, Faculty Coordinator ID
- **Processing:** Validate inputs, create club membership, assign role, create coordinator link
- **Output:** Membership created, notifications sent
- **Acceptance Criteria:**
  - Club has one faculty coordinator (Mentor)
  - Club can have multiple members (50+)
  - Member roles: President, Secretary, Treasurer, Coordinator, Member
  - Only club president can manage members
  - Coordinator is automatically a member
  - Activity history maintained

#### 3.1.2 Event Management Module

**FR-EM-001: Event Creation**

- **Priority:** High
- **Description:** Club organizers shall create events with complete details
- **Input:** Event name, description, date, time, venue, max participants, AICTE category, template
- **Processing:** Validate inputs, check venue availability, create event record
- **Output:** Event created in "Draft" status, event ID generated
- **Acceptance Criteria:**
  - Event date must be future date
  - Venue availability checked automatically
  - AICTE category selection from predefined list
  - Certificate template mandatory for point-bearing events

**FR-EM-002: Event Scheduling**

- **Priority:** High
- **Description:** Organizers shall schedule events and transition from Draft to Scheduled
- **Input:** Event ID, confirmation
- **Processing:** Validate hall booking, update status, send notifications
- **Output:** Event status changed to "Scheduled", confirmation emails sent
- **Acceptance Criteria:**
  - Hall booking must be confirmed
  - Cannot schedule if venue conflict exists
  - Notifications sent to all registered participants
  - Minimum 24-hour advance scheduling

**FR-EM-003: Event Registration**

- **Priority:** High
- **Description:** Students shall register for upcoming events
- **Input:** Event ID, student ID
- **Processing:** Check eligibility, verify capacity, create registration
- **Output:** Registration confirmation, email notification
- **Acceptance Criteria:**
  - Registration allowed only for scheduled events
  - Capacity limit enforced
  - Duplicate registration prevented
  - Student can register for maximum 10 active events
  - Registration deadline: 2 hours before event start

**FR-EM-004: Event Status Workflow**

- **Priority:** High
- **Description:** System shall manage event lifecycle transitions
- **States:** Draft → Scheduled → Ongoing → Completed/Cancelled
- **Transitions:**
  - Draft → Scheduled: Organizer confirms (hall booking required)
  - Scheduled → Ongoing: Organizer starts event (manual trigger)
  - Ongoing → Completed: Organizer ends event with attendance (manual trigger)
  - Any → Cancelled: Organizer/Admin cancels with reason
- **Acceptance Criteria:**
  - Only valid transitions allowed
  - State changes logged with timestamp and user
  - Notifications sent on state change
  - Cannot modify past events

**FR-EM-005: Event Attendance Marking**

- **Priority:** High
- **Description:** Organizers shall mark attendance for event participants
- **Input:** Event ID, student IDs, attendance status (Present/Absent)
- **Processing:** Validate event is ongoing/completed, update attendance records
- **Output:** Attendance marked, point allocation triggered for present students
- **Acceptance Criteria:**
  - Attendance can be marked only for ongoing or just-completed events
  - Bulk attendance marking supported
  - QR code scan option for quick check-in
  - Attendance can be modified within 24 hours of event completion

**FR-EM-006: Event Completion**

- **Priority:** High
- **Description:** System shall complete events and trigger certificate generation
- **Input:** Event ID, attendance list, completion confirmation
- **Processing:** Validate attendance marked, generate certificates, allocate points, update status
- **Output:** Event marked complete, certificates generated, points allocated
- **Acceptance Criteria:**
  - Attendance must be marked for all registered participants
  - Certificates generated only for present students
  - AICTE points allocated automatically
  - Event cannot be reopened after completion

**FR-EM-007: Event Modification**

- **Priority:** Medium
- **Description:** Organizers shall modify event details before completion
- **Input:** Event ID, updated fields, modification reason
- **Processing:** Validate permissions, update event, log changes, notify participants
- **Output:** Event updated, audit trail entry, notification sent
- **Acceptance Criteria:**
  - Only draft and scheduled events can be modified
  - Venue change requires new hall booking
  - Date/time change sends notification to all registered students
  - All changes logged in event edit history

**FR-EM-008: Event Cancellation**

- **Priority:** Medium
- **Description:** Organizers/Admins shall cancel events with justification
- **Input:** Event ID, cancellation reason
- **Processing:** Update status to cancelled, release hall booking, notify participants
- **Output:** Event cancelled, hall released, refund/credit processed
- **Acceptance Criteria:**
  - Cancellation reason mandatory
  - Notifications sent to all registered participants
  - Hall booking automatically released
  - Cancelled events visible in history but greyed out

#### 3.1.3 Hall Booking Module

**FR-HB-001: Hall Availability Calendar**

- **Priority:** High
- **Description:** System shall display real-time hall availability
- **Input:** Date range, hall filter
- **Processing:** Query bookings, calculate availability, render calendar
- **Output:** Interactive calendar showing available/booked slots
- **Acceptance Criteria:**
  - Calendar view: Day, Week, Month
  - Color coding: Green (available), Red (booked), Yellow (pending approval)
  - Filter by hall name, capacity, facilities
  - Minimum 15-minute time slots

**FR-HB-002: Hall Booking Creation**

- **Priority:** High
- **Description:** Organizers shall book halls for events
- **Input:** Hall ID, date, start time, end time, event ID, setup/cleanup buffer
- **Processing:** Check availability, prevent conflicts, create booking
- **Output:** Booking created, confirmation sent
- **Acceptance Criteria:**
  - Real-time conflict detection
  - Minimum 30-minute booking duration
  - Setup buffer: 30 minutes before, 15 minutes after
  - Booking requires admin approval (configurable)

**FR-HB-003: Booking Conflict Prevention**

- **Priority:** High
- **Description:** System shall prevent double-booking of halls
- **Input:** Booking request (hall, date, time range)
- **Processing:** Query existing bookings, check for overlaps including buffers
- **Output:** Booking allowed/rejected with conflict details
- **Acceptance Criteria:**
  - Zero tolerance for conflicts
  - Buffer times considered in conflict detection
  - Conflict details shown: existing event name, time, organizer
  - Alternative time slots suggested

**FR-HB-004: Booking Approval Workflow**

- **Priority:** Medium
- **Description:** Admins shall approve or reject hall booking requests
- **Input:** Booking ID, approval decision, comments
- **Processing:** Update booking status, notify organizer, confirm event schedule
- **Output:** Booking approved/rejected, notification sent
- **Acceptance Criteria:**
  - Approval required within 24 hours
  - Auto-rejection after 48 hours of pending
  - Rejection reason mandatory
  - Approved bookings locked from modification

**FR-HB-005: Booking Modification**

- **Priority:** Medium
- **Description:** Organizers shall modify bookings subject to availability
- **Input:** Booking ID, updated details
- **Processing:** Validate availability, check permissions, update booking
- **Output:** Booking modified, notifications sent
- **Acceptance Criteria:**
  - Modification allowed up to 48 hours before event
  - Requires fresh approval if major change (date/hall)
  - Original booking released if hall changed
  - Modification history maintained

**FR-HB-006: Booking Cancellation**

- **Priority:** Medium
- **Description:** Organizers shall cancel hall bookings
- **Input:** Booking ID, cancellation reason
- **Processing:** Release booking, update availability, notify stakeholders
- **Output:** Booking cancelled, hall released
- **Acceptance Criteria:**
  - Cancellation reason mandatory
  - Hall immediately available for re-booking
  - Cancellation logged with timestamp
  - Cannot cancel within 4 hours of event start

#### 3.1.4 Certificate Generation Module

**FR-CG-001: Certificate Template Management**

- **Priority:** High
- **Description:** The system shall use one global certificate template for all events. No event‑specific or club‑specific templates are allowed. This template is static in terms of visual design and branding (backgrounds, logos, borders, signatures) and can only be populated dynamically with event‑specific and participant‑specific data at generation time.
- **Input:** None (template is fixed and pre‑configured by the system administrator)
- **Processing:** Load the global template, validate placeholder availability, and allow administrators to update ONLY dynamic field positions (optional).
- **Output:** A single locked certificate template stored centrally.
- **Acceptance Criteria:**
  - Only ONE certificate template exists in the entire CertifyTrack system.
  - Template visual design is immutable except the following dynamically populated fields: {student_name}, {usn}, {event_name}, {club_name}, {event_date}, {issue_date}, {points}.
  - No club/event is allowed to upload or customize templates.
  - Administrators may reposition placeholders but cannot modify branding (logos, headers, backgrounds).
  - A4 PDF output maintained.

**FR-CG-002: Bulk Certificate Generation**

- **Priority:** High
- **Description:** The system shall generate certificates using the single global template. Event‑level customization of design is strictly prohibited. At event completion, dynamic data shall be merged into the template.
- **Input:** Event ID, attendance list
- **Processing:** For each participant, insert dynamic values into placeholders, embed QR code, and generate final PDF.
- **Output:** Individual PDF certificates for each attendee
- **Acceptance Criteria:**
  - Certificate design remains identical across all events.
  - Only dynamic data varies; visual assets remain unchanged.
  - QR code contains: certificate ID, student USN, event ID, issue date
  - File naming: {USN}_{EventID}_{Date}.pdf
  - Certificates generated within 5 minutes of event completion.

**FR-CG-003: Certificate Download**

- **Priority:** High
- **Description:** Students shall download their certificates
- **Input:** Student ID, certificate ID (optional)
- **Processing:** Retrieve certificate file, verify ownership, serve file
- **Output:** PDF certificate downloaded
- **Acceptance Criteria:**
  - Download limit: Unlimited
  - Certificate list filtered by event, date, status
  - Batch download option (zip file)
  - Download activity logged

**FR-CG-004: Certificate Verification**

- **Priority:** Medium
- **Description:** System shall verify certificate authenticity via QR code
- **Input:** QR code data or certificate ID
- **Processing:** Parse QR data, query database, validate details
- **Output:** Verification result with certificate details
- **Acceptance Criteria:**
  - Public verification page (no login required)
  - Displays: Student name, USN, event name, date, organizer
  - Tamper detection: checks file hash
  - Invalid/fake certificate detection

**FR-CG-005: Certificate Email Delivery**

- **Priority:** Medium
- **Description:** System shall email certificates to students automatically
- **Input:** Event completion trigger
- **Processing:** Generate certificates, compose email, send with attachment
- **Output:** Email with certificate PDF sent to student
- **Acceptance Criteria:**
  - Email sent within 10 minutes of generation
  - PDF attached (max 5MB)
  - Email body includes event details and congratulations message
  - Retry mechanism for failed deliveries (3 attempts)

#### 3.1.4.1 Impact on Other Modules

**Event Management (Revised Minimal Notes)**

- Event creation no longer requires selecting a certificate template.
- Remove all fields related to template selection from UI and backend.
- Certificate generation trigger remains unchanged.

**User Roles (Revised)**

- Club Organizers lose the ability to upload or modify templates.
- Only Administrators may modify placeholder coordinates (if supported).

**Reporting & Audit Trail**

- Audit logs no longer track per-club template uploads.

#### 3.1.5 AICTE Points Management Module

**FR-AP-001: Point Category Configuration**

- **Priority:** High
- **Description:** Admins shall configure AICTE point categories and rules
- **Input:** Category name, description, points range, validation rules
- **Processing:** Validate schema compliance, store configuration
- **Output:** Category configured, available for event assignment
- **Acceptance Criteria:**
  - Categories: Technical, Cultural, Sports, Social Service, etc.
  - Point range: 1-100 per activity
  - Maximum points per category per semester configurable
  - Rules include: eligibility criteria, approval requirements

**FR-AP-002: Automatic Point Allocation**

- **Priority:** High
- **Description:** System shall allocate points upon event completion
- **Input:** Event completion, attendance list, event point configuration
- **Processing:** Calculate points per student, create point transactions, set pending status
- **Output:** Points allocated to students, pending mentor approval
- **Acceptance Criteria:**
  - Points allocated only for present students
  - Point value from event configuration
  - Transaction status: Pending → Approved/Rejected
  - Student notified of point credit (pending)

**FR-AP-003: Point Validation Workflow**

- **Priority:** High
- **Description:** Mentors shall approve or reject point allocations
- **Input:** Student ID, transaction ID, approval decision, comments
- **Processing:** Update transaction status, credit/reject points, notify student
- **Output:** Points approved and added to ledger OR rejected with reason
- **Acceptance Criteria:**
  - Mentor can approve/reject for assigned mentees only
  - Batch approval supported
  - Rejection reason mandatory
  - Approval deadline: 7 days (auto-approve afterward)
  - Student notified within 5 minutes

**FR-AP-004: Point Ledger**

- **Priority:** High
- **Description:** Students shall view detailed point transaction history
- **Input:** Student ID, filter criteria (date range, category, status)
- **Processing:** Query transactions, calculate totals, render ledger
- **Output:** Detailed point ledger with transaction history
- **Acceptance Criteria:**
  - Columns: Date, Event Name, Category, Points, Status, Approved By
  - Filter by: Status (Pending/Approved/Rejected), Category, Date range
  - Total points by category displayed
  - Export to PDF/Excel

**FR-AP-005: Point Summary Report**

- **Priority:** Medium
- **Description:** System shall generate point summary for students and mentors
- **Input:** Student ID or mentor ID, academic year, semester
- **Processing:** Aggregate points by category, calculate totals, generate report
- **Output:** PDF/Excel report with point breakdown
- **Acceptance Criteria:**
  - Summary includes: Total points, category-wise breakdown, pending approvals
  - Comparison with minimum AICTE requirements
  - Graphical representation (pie/bar chart)
  - Mentor can generate for all mentees

**FR-AP-006: Point Override**

- **Priority:** Low
- **Description:** Mentors shall manually adjust point allocations with justification
- **Input:** Transaction ID, new point value, justification
- **Processing:** Validate permissions, update points, log override, notify student
- **Output:** Points adjusted, override logged in audit trail
- **Acceptance Criteria:**
  - Override reason mandatory (min 50 characters)
  - Only approved points can be overridden
  - Admins can override any transaction
  - Mentors can override only for their mentees
  - Override logged with timestamp, old value, new value

#### 3.1.6 Notification Module

**FR-NM-001: Email Notifications**

- **Priority:** High
- **Description:** System shall send email notifications for critical events
- **Triggers:**
  - User registration confirmation
  - Event registration confirmation
  - Event reminder (24 hours before)
  - Event cancellation
  - Certificate generation
  - Point allocation approval/rejection
  - Hall booking approval/rejection
- **Processing:** Compose email from template, populate variables, send via SMTP
- **Output:** Email delivered to recipient
- **Acceptance Criteria:**
  - HTML email templates with institutional branding
  - Delivery within 5 minutes of trigger
  - Retry mechanism for failures (3 attempts, exponential backoff)
  - Unsubscribe option (except mandatory notifications)
  - Delivery status tracking

**FR-NM-002: In-App Notifications**

- **Priority:** Medium
- **Description:** System shall display in-app notifications for user actions
- **Input:** User activity triggers
- **Processing:** Create notification record, push to user's notification center
- **Output:** Notification displayed in UI, badge count updated
- **Acceptance Criteria:**
  - Real-time notification delivery (WebSocket/polling)
  - Notification types: Info, Success, Warning, Error
  - Mark as read/unread functionality
  - Notification history retained for 30 days
  - Click notification to navigate to relevant page

**FR-NM-003: SMS Notifications**

- **Priority:** Low
- **Description:** System shall send SMS for urgent notifications (optional feature)
- **Triggers:**
  - Event cancellation (within 24 hours)
  - Emergency announcements
- **Processing:** Compose SMS, send via SMS gateway, log delivery
- **Output:** SMS delivered to registered mobile number
- **Acceptance Criteria:**
  - SMS limit: 160 characters
  - Delivery confirmation from gateway
  - Opt-in required for SMS notifications
  - Failure fallback to email

**FR-NM-004: Notification Preferences**

- **Priority:** Medium
- **Description:** Users shall configure notification preferences
- **Input:** User ID, notification settings (email, SMS, in-app toggles per event type)
- **Processing:** Update user preferences, save configuration
- **Output:** Preferences saved, applied to future notifications
- **Acceptance Criteria:**
  - Granular control per notification type
  - Cannot disable mandatory notifications (account security, legal)
  - Default settings: All notifications enabled
  - Preferences accessible in profile settings

#### 3.1.7 Reporting Module

**FR-RP-001: Student Activity Report**

- **Priority:** Medium
- **Description:** System shall generate comprehensive student activity reports
- **Input:** Student ID, date range, filter options
- **Processing:** Aggregate event registrations, attendance, points, certificates
- **Output:** PDF/Excel report with activity summary
- **Acceptance Criteria:**
  - Sections: Events attended, total points, certificates earned, pending approvals
  - Date range selector (semester, academic year, custom)
  - Graphical charts: Point distribution, attendance trend
  - Export formats: PDF, Excel, CSV

**FR-RP-002: Event Statistics Report**

- **Priority:** Medium
- **Description:** Organizers shall generate event performance reports
- **Input:** Event ID or date range, club filter
- **Processing:** Calculate metrics: registrations, attendance, completion rate
- **Output:** Report with event statistics and visualizations
- **Acceptance Criteria:**
  - Metrics: Total registrations, attendance count, attendance %, no-shows, points distributed
  - Comparison with previous events
  - Peak registration times analysis
  - Export to PDF/Excel

**FR-RP-003: Club Performance Analytics**

- **Priority:** Medium
- **Description:** Admins shall view club-level performance analytics
- **Input:** Club ID, date range, metrics selection
- **Processing:** Aggregate club events, attendance, student engagement
- **Output:** Dashboard with club performance metrics
- **Acceptance Criteria:**
  - Metrics: Total events conducted, average attendance, student participation rate
  - Club-to-club comparison
  - Trend analysis (monthly/semester)
  - Top performing clubs leaderboard

**FR-RP-004: AICTE Points Distribution Report**

- **Priority:** Medium
- **Description:** System shall generate institutional AICTE compliance reports
- **Input:** Date range, department filter, category filter
- **Processing:** Aggregate all student points, calculate distributions, identify gaps
- **Output:** Comprehensive AICTE compliance report
- **Acceptance Criteria:**
  - Category-wise point distribution
  - Students meeting/not meeting minimum requirements
  - Department-wise analysis
  - Compliance percentage calculation
  - Export for AICTE submission

**FR-RP-005: Hall Utilization Report**

- **Priority:** Low
- **Description:** Admins shall view hall booking and utilization statistics
- **Input:** Date range, hall filter
- **Processing:** Calculate booking hours, utilization rate, peak times
- **Output:** Hall utilization report with recommendations
- **Acceptance Criteria:**
  - Metrics: Total bookings, total hours, utilization %, idle time
  - Peak usage days/times heatmap
  - Most/least used halls
  - Booking approval rate

**FR-RP-006: Audit Trail Report**

- **Priority:** Medium
- **Description:** Admins shall access comprehensive audit logs
- **Input:** Date range, user filter, action type filter
- **Processing:** Query audit logs, format for readability
- **Output:** Detailed audit trail report
- **Acceptance Criteria:**
  - All critical actions logged: User creation, role changes, event modifications, point overrides
  - Fields: Timestamp, user, action, IP address, changes made
  - Filter by: User, date, action type, module
  - Export to CSV for external analysis

### Section 3.1.8 Club Management Module (NEW)

**FR-CM-001: Club Creation (NEW)**

- **Priority:** High
- **Description:** Administrators shall create clubs with faculty coordination
- **Input:** Club name, description, faculty coordinator (Mentor), establishment date
- **Processing:** Validate unique club name, create club record, link coordinator
- **Output:** Club created, confirmation sent to coordinator
- **Acceptance Criteria:**
  - Club name must be unique
  - Faculty coordinator must be a valid Mentor user
  - Establishment date optional
  - Club status: Active/Inactive
  - Coordinator notified of assignment

**FR-CM-002: Club Member Management (NEW)**

- **Priority:** High
- **Description:** Club presidents shall manage club members and their roles
- **Input:** Club ID, Student ID, Role, Action (add/remove/update)
- **Processing:** Validate permissions, create/update/delete membership, log action
- **Output:** Membership updated, notification sent
- **Acceptance Criteria:**
  - Only club president can modify members
  - Multiple roles supported
  - Member removal possible (keeps history)
  - Activity notifications sent
  - Max 200 members per club

**FR-CM-003: Club Coordinator Assignment (NEW)**

- **Priority:** High
- **Description:** Administrators shall assign faculty coordinators to clubs
- **Input:** Club ID, Mentor ID
- **Processing:** Validate mentor, update club coordinator, notify mentor
- **Output:** Coordinator assigned, notification sent
- **Acceptance Criteria:**
  - One coordinator per club
  - Coordinator must be Mentor user
  - Previous coordinator notified of change
  - One mentor can coordinate multiple clubs
  - Assignment history maintained

**FR-CM-004: Club Profile (NEW)**

- **Priority:** Medium
- **Description:** Users shall view complete club information
- **Input:** Club ID
- **Processing:** Retrieve club data, member list, coordinator info, event history
- **Output:** Complete club profile with member information
- **Acceptance Criteria:**
  - Club name, description, coordinator, member list visible
  - Member roles displayed
  - Recent events shown
  - Contact information displayed

### 3.2 Non-Functional Requirements

#### 3.2.1 Performance Requirements

**NFR-PF-001: Response Time**

- **Priority:** High
- **Requirement:** 95% of API requests shall complete within 500ms under normal load
- **Measurement:** Average response time measured by APM tool
- **Acceptance Criteria:**
  - Page load time: ≤ 2 seconds
  - API endpoints: ≤ 500ms (95th percentile)
  - Search queries: ≤ 1 second
  - Report generation: ≤ 5 seconds
  - Certificate generation: ≤ 3 seconds per certificate

**NFR-PF-002: Throughput**

- **Priority:** High
- **Requirement:** System shall support 500 concurrent users without degradation
- **Measurement:** Load testing with concurrent user simulation
- **Acceptance Criteria:**
  - 500 concurrent users: Normal performance
  - 1000 concurrent users: Graceful degradation (≤ 1s response time)
  - Peak load during event registration: 2000 simultaneous requests
  - Database connections: Connection pooling with max 100 connections
  - **Peak load during bulk operations:** 10,000 user imports
  - **Bulk mentee assignment:** 500 mentees per operation
  - **Bulk user creation:** 1,000 users per batch

**NFR-PF-003: Scalability**

- **Priority:** Medium
- **Requirement:** System architecture shall support horizontal scaling
- **Acceptance Criteria:**
  - Stateless API design for load balancing
  - Database read replicas supported
  - Caching layer (Redis) for frequently accessed data
  - CDN support for static assets and certificates
  - Support for 10,000+ registered users per institution

**NFR-PF-004: Database Performance**

- **Priority:** High
- **Requirement:** Database queries shall be optimized for performance
- **Acceptance Criteria:**
  - All tables properly indexed
  - Query execution time: ≤ 100ms for 90% of queries
  - Connection pooling enabled
  - Query optimization using EXPLAIN ANALYZE
  - No N+1 query problems

#### 3.2.2 Security Requirements

**NFR-SC-001: Authentication**

- **Priority:** Critical
- **Requirement:** System shall implement secure multi-factor authentication
- **Acceptance Criteria:**
  - Password hashing: bcrypt with minimum 12 rounds
  - JWT tokens for API authentication
  - Token expiry: 24 hours with refresh mechanism
  - Session timeout: 30 minutes of inactivity
  - Failed login lockout: 5 attempts, 15-minute lockout
  - Password complexity: Min 8 chars, uppercase, lowercase, number, special char
  - Password reset via email OTP (6 digits, 10-minute validity)

**NFR-SC-002: Authorization**

- **Priority:** Critical
- **Requirement:** System shall enforce role-based access control (RBAC)
- **Acceptance Criteria:**
  - Permissions checked at API level (not just UI)
  - Principle of least privilege enforced
  - No privilege escalation vulnerabilities
  - Admin actions require re-authentication
  - Unauthorized access returns HTTP 403 with generic message

**NFR-SC-003: Data Protection**

- **Priority:** Critical
- **Requirement:** System shall protect sensitive data at rest and in transit
- **Acceptance Criteria:**
  - All HTTP traffic over TLS 1.3
  - Sensitive fields encrypted in database (passwords, tokens)
  - Database connection encrypted
  - No sensitive data in logs
  - PII data anonymized in non-production environments
  - Certificate files stored with restricted access permissions

**NFR-SC-004: OWASP Top 10 Compliance**

- **Priority:** Critical
- **Requirement:** System shall mitigate OWASP Top 10 vulnerabilities
- **Acceptance Criteria:**
  - SQL Injection: ORM used, prepared statements
  - XSS: Input sanitization, output encoding, CSP headers
  - CSRF: CSRF tokens for state-changing operations
  - Broken Authentication: Secure session management
  - Sensitive Data Exposure: Encryption, secure headers
  - Security Misconfiguration: Secure defaults, no debug mode in production
  - Insecure Deserialization: Input validation
  - Using Components with Known Vulnerabilities: Regular dependency updates
  - Insufficient Logging: Comprehensive audit trails
  - API Security: Rate limiting, input validation

**NFR-SC-005: Audit Logging**

- **Priority:** High
- **Requirement:** System shall maintain comprehensive audit trails
- **Acceptance Criteria:**
  - All security events logged: Login attempts, permission changes, data modifications
  - Log fields: Timestamp, user ID, IP address, action, result
  - Logs stored immutably (append-only)
  - Log retention: 3 years minimum
  - Regular log review and monitoring
  - Sensitive data not logged (passwords, tokens)

**NFR-SC-006: API Security**

- **Priority:** High
- **Requirement:** APIs shall be protected against abuse
- **Acceptance Criteria:**
  - Rate limiting: 100 requests/minute per user, 1000/minute per IP
  - Input validation: All inputs validated against schema
  - Output encoding: Prevent injection attacks
  - API versioning: /api/v1/ prefix
  - CORS policy: Whitelist approved domains only
  - API documentation: OpenAPI 3.0 specification

#### 3.2.3 Usability Requirements

**NFR-US-001: User Interface**

- **Priority:** High
- **Requirement:** System shall provide intuitive and consistent UI
- **Acceptance Criteria:**
  - Material Design guidelines followed
  - Consistent navigation across all pages
  - Maximum 3 clicks to reach any feature
  - Clear labeling and instructions
  - Contextual help available
  - Responsive design (mobile, tablet, desktop)

**NFR-US-002: Accessibility**

- **Priority:** High
- **Requirement:** System shall comply with WCAG 2.1 Level AA
- **Acceptance Criteria:**
  - Keyboard navigation fully supported
  - Screen reader compatible
  - Color contrast ratio ≥ 4.5:1
  - Form labels and error messages clear
  - Alt text for all images
  - Focus indicators visible
  - No flashing content

**NFR-US-003: Learnability**

- **Priority:** Medium
- **Requirement:** New users shall be able to complete basic tasks within 15 minutes
- **Acceptance Criteria:**
  - First-time user onboarding wizard
  - Tooltips for complex features
  - Video tutorials embedded
  - Comprehensive user manual
  - In-app help documentation
  - Error messages with actionable guidance

**NFR-US-004: Error Handling**

- **Priority:** High
- **Requirement:** System shall display user-friendly error messages
- **Acceptance Criteria:**
  - No technical jargon in user-facing errors
  - Clear indication of what went wrong
  - Actionable steps to resolve issue
  - Error messages with unique codes for support
  - Validation errors shown in context (form fields)
  - Graceful handling of network errors

#### 3.2.4 Reliability Requirements

**NFR-RL-001: Availability**

- **Priority:** High
- **Requirement:** System shall maintain 99.5% uptime
- **Measurement:** Uptime measured monthly, excluding planned maintenance
- **Acceptance Criteria:**
  - Maximum unplanned downtime: 3.65 hours/month
  - Planned maintenance: Off-peak hours only (announced 48 hours prior)
  - Health check endpoint: /api/health
  - Automatic restart on failure
  - Load balancer health checks every 30 seconds

**NFR-RL-002: Fault Tolerance**

- **Priority:** High
- **Requirement:** System shall gracefully handle component failures
- **Acceptance Criteria:**
  - Database connection failures: Retry with exponential backoff
  - Email service failure: Queue for retry (max 3 attempts)
  - File storage failure: Fallback to local storage
  - Redis cache failure: Fall back to database
  - No cascading failures

**NFR-RL-003: Data Backup**

- **Priority:** Critical
- **Requirement:** System shall maintain regular data backups
- **Acceptance Criteria:**
  - Daily automated backups at 2:00 AM
  - Incremental backups every 6 hours
  - Backup retention: 30 days rolling
  - Backup verification: Weekly restore test
  - Offsite backup storage
  - Recovery Point Objective (RPO): 6 hours
  - Recovery Time Objective (RTO): 4 hours

**NFR-RL-004: Error Recovery**

- **Priority:** Medium
- **Requirement:** System shall recover from errors without data loss
- **Acceptance Criteria:**
  - Transaction rollback on database errors
  - Certificate generation failure: Retry mechanism
  - Email sending failure: Queue for retry
  - Incomplete operations logged for manual review
  - State consistency maintained

#### 3.2.5 Maintainability Requirements

**NFR-MT-001: Code Quality**

- **Priority:** High
- **Requirement:** Codebase shall follow industry standards and best practices
- **Acceptance Criteria:**
  - Python: PEP 8 compliance checked by flake8
  - JavaScript: ESLint with Airbnb style guide
  - Code complexity: Cyclomatic complexity ≤ 10
  - Code duplication: ≤ 5%
  - Code review required for all changes
  - Meaningful variable and function names
  - **Profile creation workflow validation:** 95% coverage
  - **Club member management logic:** 85% coverage
  - **Mentor-mentee assignment:** 90% coverage

**NFR-MT-002: Testing Coverage**

- **Priority:** High
- **Requirement:** System shall maintain high test coverage
- **Acceptance Criteria:**
  - Unit test coverage: ≥ 80%
  - Integration test coverage: ≥ 60%
  - E2E test coverage: Critical user flows
  - Test execution time: ≤ 10 minutes
  - All tests pass before deployment
  - Regression test suite maintained

**NFR-MT-003: Documentation**

- **Priority:** High
- **Requirement:** System shall be comprehensively documented
- **Acceptance Criteria:**
  - API documentation: OpenAPI 3.0 specification
  - Code documentation: Docstrings for all public functions/classes
  - Database schema documentation: ER diagrams, table descriptions
  - User manual: Role-specific guides with screenshots
  - Administrator manual: Installation, configuration, troubleshooting
  - README files in all code repositories

**NFR-MT-004: Modularity**

- **Priority:** Medium
- **Requirement:** System shall be designed with modular architecture
- **Acceptance Criteria:**
  - Django apps for each major module
  - React components reusable and composable
  - Clear separation of concerns (MVC pattern)
  - Loose coupling between modules
  - Plugin architecture for future extensions
  - Configuration externalized (environment variables)

**NFR-MT-005: Logging**

- **Priority:** High
- **Requirement:** System shall implement comprehensive logging
- **Acceptance Criteria:**
  - Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
  - Structured logging (JSON format)
  - Log rotation: Daily, max 100MB per file
  - Application logs, access logs, error logs separate
  - Correlation IDs for request tracing
  - Log aggregation with centralized logging system (ELK stack compatible)

#### 3.2.6 Portability Requirements

**NFR-PT-001: Platform Independence**

- **Priority:** Medium
- **Requirement:** System shall run on multiple operating systems
- **Acceptance Criteria:**
  - Supported OS: Linux (Ubuntu, CentOS), Windows Server, macOS
  - Containerized deployment with Docker
  - Docker Compose for development environment
  - Kubernetes-ready for production orchestration
  - Environment-specific configuration via .env files

**NFR-PT-002: Database Portability**

- **Priority:** Low
- **Requirement:** System shall support PostgreSQL 15 and above
- **Acceptance Criteria:**
  - ORM used for database abstraction (Django ORM)
  - No raw SQL queries (or minimal with comments)
  - Database migrations managed by Django
  - Migration rollback supported
  - Database agnostic code where possible

**NFR-PT-003: Browser Compatibility**

- **Priority:** High
- **Requirement:** System shall work on all modern browsers
- **Acceptance Criteria:**
  - Supported browsers: Chrome 110+, Firefox 110+, Safari 15+, Edge 110+
  - Responsive design: Mobile (320px+), Tablet (768px+), Desktop (1024px+)
  - Progressive enhancement approach
  - Polyfills for older browser features
  - Cross-browser testing in CI/CD pipeline

#### 3.2.7 Compliance Requirements

**NFR-CP-001: Data Privacy**

- **Priority:** Critical
- **Requirement:** System shall comply with data protection regulations
- **Acceptance Criteria:**
  - GDPR compliance for EU users (if applicable)
  - Data retention policies enforced
  - User consent for data processing
  - Right to data export (JSON format)
  - Right to be forgotten (account deletion with data anonymization)
  - Privacy policy accessible and clear

**NFR-CP-002: AICTE Compliance**

- **Priority:** High
- **Requirement:** System shall adhere to AICTE activity point guidelines
- **Acceptance Criteria:**
  - Point categories match AICTE specifications
  - Point allocation rules configurable
  - Audit trail for compliance verification
  - Reports in AICTE-specified format
  - Documentation for AICTE inspection

**NFR-CP-003: Accessibility Standards**

- **Priority:** High
- **Requirement:** System shall meet accessibility standards
- **Acceptance Criteria:**
  - WCAG 2.1 Level AA compliance
  - Accessibility audit passed
  - Screen reader testing completed
  - Keyboard navigation verified
  - Accessibility statement published

### 3.3 External Interface Requirements

#### 3.3.1 User Interfaces

**UI-001: Web Application Interface**

- Responsive single-page application (SPA)
- Material-UI component library
- Color scheme: Institutional branding colors
- Typography: Roboto font family
- Navigation: Top navigation bar with role-based menu items
- Dashboard: Role-specific landing page with key metrics and quick actions

**UI-002: Forms and Input**

- Form validation: Real-time with inline error messages
- Required fields: Red asterisk indicator
- Date pickers: Calendar widget
- Time pickers: 12-hour format with AM/PM
- File uploads: Drag-and-drop with progress bar
- Auto-save: Draft events and templates

**UI-003: Data Display**

- Tables: Sortable columns, pagination (25 rows per page), search/filter
- Charts: Interactive charts using Chart.js/Recharts
- Lists: Infinite scroll for long lists
- Cards: Event cards with thumbnails and key information
- Modals: Confirmations and detailed views

#### 3.3.2 API Interfaces

**API-001: REST API Specification**

- Base URL: https://{domain}/api/v1/
- Protocol: HTTPS only
- Format: JSON request/response
- Authentication: JWT Bearer token in Authorization header
- Versioning: URL path versioning (/api/v1/, /api/v2/)
- Status codes: Standard HTTP codes (200, 201, 400, 401, 403, 404, 500)

**API-002: Request/Response Format**

- Request headers: Content-Type: application/json, Authorization: Bearer {token}
- Response format:
  ```json
  {
    "success": true,
    "data": {...},
    "message": "Operation successful",
    "timestamp": "2025-11-16T10:30:00Z"
  }
  ```
- Error response:
  ```json
  {
    "success": false,
    "error": {
      "code": "ERR_001",
      "message": "User-friendly error message",
      "details": {...}
    },
    "timestamp": "2025-11-16T10:30:00Z"
  }
  ```

**API-003: Pagination**

- Query parameters: ?page=1&page_size=25
- Response includes:
  ```json
  {
    "data": [...],
    "pagination": {
      "page": 1,
      "page_size": 25,
      "total_pages": 10,
      "total_count": 250
    }
  }
  ```

**API-004: Filtering and Sorting**

- Filter: ?status=active&department=CSE
- Sort: ?sort_by=created_at&order=desc
- Search: ?search=query

#### 3.3.3 Hardware Interfaces

**HW-001: Server Requirements**

- Minimum: 4 CPU cores, 8GB RAM, 100GB SSD
- Recommended: 8 CPU cores, 16GB RAM, 500GB SSD
- Network: 1 Gbps connection
- Backup storage: Network-attached storage or cloud storage

**HW-002: Client Requirements**

- Desktop/Laptop: Any modern computer with browser
- Mobile/Tablet: iOS 13+ or Android 8+
- Screen resolution: Minimum 1366×768
- Network: Broadband connection (minimum 2 Mbps)

#### 3.3.4 Software Interfaces

**SW-001: Database Interface**

- Database: PostgreSQL 15+
- Connection: SQLAlchemy/Django ORM
- Connection pooling: Max 100 connections
- Migrations: Django migration framework

**SW-002: Email Interface**

- Protocol: SMTP or AWS SES API
- Authentication: Username/password or API key
- TLS: Required
- Delivery tracking: Webhook for delivery status

**SW-003: Storage Interface**

- Local filesystem: /media/certificates/, /media/templates/
- Cloud storage: S3-compatible API (AWS S3, MinIO)
- File permissions: Restricted to application user
- CDN: CloudFront or CloudFlare for certificate delivery

**SW-004: Cache Interface**

- Cache: Redis 7.x
- Connection: redis-py client
- Data structure: Key-value store
- TTL: Configurable per cache key
- Eviction policy: LRU (Least Recently Used)

#### 3.3.5 Communication Interfaces

**CM-001: HTTP/HTTPS**

- Protocol: HTTPS (TLS 1.3)
- Port: 443
- Certificate: Valid SSL/TLS certificate
- Redirects: HTTP to HTTPS automatic redirect

**CM-002: WebSocket** (Optional for real-time notifications)

- Protocol: WSS (WebSocket Secure)
- Library: Django Channels
- Use case: Real-time in-app notifications
- Fallback: Long polling

**CM-003: Email Protocols**

- Outbound: SMTP over TLS (port 587)
- Inbound: IMAP (for bounce handling, optional)

---

## 4. System Models

### 4.1 Use Case Diagrams

#### 4.1.1 Student Use Cases

**Actors:** Student

**Use Cases:**

1. Register for Event
2. View Registered Events
3. Download Certificate
4. View AICTE Points
5. Update Profile
6. Receive Notifications

#### 4.1.2 Club Organizer Use Cases

**Actors:** Club Organizer

**Use Cases:**

1. Create Event
2. Edit Event Details
3. Schedule Event
4. Book Hall
5. Upload Certificate Template
6. Mark Attendance
7. Complete Event
8. Generate Certificates
9. View Event Reports

#### 4.1.3 Mentor Use Cases

**Actors:** Mentor

**Use Cases:**

1. View Mentee Activities
2. Approve AICTE Points
3. Reject AICTE Points
4. Override Point Allocation
5. Generate Mentee Reports
6. Review Certificates

#### 4.1.4 Administrator Use Cases

**Actors:** System Administrator

**Use Cases:**

1. Manage Users
2. Assign Roles
3. Configure AICTE Categories
4. Approve Hall Bookings
5. Resolve Conflicts
6. View Audit Logs
7. Generate System Reports
8. Manage Halls/Venues

### 4.2 Sequence Diagrams

#### 4.2.1 Event Registration Flow

1. Student browses events
2. Student clicks "Register"
3. System checks eligibility and capacity
4. System creates registration record
5. System sends confirmation email
6. Student receives confirmation

#### 4.2.2 Event Completion and Certificate Generation Flow

1. Organizer marks attendance
2. Organizer clicks "Complete Event"
3. System validates attendance data
4. System generates certificates (bulk)
5. System allocates AICTE points (pending)
6. System sends certificates via email
7. System notifies students and mentor

#### 4.2.3 Point Approval Workflow

1. System allocates points (pending status)
2. System notifies mentor
3. Mentor reviews point allocation
4. Mentor approves/rejects
5. System updates point ledger
6. System notifies student

### 4.3 State Diagrams

#### 4.3.1 Event State Diagram

**States:**

- Draft: Initial state, event being created
- Scheduled: Event confirmed with hall booking
- Ongoing: Event started by organizer
- Completed: Event ended with attendance marked
- Cancelled: Event cancelled with reason

**Transitions:**

- Draft → Scheduled: Organizer confirms (requires hall booking)
- Scheduled → Ongoing: Organizer starts event
- Scheduled → Cancelled: Organizer/Admin cancels
- Ongoing → Completed: Organizer completes with attendance
- Ongoing → Cancelled: Emergency cancellation

#### 4.3.2 AICTE Point Transaction State Diagram

**States:**

- Pending: Points allocated, awaiting mentor approval
- Approved: Mentor approved, points credited
- Rejected: Mentor rejected, points not credited
- Overridden: Mentor manually adjusted points

**Transitions:**

- System creates → Pending
- Pending → Approved: Mentor approves
- Pending → Rejected: Mentor rejects
- Approved → Overridden: Mentor adjusts

#### 4.3.3 Hall Booking State Diagram

**States:**

- Pending: Booking requested, awaiting approval
- Approved: Booking confirmed
- Rejected: Booking denied
- Cancelled: Booking cancelled by organizer
- Completed: Event occurred

**Transitions:**

- Organizer creates → Pending
- Pending → Approved: Admin approves
- Pending → Rejected: Admin rejects
- Approved → Cancelled: Organizer cancels
- Approved → Completed: Event date passed

### 4.4 Data Flow Diagrams

#### 4.4.1 Level 0 DFD (Context Diagram)

**External Entities:**

- Students
- Mentors
- Club Organizers
- Administrators
- Email System
- Database

**Data Flows:**

- User credentials → System → Authentication token
- Event data → System → Event created
- Attendance data → System → Certificates generated
- Point allocation → System → Mentor notification
- Approval decision → System → Updated ledger

---

## 5. Appendices

### 5.1 Appendix A: Risk Analysis

| Risk ID | Risk Description                    | Probability | Impact   | Mitigation Strategy                                            |
| ------- | ----------------------------------- | ----------- | -------- | -------------------------------------------------------------- |
| R-001   | Database server failure             | Low         | Critical | Daily backups, database replication, RTO 4 hours               |
| R-002   | Email service outage                | Medium      | High     | Queue emails for retry, use backup SMTP provider               |
| R-003   | Security breach / data leak         | Low         | Critical | Regular security audits, penetration testing, encryption       |
| R-004   | Peak load during event registration | High        | Medium   | Load testing, auto-scaling, queue management                   |
| R-005   | Certificate generation failure      | Medium      | High     | Retry mechanism, manual regeneration option                    |
| R-006   | Hall booking conflicts              | Medium      | Medium   | Real-time validation, admin override capability                |
| R-007   | Network connectivity issues         | Medium      | Medium   | Offline capability for critical features, graceful degradation |
| R-008   | Third-party dependency failures     | Medium      | Medium   | Fallback mechanisms, vendor SLA monitoring                     |
| R-009   | User adoption resistance            | Medium      | High     | Training programs, user feedback, phased rollout               |
| R-010   | Data migration from legacy systems  | Low         | High     | Comprehensive migration plan, data validation, rollback plan   |

### 5.2 Appendix B: Glossary

| Term                 | Definition                                                                              |
| -------------------- | --------------------------------------------------------------------------------------- |
| Activity Points      | Credits awarded for participation in extracurricular activities as per AICTE guidelines |
| Audit Trail          | Chronological record of system activities enabling reconstruction and review            |
| Certificate Template | Reusable design layout for generating event certificates                                |
| Club Organizer       | Student or faculty managing club activities and events                                  |
| Double-Booking       | Situation where the same venue is reserved for overlapping time slots                   |
| Event Lifecycle      | Series of states an event passes through from creation to completion                    |
| Hall Booking         | Reservation of institutional venue for specific date and time                           |
| Mentor               | Faculty member assigned to guide and approve student activities                         |
| Point Ledger         | Record of all AICTE point transactions for a student                                    |
| QR Code              | Machine-readable code embedded in certificates for verification                         |
| USN                  | University Seat Number - unique identifier for students                                 |

### 5.3 Appendix C: Future Enhancements Roadmap

#### Phase 2 (6-12 months post-launch)

- Mobile native applications (iOS and Android)
- Advanced analytics dashboard with predictive insights
- QR code-based attendance marking via mobile app
- Integration with biometric attendance systems
- Gamification of student engagement
- AI-powered event recommendations

#### Phase 3 (12-24 months post-launch)

- Third-party LMS/ERP integration (Moodle, SAP, Oracle)
- Multi-campus deployment with centralized management
- Blockchain-based certificate verification
- Virtual event support (Zoom/Teams integration)
- Resource management (equipment, volunteers)
- Budget tracking and financial reporting

#### Phase 4 (24+ months post-launch)

- AI chatbot for student queries
- Machine learning for event success prediction
- Advanced fraud detection for certificate verification
- Integration with national AICTE portal
- White-label solution for multiple institutions
- Mobile SDKs for third-party integrations

### 5.4 Appendix D: Assumptions Log

1. Institution provides server infrastructure or cloud budget
2. AICTE point allocation schema remains stable
3. Student USNs are unique and permanent throughout academic tenure
4. Users have basic computer literacy and internet access
5. Institutional email system is reliable and monitored
6. Hall/venue information is accurate and up-to-date
7. Certificate templates follow standardized A4 format
8. Faculty workload permits mentor validation within 7 days
9. Academic calendar is provided for semester planning
10. Legal approval obtained for digital certificates vs. physical

### 5.5 Appendix E: Success Metrics

**System Performance Metrics:**

- API response time: ≤ 500ms (95th percentile)
- System uptime: ≥ 99.5%
- Certificate generation: ≤ 3 seconds per certificate
- Peak concurrent users: 500 without degradation

**Business Metrics:**

- Administrative time reduction: 70%
- Event registration time: ≤ 2 minutes
- Certificate delivery: Within 10 minutes of event completion
- Point approval turnaround: ≤ 7 days
- User satisfaction: ≥ 4.0/5.0

**Adoption Metrics:**

- Active users: ≥ 80% of student body within 3 months
- Events managed: 100% through platform within 6 months
- Hall booking digital rate: ≥ 95% within 3 months
- Certificate downloads: ≥ 90% within 24 hours of issuance

### 5.6 Appendix F: Developer Notes

- Remove template upload endpoints
- Remove template association tables
- Always load global template
- Maintain backward compatibilit

---

## Document Approval

| Role                       | Name | Signature | Date |
| -------------------------- | ---- | --------- | ---- |
| Project Manager            |      |           |      |
| Lead Developer             |      |           |      |
| QA Lead                    |      |           |      |
| System Architect           |      |           |      |
| Stakeholder Representative |      |           |      |

---

**End of Document**

_Version 2.1 - November 21, 2025_
