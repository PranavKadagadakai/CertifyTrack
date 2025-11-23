"""
Email sending utilities for CertifyTrack.
Handles verification emails and password reset OTP delivery.
Uses plain HTML strings (no Django templates needed).
"""

from django.core.mail import send_mail
from django.conf import settings


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
