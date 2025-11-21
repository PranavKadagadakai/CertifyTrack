# 🚀 Admin Module Quick Start Guide

## Login as Admin

1. Create admin account (during setup or via management command)
2. Use credentials to login at `/login`
3. Access admin dashboard at `/dashboard` (auto-redirects if user_type='admin')

## Access Admin Features

### Dashboard Overview

**URL:** `http://localhost:5173/dashboard` (when logged in as admin)

Stats displayed:

- Total Users, Students, Mentors, Clubs
- User breakdown by role
- Total events, certificates, active bookings

### User Management Tab

**List Users:**

- Filter by type (Student, Mentor, Club Organizer, Admin)
- Filter by verification status
- Search by username or email

**Create User:**

1. Click "➕ Create User"
2. Fill form with required fields
3. Select user type
4. Fill role-specific fields:
   - Student: USN, Department, Semester
   - Mentor: Employee ID, Department, Designation
   - Club Organizer: Just basic info
5. Click "Create User"
   - Email auto-verified
   - Password set to provided value

**Manage Accounts:**

- Disable: Prevents login (reverts is_active to False)
- Enable: Allows login (sets is_active to True)
- Reset Password: Set new password for user
- Unlock: Removes account lock after failed attempts

### Club Management Tab

**Create Club:**

1. Click "➕ Create Club"
2. Enter club name and description
3. Select establishment date
4. Optionally select faculty coordinator
5. Click "Create Club"

**Manage Club:**

- Assign Faculty Coordinator: Select mentor from dropdown
- Assign Club Head: Select student from dropdown
- View member count
- Check club status (Active/Inactive)

### Mentee Assignment Tab

**View Assignments:**

- See all mentors with their assigned mentees count
- Expand to view individual student assignments
- Format: USN and Student Name

**Bulk Upload:**

1. Prepare CSV file with columns: mentor_id, student_usn
2. Click file upload input
3. Select CSV file
4. Click "Upload & Assign"
5. View results with error count

Example CSV:

```
mentor_id,student_usn
1,USN001
1,USN002
2,USN003
```

### AICTE Configuration Tab

**Create Category:**

1. Click "➕ Create Category"
2. Enter category name
3. Add description
4. Set min points (optional)
5. Set max points (optional)
6. Click "Save"

**Manage Categories:**

- Edit: Update category details
- Delete: Remove category (with confirmation)
- View: See all configured categories

### Reports Tab

**System Statistics:**

- Total users, students, mentors, clubs
- Events, certificates, bookings overview

**User Activity Report:**

- Verified vs unverified users
- Active vs inactive users
- Locked user count

**Event Statistics:**

- Total events
- Total registrations
- Attendance metrics

**Hall Utilization:**

- Hall usage per venue
- Total/Approved/Pending bookings
- Hall capacity

**Audit Logs:**

- View recent admin actions
- Filter by date range (7/30/90 days)
- Shows: Username, Timestamp, Action

## Common Tasks

### Add New Student

1. Go to User Management → Click "➕ Create User"
2. Fill: Username, Email, Password, First Name, Last Name
3. Select "Student" as type
4. Fill: USN, Department, Semester
5. Click "Create User"

### Add Mentor to Club

1. Go to Club Management
2. Find club in list
3. Click "Faculty Coordinator" dropdown
4. Select mentor name
5. Auto-saves assignment

### Bulk Assign Mentees

1. Go to Mentee Assignment
2. Prepare CSV: mentor_id, student_usn
3. Click file upload
4. Select CSV
5. Click "Upload & Assign"
6. Review results

### Reset User Password

1. Go to User Management
2. Find user in list
3. Click "Reset Password" button
4. Enter new password (8+ chars)
5. Click "Reset" in modal
6. Confirm success message

### Create AICTE Category

1. Go to AICTE Config
2. Click "➕ Create Category"
3. Name: "Hackathon Participation"
4. Description: "Participation in coding hackathons"
5. Min Points: 10
6. Max Points: 25
7. Click "Save"

### View System Audit Logs

1. Go to Reports
2. Scroll to "Audit Logs" section
3. See recent admin actions
4. Change date filter if needed (7/30/90 days)
5. View all admin operations

## API Usage Examples

### List Users

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/admin/users/?user_type=student"
```

### Create User

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newstudent",
    "email": "student@example.com",
    "password": "SecurePass123",
    "user_type": "student",
    "usn": "USN123",
    "department": "CSE",
    "semester": 3
  }' \
  http://localhost:8000/api/admin/users/create/
```

### Reset Password

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"new_password": "NewSecurePass123"}' \
  http://localhost:8000/api/admin/users/1/reset_password/
```

### Get System Stats

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/admin/reports/system_stats/
```

## Troubleshooting

### Can't access Admin Dashboard

- ✓ Verify user_type is 'admin'
- ✓ Check authentication token is valid
- ✓ Ensure admin routes are registered in App.jsx

### Create User Fails

- ✓ Check username is unique
- ✓ Check email is unique (if required)
- ✓ Verify required fields for user type are filled
- ✓ Check password is 8+ characters

### Bulk Upload Errors

- ✓ Verify CSV headers: mentor_id, student_usn
- ✓ Check mentor IDs exist in database
- ✓ Check student USNs exist in database
- ✓ Review error message for specific row

### Permission Denied Errors

- ✓ Verify user is admin type
- ✓ Check authorization token
- ✓ Ensure IsAdmin permission is applied

## Keyboard Shortcuts

- `Tab` - Navigate form fields
- `Enter` - Submit form or click focused button
- `Escape` - Close modals
- `Ctrl+F` - Search/find on page

## Tips & Tricks

1. **Bulk Operations:**

   - Use CSV uploads for large-scale assignments
   - Prepare data in Excel/Sheets, export as CSV

2. **User Filtering:**

   - Use search bar for quick user lookup
   - Filter by type to manage specific roles

3. **Audit Trail:**

   - Check audit logs before major changes
   - Verify admin actions are logged

4. **Error Recovery:**
   - Read error messages carefully
   - Check data format in forms
   - Review CSV format documentation

## Performance Tips

- Limit date ranges in audit logs (use 7 days for faster loading)
- Batch operations with CSV instead of individual creates
- Clear filters to load default views faster

## Security Reminders

✓ Always logout after admin session
✓ Don't share admin credentials
✓ Review audit logs regularly
✓ Use strong passwords for admin accounts
✓ Test changes in staging before production

## Need Help?

1. Check ADMIN_MODULE_GUIDE.md for detailed docs
2. Review browser console for error messages
3. Check backend logs: `python manage.py runserver --verbosity=3`
4. Verify API endpoints are registered: `python manage.py show_urls`

---

**Last Updated:** November 21, 2025
**Version:** 1.0
**Status:** Production Ready
