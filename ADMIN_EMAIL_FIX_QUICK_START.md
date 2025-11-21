# 🔐 Admin Setup & Login Guide

## Quick Answer

**Is email verification required for admins?**
- ✅ **NO** - Admins can now login without email verification!
- Regular users (students, mentors, club organizers) must verify their email first

## What Changed

The LoginView was updated to skip email verification for admin users, while still requiring it for regular users.

**Before:** Admins created with `createsuperuser` couldn't login (403 Forbidden - "Please verify your email")
**After:** Admins can login immediately without email verification

## Setting Up Admin Accounts

### Option 1: Create Admin with Django Command (Recommended)

```bash
# Navigate to backend directory
cd BackEnd

# Create superuser with Django command
python manage.py createsuperuser
# Follow prompts for username and password
# Leave email blank or enter any value

# Set a proper email (optional but recommended)
python manage.py set_admin_email <username> <email>

# Example:
python manage.py set_admin_email admin1 admin@certifytrack.local
```

### Option 2: Quick Verification for All Admins

```bash
# Mark all admin accounts as email verified
python manage.py verify_all_admins

# Output:
# ✓ Successfully verified emails for X admin user(s)
# Admin users:
#   • admin1                  | admin@example.com    | ✓ Verified
```

### Option 3: Register as Admin via API (Development Only)

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin1",
    "email": "admin@example.com",
    "password": "securepass123",
    "user_type": "admin"
  }'
```

**Note:** This requires admin user to already exist or a public registration endpoint

## Management Commands Reference

### set_admin_email

Update email for an existing admin user.

```bash
python manage.py set_admin_email <username> <email>

# Example:
python manage.py set_admin_email admin1 admin@certifytrack.local

# Output:
# ✓ Successfully updated email for user "admin1"
#   Old email: (none)
#   New email: admin@certifytrack.local
#   Email verified: Yes
```

**Use cases:**
- Fix missing/wrong email on superuser
- Update admin email address
- Verify admin email without sending verification email

**Automatic actions:**
- Sets email address
- Marks email as verified
- Clears verification token

### verify_all_admins

Quickly verify all admin and superuser accounts.

```bash
python manage.py verify_all_admins

# Output:
# ✓ Successfully verified emails for 2 admin user(s)
# Admin users:
#   • admin1                  | admin@example.com    | ✓ Verified
#   • root                    | (no email)           | ✓ Verified
```

**Use cases:**
- Set up multiple admin accounts at once
- Quick verification without individual commands
- Check admin account status

## Login Flow for Different User Types

### Student/Mentor/Club Organizer
```
1. User enters username + password
2. System checks if email is verified
3. ❌ If NOT verified → "Please verify your email before logging in"
4. ✅ If verified → Login successful
```

### Admin User
```
1. Admin enters username + password
2. System checks credentials
3. ✅ Skip email verification check
4. ✅ Login successful (regardless of email verification status)
```

## Troubleshooting

### "Please verify your email" Error

**If you're a regular user:**
1. Check your email for verification link
2. Click the link to verify
3. Try logging in again

**If you're an admin:**
1. This should no longer happen
2. Try updating your code: `git pull origin main`
3. Restart backend: `python manage.py runserver`

### Can't Login as Admin

**Step 1: Verify admin account exists**
```bash
python manage.py shell
>>> from api.models import User
>>> User.objects.filter(is_superuser=True)
```

**Step 2: Set email (if needed)**
```bash
python manage.py set_admin_email <username> <email>
```

**Step 3: Mark as verified**
```bash
python manage.py verify_all_admins
```

**Step 4: Try login again**
- Navigate to http://localhost:3000/login
- Enter username and password
- Should login successfully now

## Environment Setup Summary

### Development Setup
```bash
# 1. Create Django superuser
python manage.py createsuperuser
# Input: username=admin, password=admin123

# 2. (Optional) Set email
python manage.py set_admin_email admin admin@local.dev

# 3. Verify admin accounts
python manage.py verify_all_admins

# 4. Start Django server
python manage.py runserver

# 5. Start React frontend
cd ../FrontEnd
npm run dev

# 6. Login at http://localhost:5173/login
# Username: admin
# Password: admin123
```

### Production Setup
```bash
# Same as development, but additionally:

# 1. Set proper email domain
python manage.py set_admin_email admin admin@yourdomain.com

# 2. Verify all admins
python manage.py verify_all_admins

# 3. Configure email backend in settings.py
# (SMTP, AWS SES, etc.)

# 4. Update environment variables for security
# EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_PASSWORD, etc.
```

## Security Notes

⚠️ **Important for Production:**

1. **Email Verification:**
   - Admins bypass email verification for convenience
   - BUT: Set a real email address for account recovery
   - Consider enabling 2FA in future

2. **Password Policy:**
   - Admins created with `createsuperuser` should use strong passwords
   - Minimum 12 characters recommended
   - Mix of letters, numbers, special characters

3. **Access Control:**
   - Keep admin credentials secure
   - Never commit credentials to git
   - Use environment variables for sensitive data

4. **Audit Logging:**
   - All admin actions are logged in AuditLog table
   - Monitor `/admin/reports/audit_logs/` regularly

## Admin Dashboard Access

Once logged in as admin:

```
1. Dashboard: http://localhost:5173/dashboard
   (Auto-redirects to AdminDashboard for admin users)

2. Admin features available:
   - 👥 User Management (create, disable, reset password)
   - 🎯 Club Management (create clubs, assign coordinators)
   - 🤝 Mentee Assignment (bulk assign students to mentors)
   - ⭐ AICTE Configuration (manage point categories)
   - 📈 Reports (system stats, audit logs, hall utilization)
```

## Related Documentation

- ADMIN_MODULE_GUIDE.md - Full admin feature documentation
- TESTING_DEPLOYMENT_GUIDE.md - Deployment instructions
- BackEnd/README.md - Backend setup guide

## Quick Commands Reference

```bash
# Create superuser
python manage.py createsuperuser

# Set admin email
python manage.py set_admin_email admin admin@example.com

# Verify all admins
python manage.py verify_all_admins

# Check user in Django shell
python manage.py shell
>>> from api.models import User
>>> user = User.objects.get(username='admin')
>>> user.is_email_verified
>>> user.user_type

# List all users
>>> User.objects.values('id', 'username', 'email', 'user_type', 'is_email_verified')
```

---

**Last Updated:** November 21, 2025
**Status:** ✅ Admin login fixed - No email verification required
