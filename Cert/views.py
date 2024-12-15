from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import re

# Create your views here.
def home(request):
    return render(request, 'landingpage.html')

def landingpage(request):
    return render(request, 'landingpage.html')

def profile(request):
    return render(request, 'profile.html')

def validate_email_domain(email, role):
    """
    Validate the email domain based on the role:
    - Students: "students.git.edu"
    - Others (Club and Mentor): "git.edu"
    """
    if role == 'student' and not email.endswith('@students.git.edu'):
        raise ValidationError("Students must use an email ending with '@students.git.edu'.")
    elif role in ['club', 'mentor'] and not email.endswith('@git.edu'):
        raise ValidationError("Clubs and Mentors must use an email ending with '@git.edu'.")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Check and redirect based on role
            try:
                role = user.profile.role
                if role == 'student':
                    messages.success(request, "Welcome, Student!")
                    return redirect('student_dashboard')
                elif role == 'club':
                    messages.success(request, "Welcome, Club Member!")
                    return redirect('club_dashboard')
                elif role == 'mentor':
                    messages.success(request, "Welcome, Mentor!")
                    return redirect('mentor_dashboard')
            except AttributeError:
                messages.error(request, "User role not defined. Please contact admin.")
                return redirect('login')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return render(request, 'login.html')

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')  # Role: student, club, or mentor

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # Validate email domain
        try:
            validate_email_domain(email, role)
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'signup.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'signup.html')

        # Create user and profile
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Assign role to profile
        profile = Profile.objects.get(user=user)
        profile.role = role
        profile.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')

@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

@login_required
def club_dashboard(request):
    return render(request, 'club_dashboard.html')

@login_required
def mentor_dashboard(request):
    return render(request, 'mentor_dashboard.html')
