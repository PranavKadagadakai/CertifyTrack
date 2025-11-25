"""
Email sending utilities for CertifyTrack.
Handles verification emails and password reset OTP delivery.
Uses plain HTML strings (no Django templates needed).
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.timezone import now, timedelta
import uuid
import secrets
import string


def send_notification_email(user, subject, html_content, plain_content):
    """
    Send a notification email to a user based on their preferences.

    Args:
        user: User instance
        subject: Email subject
        html_content: HTML email content
        plain_content: Plain text email content
    """
    try:
        send_mail(
            subject,
            plain_content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_content,
            fail_silently=False,
        )
        print(f"[Notification Email] Sent to {user.email}: {subject}")
        return True
    except Exception as e:
        print(f"[Notification Email] Failed to send to {user.email}: {str(e)}")
        return False


def get_verification_email_html(user_name, verification_url, token, frontend_url):
    """Generate HTML for verification email."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .button:hover {{ background: #764ba2; }}
            .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
            .token-box {{ background: #e3f2fd; padding: 15px; border-left: 4px solid #667eea; margin: 15px 0; word-break: break-all; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CertifyTrack</h1>
                <p>Verify Your Email</p>
            </div>
            
            <div class="content">
                <p>Hi {user_name},</p>
                
                <p>Thank you for registering with CertifyTrack! Please verify your email address to complete your registration.</p>
                
                <p><strong>Click the button below to verify your email:</strong></p>
                
                <center>
                    <a href="{verification_url}" class="button">Verify Email</a>
                </center>
                
                <p>Or copy and paste this link in your browser:</p>
                <div class="token-box">
                    {verification_url}
                </div>
                
                <p><small><strong>If the button doesn't work:</strong> Copy and paste the link above into your browser address bar.</small></p>
                
                <p>If you didn't create this account, you can safely ignore this email.</p>
                
                <p>Best regards,<br>The CertifyTrack Team</p>
            </div>
            
            <div class="footer">
                <p>&copy; 2025 CertifyTrack. All rights reserved.</p>
                <p>Contact: support@certifytrack.com</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_verification_email_text(user_name, verification_url):
    """Generate plain text for verification email."""
    return f"""
Hi {user_name},

Thank you for registering with CertifyTrack! Please verify your email address to complete your registration.

Click this link to verify your email:
{verification_url}

If the link doesn't work, copy and paste it into your browser address bar.

If you didn't create this account, you can safely ignore this email.

Best regards,
The CertifyTrack Team
    """.strip()


def send_verification_email(user):
    """
    Send email verification link to user.
    
    Args:
        user: User instance with email_verification_token set
    """
    if not user.email_verification_token:
        raise ValueError("User must have email_verification_token set")
    
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={user.email_verification_token}"
    user_name = user.get_full_name() or user.username
    
    subject = "Verify Your CertifyTrack Email"
    html_message = get_verification_email_html(user_name, verification_url, user.email_verification_token, settings.FRONTEND_URL)
    plain_message = get_verification_email_text(user_name, verification_url)
    print(f"[Email Verification] Sent verification email to {user.email} with token: {user.email_verification_token}")
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def get_password_reset_email_html(user_name, otp, otp_minutes, frontend_url):
    """Generate HTML for password reset email."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
            .otp-box {{ background: #fff3cd; padding: 20px; border: 2px solid #ffc107; border-radius: 5px; text-align: center; margin: 20px 0; }}
            .otp-code {{ font-family: monospace; font-size: 32px; font-weight: bold; color: #f5576c; letter-spacing: 5px; }}
            .warning {{ background: #f8d7da; padding: 10px; border-left: 4px solid #f5576c; margin: 15px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CertifyTrack</h1>
                <p>Password Reset Request</p>
            </div>
            
            <div class="content">
                <p>Hi {user_name},</p>
                
                <p>We received a request to reset your password. Use the code below to reset your password:</p>
                
                <div class="otp-box">
                    <p><strong>Your Reset Code:</strong></p>
                    <p class="otp-code">{otp}</p>
                    <p><small>Valid for {otp_minutes} minutes</small></p>
                </div>
                
                <p><strong>How to reset your password:</strong></p>
                <ol>
                    <li>Go to {frontend_url}/forgot-password</li>
                    <li>Enter this code: <code>{otp}</code></li>
                    <li>Create your new password</li>
                    <li>Confirm and save</li>
                </ol>
                
                <div class="warning">
                    <p><strong>⚠️ Security Warning:</strong></p>
                    <p>If you didn't request a password reset, please ignore this email. Your account is still secure.</p>
                </div>
                
                <p><strong>This code will expire in {otp_minutes} minutes.</strong></p>
                
                <p>Never share this code with anyone. CertifyTrack staff will never ask for it.</p>
                
                <p>Best regards,<br>The CertifyTrack Team</p>
            </div>
            
            <div class="footer">
                <p>&copy; 2025 CertifyTrack. All rights reserved.</p>
                <p>Contact: support@certifytrack.com</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_password_reset_email_text(user_name, otp, otp_minutes):
    """Generate plain text for password reset email."""
    return f"""
Hi {user_name},

We received a request to reset your password. Use the code below to reset your password:

RESET CODE: {otp}
Valid for {otp_minutes} minutes

How to reset your password:
1. Go to the forgot-password page
2. Enter this code: {otp}
3. Create your new password
4. Confirm and save

⚠️ Security Warning:
If you didn't request a password reset, please ignore this email. Your account is still secure.

This code will expire in {otp_minutes} minutes.

Never share this code with anyone. CertifyTrack staff will never ask for it.

Best regards,
The CertifyTrack Team
    """.strip()


def send_password_reset_email(user, otp):
    """
    Send password reset OTP to user.
    
    Args:
        user: User instance
        otp: 6-digit OTP string
    """
    user_name = user.get_full_name() or user.username
    
    subject = "Password Reset Code - CertifyTrack"
    html_message = get_password_reset_email_html(user_name, otp, settings.PASSWORD_RESET_TIMEOUT_MINUTES, settings.FRONTEND_URL)
    plain_message = get_password_reset_email_text(user_name, otp, settings.PASSWORD_RESET_TIMEOUT_MINUTES)
    print(f"[Password Reset] Sent password reset email to {user.email} with OTP: {otp}")
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def get_account_locked_email_html(user_name, frontend_url):
    """Generate HTML for account locked email."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .button:hover {{ background: #764ba2; }}
            .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CertifyTrack</h1>
                <p>Account Locked</p>
            </div>
            
            <div class="content">
                <p>Hi {user_name},</p>
                
                <p>We detected multiple failed login attempts on your CertifyTrack account. Your account has been temporarily locked for security reasons.</p>
                
                <p><strong>What this means:</strong></p>
                <ul>
                    <li>Your account is temporarily locked for 30 minutes</li>
                    <li>You cannot log in during this time</li>
                    <li>We're protecting your account from unauthorized access</li>
                </ul>
                
                <p><strong>What you can do:</strong></p>
                <ul>
                    <li>Wait 30 minutes and try logging in again</li>
                    <li>Reset your password if you forgot it</li>
                    <li>Contact support if you need help</li>
                </ul>
                
                <center>
                    <a href="{frontend_url}/forgot-password" class="button">Reset Password</a>
                </center>
                
                <p>If you didn't attempt to log in to your account, please reset your password immediately.</p>
                
                <p>Best regards,<br>The CertifyTrack Team</p>
            </div>
            
            <div class="footer">
                <p>&copy; 2025 CertifyTrack. All rights reserved.</p>
                <p>Contact: support@certifytrack.com</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_account_locked_email_text(user_name):
    """Generate plain text for account locked email."""
    return f"""
Hi {user_name},

We detected multiple failed login attempts on your CertifyTrack account. Your account has been temporarily locked for security reasons.

What this means:
- Your account is temporarily locked for 30 minutes
- You cannot log in during this time
- We're protecting your account from unauthorized access

What you can do:
- Wait 30 minutes and try logging in again
- Reset your password if you forgot it
- Contact support if you need help

If you didn't attempt to log in to your account, please reset your password immediately.

Best regards,
The CertifyTrack Team
    """.strip()


def send_account_locked_email(user):
    """
    Send account locked warning to user.
    
    Args:
        user: User instance
    """
    user_name = user.get_full_name() or user.username
    
    subject = "Account Locked - CertifyTrack"
    html_message = get_account_locked_email_html(user_name, settings.FRONTEND_URL)
    plain_message = get_account_locked_email_text(user_name)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def get_welcome_email_html(user_name, user_type, frontend_url):
    """Generate HTML for welcome email."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .button {{ display: inline-block; background: #11998e; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .button:hover {{ background: #38ef7d; }}
            .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CertifyTrack</h1>
                <p>Welcome!</p>
            </div>
            
            <div class="content">
                <p>Hi {user_name},</p>
                
                <p>Welcome to CertifyTrack! Your account has been successfully created as a <strong>{user_type}</strong>.</p>
                
                <p>You can now:</p>
                <ul>
                    <li>Log in to your account</li>
                    <li>Complete your profile</li>
                    <li>Start exploring the platform</li>
                </ul>
                
                <center>
                    <a href="{frontend_url}/login" class="button">Go to Login</a>
                </center>
                
                <p>If you have any questions, don't hesitate to contact our support team.</p>
                
                <p>Best regards,<br>The CertifyTrack Team</p>
            </div>
            
            <div class="footer">
                <p>&copy; 2025 CertifyTrack. All rights reserved.</p>
                <p>Contact: support@certifytrack.com</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_welcome_email_text(user_name, user_type):
    """Generate plain text for welcome email."""
    return f"""
Hi {user_name},

Welcome to CertifyTrack! Your account has been successfully created as a {user_type}.

You can now:
- Log in to your account
- Complete your profile
- Start exploring the platform

If you have any questions, don't hesitate to contact our support team.

Best regards,
The CertifyTrack Team
    """.strip()


def send_welcome_email(user):
    """
    Send welcome email after successful registration and verification.

    Args:
        user: User instance
    """
    user_name = user.get_full_name() or user.username
    user_type = user.get_user_type_display()

    subject = "Welcome to CertifyTrack!"
    html_message = get_welcome_email_html(user_name, user_type, settings.FRONTEND_URL)
    plain_message = get_welcome_email_text(user_name, user_type)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


# ============================================================================
# EVENT NOTIFICATION EMAILS
# ============================================================================

def get_event_registration_email_html(user_name, event_name, event_date, event_time, club_name, frontend_url):
    """Generate HTML for event registration confirmation."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #43a047 0%, #66bb6a 100%); color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .event-details {{ background: #e8f5e8; padding: 15px; border-left: 4px solid #43a047; margin: 15px 0; }}
            .button {{ display: inline-block; background: #43a047; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .button:hover {{ background: #66bb6a; }}
            .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CertifyTrack</h1>
                <p>Event Registration Confirmed</p>
            </div>

            <div class="content">
                <p>Hi {user_name},</p>

                <p>Great news! Your registration for the event has been confirmed.</p>

                <div class="event-details">
                    <h3>Event Details:</h3>
                    <p><strong>Event:</strong> {event_name}</p>
                    <p><strong>Club:</strong> {club_name}</p>
                    <p><strong>Date:</strong> {event_date}</p>
                    <p><strong>Time:</strong> {event_time}</p>
                </div>

                <p><strong>What happens next:</strong></p>
                <ul>
                    <li>You will receive a reminder 24 hours before the event</li>
                    <li>Check your dashboard for event updates</li>
                    <li>Mark your calendar for this important date!</li>
                </ul>

                <center>
                    <a href="{frontend_url}/dashboard" class="button">View in Dashboard</a>
                </center>

                <p>Best regards,<br>The CertifyTrack Team</p>
            </div>

            <div class="footer">
                <p>&copy; 2025 CertifyTrack. All rights reserved.</p>
                <p>Contact: support@certifytrack.com</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_event_registration_email_text(user_name, event_name, event_date, event_time, club_name):
    """Generate plain text for event registration confirmation."""
    return f"""
Hi {user_name},

Great news! Your registration for the event has been confirmed.

Event Details:
- Event: {event_name}
- Club: {club_name}
- Date: {event_date}
- Time: {event_time}

What happens next:
- You will receive a reminder 24 hours before the event
- Check your dashboard for event updates
- Mark your calendar for this important date!

Best regards,
The CertifyTrack Team
    """.strip()


def send_event_registration_email(user, event):
    """Send event registration confirmation email."""
    user_name = user.get_full_name() or user.username
    event_name = event.name
    event_date = event.event_date.strftime('%A, %B %d, %Y')
    event_time = event.start_time.strftime('%I:%M %p')
    club_name = event.club.name

    subject = f"Event Registration Confirmed - {event_name}"
    html_message = get_event_registration_email_html(user_name, event_name, event_date, event_time, club_name, settings.FRONTEND_URL)
    plain_message = get_event_registration_email_text(user_name, event_name, event_date, event_time, club_name)

    return send_notification_email(user, subject, html_message, plain_message)


def get_event_cancellation_email_html(user_name, event_name, event_date, club_name, reason, frontend_url):
    """Generate HTML for event cancellation notification."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%); color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .cancellation-box {{ background: #ffebee; border: 2px solid #f44336; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0; }}
            .urgent {{ color: #d32f2f; font-weight: bold; font-size: 18px; }}
            .event-details {{ background: #fce4ec; padding: 15px; border-left: 4px solid #f44336; margin: 15px 0; }}
            .reason-box {{ background: #f8f8f8; padding: 15px; border: 1px solid #ddd; margin: 15px 0; }}
            .button {{ display: inline-block; background: #f44336; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .button:hover {{ background: #d32f2f; }}
            .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CertifyTrack</h1>
                <p>Event Cancellation Notice</p>
            </div>

            <div class="content">
                <p>Hi {user_name},</p>

                <p>We regret to inform you that an event you were registered for has been cancelled.</p>

                <div class="cancellation-box">
                    <p class="urgent">❌ EVENT CANCELLED</p>
                </div>

                <div class="event-details">
                    <h3>Event Details:</h3>
                    <p><strong>Event:</strong> {event_name}</p>
                    <p><strong>Club:</strong> {club_name}</p>
                    <p><strong>Scheduled Date:</strong> {event_date}</p>
                </div>

                {f'<div class="reason-box"><h4>Cancellation Reason:</h4><p>{reason}</p></div>' if reason else ''}

                <p><strong>What this means:</strong></p>
                <ul>
                    <li>The event will not take place as scheduled</li>
                    <li>Your registration has been automatically cancelled</li>
                    <li>You will not receive AICTE points for this event</li>
                    <li>No further action is required from you</li>
                </ul>

                <center>
                    <a href="{frontend_url}/events" class="button">Browse Other Events</a>
                </center>

                <p>We apologize for any inconvenience this may cause. Stay tuned for other exciting events from our clubs!</p>

                <p>Best regards,<br>The CertifyTrack Team</p>
            </div>

            <div class="footer">
                <p>&copy; 2025 CertifyTrack. All rights reserved.</p>
                <p>Contact: support@certifytrack.com</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_event_cancellation_email_text(user_name, event_name, event_date, club_name, reason):
    """Generate plain text for event cancellation notification."""
    return f"""
Hi {user_name},

We regret to inform you that an event you were registered for has been cancelled.

❌ EVENT CANCELLED

Event Details:
- Event: {event_name}
- Club: {club_name}
- Scheduled Date: {event_date}

{f'Cancellation Reason: {reason}' if reason else ''}

What this means:
- The event will not take place as scheduled
- Your registration has been automatically cancelled
- You will not receive AICTE points for this event
- No further action is required from you

We apologize for any inconvenience this may cause. Stay tuned for other exciting events from our clubs!

Best regards,
The CertifyTrack Team
    """.strip()


def send_event_cancellation_email(user, event, reason=None):
    """Send event cancellation notification email."""
    user_name = user.get_full_name() or user.username
    event_name = event.name
    event_date = event.event_date.strftime('%A, %B %d, %Y')
    club_name = event.club.name

    subject = f"Event Cancelled - {event_name}"
    html_message = get_event_cancellation_email_html(user_name, event_name, event_date, club_name, reason, settings.FRONTEND_URL)
    plain_message = get_event_cancellation_email_text(user_name, event_name, event_date, club_name, reason)

    return send_notification_email(user, subject, html_message, plain_message)


def get_certificate_generation_email_html(user_name, event_name, certificate_url, frontend_url):
    """Generate HTML for certificate generation notification."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .certificate-box {{ background: #e3f2fd; border: 2px solid #2196f3; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0; }}
            .celebration {{ color: #1976d2; font-weight: bold; font-size: 20px; }}
            .certificate-details {{ background: #bbdefb; padding: 15px; border-left: 4px solid #2196f3; margin: 15px 0; }}
            .button {{ display: inline-block; background: #2196f3; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
            .button:hover {{ background: #1976d2; }}
            .download-button {{ background: #4caf50; }}
            .download-button:hover {{ background: #388e3c; }}
            .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CertifyTrack</h1>
                <p>Certificate Generated</p>
            </div>

            <div class="content">
                <p>Hi {user_name},</p>

                <p>🎉 Congratulations! Your certificate has been generated and is now available for download.</p>

                <div class="certificate-box">
                    <p class="celebration">🏆 CERTIFICATE READY!</p>
                    <p>You have successfully participated in:</p>
                    <h3>{event_name}</h3>
                </div>

                <div class="certificate-details">
                    <h4>What you accomplished:</h4>
                    <ul>
                        <li>✓ Successfully attended the event</li>
                        <li>✓ Contributed to club activities</li>
                        <li>✓ Earned AICTE activity points</li>
                        <li>✓ Received official recognition</li>
                    </ul>
                </div>

                <p><strong>Download your certificate:</strong></p>

                <center>
                    <a href="{certificate_url}" class="button download-button">Download Certificate</a>
                    <br><br>
                    <a href="{frontend_url}/certificates" class="button">View All Certificates</a>
                </center>

                <p>Your certificate includes:</p>
                <ul>
                    <li>Official event verification</li>
                    <li>QR code for authenticity checking</li>
                    <li>Institutional endorsement</li>
                    <li>AICTE point attribution</li>
                </ul>

                <p>Keep this certificate for your academic records and future reference!</p>

                <p>Best regards,<br>The CertifyTrack Team</p>
            </div>

            <div class="footer">
                <p>&copy; 2025 CertifyTrack. All rights reserved.</p>
                <p>Contact: support@certifytrack.com</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_certificate_generation_email_text(user_name, event_name, certificate_url):
    """Generate plain text for certificate generation notification."""
    return f"""
Hi {user_name},

🎉 Congratulations! Your certificate has been generated and is now available for download.

🏆 CERTIFICATE READY!
You have successfully participated in: {event_name}

What you accomplished:
✓ Successfully attended the event
✓ Contributed to club activities
✓ Earned AICTE activity points
✓ Received official recognition

Download your certificate: {certificate_url}

Your certificate includes:
- Official event verification
- QR code for authenticity checking
- Institutional endorsement
- AICTE point attribution

Keep this certificate for your academic records and future reference!

Best regards,
The CertifyTrack Team
    """.strip()


def send_certificate_generation_email(user, event, certificate_url):
    """Send certificate generation notification email."""
    user_name = user.get_full_name() or user.username
    event_name = event.name

    subject = f"Certificate Available - {event_name}"
    html_message = get_certificate_generation_email_html(user_name, event_name, certificate_url, settings.FRONTEND_URL)
    plain_message = get_certificate_generation_email_text(user_name, event_name, certificate_url)

    return send_notification_email(user, subject, html_message, plain_message)


def get_points_approval_email_html(user_name, event_name, points, status, reason, frontend_url):
    """Generate HTML for AICTE points approval/rejection notification."""
    status_color = "#4caf50" if status.lower() == "approved" else "#f44336"
    status_icon = "✅" if status.lower() == "approved" else "❌"
    status_title = "Points Approved" if status.lower() == "approved" else "Points Rejected"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, {status_color} 0%, {"#388e3c" if status_color == "#4caf50" else "#d32f2f"} 100%); color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .points-box {{ background: {"#e8f5e8" if status_color == "#4caf50" else "#ffebee"}; border: 2px solid {status_color}; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0; }}
            .status-icon {{ font-size: 24px; }}
            .points-details {{ background: {"#f1f8e9" if status_color == "#4caf50" else "#ffcdd2"}; padding: 15px; border-left: 4px solid {status_color}; margin: 15px 0; }}
            .button {{ display: inline-block; background: {status_color}; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .button:hover {{ background: {"#388e3c" if status_color == "#4caf50" else "#d32f2f"}; }}
            .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CertifyTrack</h1>
                <p>AICTE Points Decision</p>
            </div>

            <div class="content">
                <p>Hi {user_name},</p>

                <p>Decision has been made on your AICTE activity points.</p>

                <div class="points-box">
                    <p class="status-icon">{status_icon}</p>
                    <h2>{status_title}</h2>
                    <p><strong>Event:</strong> {event_name}</p>
                    <p><strong>Points:</strong> {points}</p>
                </div>

                <div class="points-details">
                    <h4>Decision Details:</h4>
                    <p><strong>Status:</strong> {status}</p>
                    <p><strong>Points Awarded:</strong> {points if status.lower() == "approved" else "0"}</p>
                    {f'<p><strong>Reason:</strong> {reason}</p>' if reason else ''}
                </div>

                <p><strong>What this means:</strong></p>
                {"<ul><li>✅ Points have been added to your account</li><li>🎯 Keep earning more activity points!</li><li>📈 Check your progress in the dashboard</li></ul>" if status.lower() == "approved" else "<ul><li>❌ Points were not approved for this activity</li><li>💡 Contact your mentor for clarification</li><li>🎯 Keep participating in eligible activities</li></ul>"}

                <center>
                    <a href="{frontend_url}/points" class="button">View Points Dashboard</a>
                </center>

                <p>Best regards,<br>The CertifyTrack Team</p>
            </div>

            <div class="footer">
                <p>&copy; 2025 CertifyTrack. All rights reserved.</p>
                <p>Contact: support@certifytrack.com</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_points_approval_email_text(user_name, event_name, points, status, reason):
    """Generate plain text for AICTE points approval/rejection notification."""
    status_emoji = "✅" if status.lower() == "approved" else "❌"

    return f"""
Hi {user_name},

Decision has been made on your AICTE activity points.

{status_emoji} {status.upper()}

Event: {event_name}
Points: {points}

Decision Details:
- Status: {status}
- Points Awarded: {points if status.lower() == "approved" else "0"}
{f'- Reason: {reason}' if reason else ''}

{{What this means:
✅ Points have been added to your account
🎯 Keep earning more activity points!
📈 Check your progress in the dashboard" if status.lower() == "approved" else "What this means:
❌ Points were not approved for this activity
💡 Contact your mentor for clarification
🎯 Keep participating in eligible activities"}}

Best regards,
The CertifyTrack Team
    """.strip()


def send_points_decision_email(user, event, points, status, reason=None):
    """Send AICTE points approval/rejection notification email."""
    user_name = user.get_full_name() or user.username
    event_name = event.name

    subject = f"AICTE Points {status.title()} - {event_name}"
    html_message = get_points_approval_email_html(user_name, event_name, points, status, reason, settings.FRONTEND_URL)
    plain_message = get_points_approval_email_text(user_name, event_name, points, status, reason)

    return send_notification_email(user, subject, html_message, plain_message)


def get_hall_booking_decision_email_html(user_name, hall_name, event_name, booking_date, start_time, status, reason, frontend_url):
    """Generate HTML for hall booking approval/rejection notification."""
    status_color = "#4caf50" if status.lower() == "approved" else "#f44336"
    status_icon = "✅" if status.lower() == "approved" else "❌"
    status_title = "Booking Approved" if status.lower() == "approved" else "Booking Rejected"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, {status_color} 0%, {"#388e3c" if status_color == "#4caf50" else "#d32f2f"} 100%); color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .booking-box {{ background: {"#e8f5e8" if status_color == "#4caf50" else "#ffebee"}; border: 2px solid {status_color}; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0; }}
            .status-icon {{ font-size: 24px; }}
            .booking-details {{ background: {"#f1f8e9" if status_color == "#4caf50" else "#ffcdd2"}; padding: 15px; border-left: 4px solid {status_color}; margin: 15px 0; }}
            .button {{ display: inline-block; background: {status_color}; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .button:hover {{ background: {"#388e3c" if status_color == "#4caf50" else "#d32f2f"}; }}
            .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CertifyTrack</h1>
                <p>Hall Booking Decision</p>
            </div>

            <div class="content">
                <p>Hi {user_name},</p>

                <p>Decision has been made on your hall booking request.</p>

                <div class="booking-box">
                    <p class="status-icon">{status_icon}</p>
                    <h2>{status_title}</h2>
                    <p><strong>Hall:</strong> {hall_name}</p>
                    <p><strong>Event:</strong> {event_name}</p>
                </div>

                <div class="booking-details">
                    <h4>Booking Details:</h4>
                    <p><strong>Date:</strong> {booking_date}</p>
                    <p><strong>Time:</strong> {start_time}</p>
                    <p><strong>Status:</strong> {status}</p>
                    {f'<p><strong>Reason:</strong> {reason}</p>' if reason else ''}
                </div>

                <p><strong>What this means:</strong></p>
                {"<ul><li>✅ Your booking has been confirmed</li><li>🏛️ Hall has been reserved for your event</li><li>📅 You can now proceed with event scheduling</li></ul>" if status.lower() == "approved" else "<ul><li>❌ Booking request has been denied</li><li>🏛️ Hall is not available for the requested time</li><li>🔄 Try booking a different hall or time slot</li></ul>"}

                <center>
                    <a href="{frontend_url}/bookings" class="button">View All Bookings</a>
                </center>

                <p>Best regards,<br>The CertifyTrack Team</p>
            </div>

            <div class="footer">
                <p>&copy; 2025 CertifyTrack. All rights reserved.</p>
                <p>Contact: support@certifytrack.com</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_hall_booking_decision_email_text(user_name, hall_name, event_name, booking_date, start_time, status, reason):
    """Generate plain text for hall booking approval/rejection notification."""
    status_emoji = "✅" if status.lower() == "approved" else "❌"

    return f"""
Hi {user_name},

Decision has been made on your hall booking request.

{status_emoji} {status.upper()}

Booking Details:
- Hall: {hall_name}
- Event: {event_name}
- Date: {booking_date}
- Time: {start_time}
- Status: {status}
{f'- Reason: {reason}' if reason else ''}

{{What this means:
✅ Your booking has been confirmed
🏛️ Hall has been reserved for your event
📅 You can now proceed with event scheduling" if status.lower() == "approved" else "What this means:
❌ Booking request has been denied
🏛️ Hall is not available for the requested time
🔄 Try booking a different hall or time slot"}}

Best regards,
The CertifyTrack Team
    """.strip()


def send_hall_booking_decision_email(user, booking, decision, reason=None):
    """Send hall booking approval/rejection notification email."""
    user_name = user.get_full_name() or user.username
    hall_name = booking.hall.name
    event_name = booking.event.name
    booking_date = booking.booking_date.strftime('%A, %B %d, %Y')
    start_time = booking.start_time.strftime('%I:%M %p')

    subject = f"Hall Booking {decision.title()} - {hall_name}"
    html_message = get_hall_booking_decision_email_html(user_name, hall_name, event_name, booking_date, start_time, decision, reason, settings.FRONTEND_URL)
    plain_message = get_hall_booking_decision_email_text(user_name, hall_name, event_name, booking_date, start_time, decision, reason)

    return send_notification_email(user, subject, html_message, plain_message)


def get_event_reminder_email_html(user_name, event_name, event_date, event_time, club_name, venue, frontend_url):
    """Generate HTML for event reminder."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #ff9800 0%, #ff5722 100%); color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .reminder-box {{ background: #fff3cd; border: 2px solid #ff9800; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0; }}
            .urgent {{ color: #ff5722; font-weight: bold; font-size: 18px; }}
            .event-details {{ background: #e8f5e8; padding: 15px; border-left: 4px solid #ff9800; margin: 15px 0; }}
            .button {{ display: inline-block; background: #ff9800; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .button:hover {{ background: #ff5722; }}
            .footer {{ background: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>CertifyTrack</h1>
                <p>Event Reminder</p>
            </div>

            <div class="content">
                <p>Hi {user_name},</p>

                <p>This is a friendly reminder about your upcoming event.</p>

                <div class="reminder-box">
                    <p class="urgent">📅 DON'T FORGET!</p>
                    <p>Your event starts in less than 24 hours</p>
                </div>

                <div class="event-details">
                    <h3>Event Details:</h3>
                    <p><strong>Event:</strong> {event_name}</p>
                    <p><strong>Club:</strong> {club_name}</p>
                    <p><strong>Date:</strong> {event_date}</p>
                    <p><strong>Time:</strong> {event_time}</p>
                    <p><strong>Venue:</strong> {venue or 'TBD'}</p>
                </div>

                <p><strong>Important Reminders:</strong></p>
                <ul>
                    <li>Arrive 15 minutes early for check-in</li>
                    <li>Bring your student ID card</li>
                    <li>Come prepared and enthusiastic!</li>
                </ul>

                <center>
                    <a href="{frontend_url}/dashboard" class="button">View Event Details</a>
                </center>

                <p>Best regards,<br>The CertifyTrack Team</p>
            </div>

            <div class="footer">
                <p>&copy; 2025 CertifyTrack. All rights reserved.</p>
                <p>Contact: support@certifytrack.com</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_event_reminder_email_text(user_name, event_name, event_date, event_time, club_name, venue):
    """Generate plain text for event reminder."""
    return f"""
Hi {user_name},

This is a friendly reminder about your upcoming event.

📅 DON'T FORGET!
Your event starts in less than 24 hours

Event Details:
- Event: {event_name}
- Club: {club_name}
- Date: {event_date}
- Time: {event_time}
- Venue: {venue or 'TBD'}

Important Reminders:
- Arrive 15 minutes early for check-in
- Bring your student ID card
- Come prepared and enthusiastic!

Best regards,
The CertifyTrack Team
    """.strip()


def send_event_reminder_email(user, event):
    """Send event reminder email 24 hours before."""
    user_name = user.get_full_name() or user.username
    event_name = event.name
    event_date = event.event_date.strftime('%A, %B %d, %Y')
    event_time = event.start_time.strftime('%I:%M %p')
    club_name = event.club.name
    venue = event.assigned_hall.name if event.assigned_hall else None

    subject = f"Event Reminder - {event_name} Tomorrow"
    html_message = get_event_reminder_email_html(user_name, event_name, event_date, event_time, club_name, venue, settings.FRONTEND_URL)
    plain_message = get_event_reminder_email_text(user_name, event_name, event_date, event_time, club_name, venue)

    return send_notification_email(user, subject, html_message, plain_message)
