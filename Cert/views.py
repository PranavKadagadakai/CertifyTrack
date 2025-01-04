from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import re
from Cert.models import Profile, Event, CertificateTemplate, Club, Certificate, Participant
import csv
from django.http import HttpResponse
from Cert.forms import ClubCreationForm, EventForm, ProfileEditForm, ParticipantUploadForm
from django.core.mail import send_mail
from django.conf import settings
from .certificate_generator import generate_certificates

""" 
Base Link Views
"""
 
def home(request):
    if not request.user.is_authenticated:
        return redirect('landingpage')

    try:
        role = request.user.profile.role
        if role == 'student':
            return redirect('student_dashboard')
        elif role == 'club':
            return redirect('club_dashboard')
        elif role == 'mentor':
            return redirect('mentor_dashboard')
    except Profile.DoesNotExist:
        messages.error(request, "Profile not configured. Contact admin.")
    
    return redirect('landingpage')

def landingpage(request):
    """
    Redirects unauthenticated users to the login page by default and allows access to the signup page.
    Authenticated users are redirected to their respective dashboards.
    """
    if request.user.is_authenticated:
        # Redirect to the respective dashboard based on role
        role = getattr(request.user.profile, 'role', None)
        if role == 'student':
            return redirect('student_dashboard')
        elif role == 'club':
            return redirect('club_dashboard')
        elif role == 'mentor':
            return redirect('mentor_dashboard')
        else:
            messages.error(request, "Your account is not properly configured. Please contact support.")
            return redirect('home')

    # Render landing page if the user is not authenticated
    return render(request, 'landingpage.html')

@login_required
def profile(request):
    """
    Display the user's profile details.
    """
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        # Extract data from the submitted form
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Here you could use the send_mail function to send the contact form data
        send_mail(
            f"Contact Form Message from {name}",
            f"Message: {message}\nFrom: {name}, Email: {email}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],  # This should be your contact email address
            fail_silently=False,
        )

        # Return a success message (you can customize this)
        return HttpResponse('Thank you for contacting us. We will get back to you soon.')

    return render(request, 'contact.html')

@login_required
def edit_profile(request):
    profile = request.user.profile  # Get the profile associated with the logged-in user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)  # No need to pass 'role' here
        if form.is_valid():
            form.save()  # Save the form data to the profile model
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')  # Redirect to the profile page after saving changes
        else:
            messages.error(request, "There were errors in the form.")
    else:
        form = ProfileEditForm(instance=profile)  # Pass the profile instance to the form

    return render(request, 'edit_profile.html', {'form': form})


"""
Authentication Views
"""

def custom_logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to 'home' or another appropriate page


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
            # Ensure the user has a profile
            Profile.objects.get_or_create(user=user)

            login(request, user)
            # Redirect to appropriate dashboard based on role
            role = getattr(user.profile, 'role', None)
            if role == 'student':
                return redirect('student_dashboard')
            elif role == 'club':
                return redirect('club_dashboard')
            elif role == 'mentor':
                return redirect('mentor_dashboard')
        else:
            messages.error(request, "Invalid credentials.")
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
        profile, created = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()
        
        if role == 'club':
            # Create a Club instance for the user
            Club.objects.create(admin=user, name=f"{username}'s Club")

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')

"""
Role Specific Views
"""

# 1. Club Role's Views

@login_required
def club_dashboard(request):
    try:
        club = Club.objects.get(admin=request.user)
    except Club.DoesNotExist:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    # Retrieve events for the club (assuming you have a ForeignKey to Club in the Event model)
    events = Event.objects.filter(club=club)
    
    return render(request, 'club_dashboard.html', {'club': club, 'events': events})

@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            if 'certificate_template' in request.FILES:
                event.certificate_template = request.FILES['certificate_template'].read()
            event.save()
            return redirect('club_dashboard')  # Replace 'event_list' with your desired redirect URL
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

@login_required
def upload_certificate_template(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the user is authorized to upload a template
    if event.club.admin != request.user:
        messages.error(request, "You are not authorized to upload a certificate template for this event.")
        return redirect('club_dashboard')

    if request.method == 'POST' and request.FILES.get('template'):
        template_file = request.FILES['template']
        
        # Validate file format
        if not template_file.name.endswith(('.pdf', '.png', '.jpg')):
            messages.error(request, "The template must be in PDF, PNG, or JPG format.")
            return redirect('upload_certificate_template', event_id=event.id)

        # Create or update the template
        template, created = CertificateTemplate.objects.get_or_create(event=event)
        template.template_file = template_file
        template.save()

        # Link the template to the event
        event.template = template
        event.save()

        messages.success(request, "Certificate template uploaded successfully.")
        return redirect('club_dashboard')

    return render(request, 'upload_certificate_template.html', {'event': event})

@login_required
def update_event_status(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.club.admin != request.user:
        messages.error(request, "You are not authorized to update this event.")
        return redirect('club_dashboard')

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status == 'finished' and not event.certificate_template:
            messages.error(request, "Upload a certificate template before marking the event as finished.")
            return redirect('upload_certificate_template', event_id=event.id)

        event.status = new_status
        event.save()
        messages.success(request, f"Event status updated to {new_status}.")
        return redirect('club_dashboard')

    return render(request, 'update_event_status.html', {'event': event})

@login_required
def upload_participants(request, event_id):
    if request.user.profile.role != 'club':
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    event = Event.objects.get(id=event_id, club__admin=request.user)

    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "File is not a CSV.")
            return redirect('club_dashboard')

        try:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = csv.reader(decoded_file.splitlines())
            for row in io_string:
                usn = row[0]
                try:
                    student_profile = Profile.objects.get(user__username=usn, role='student')
                    event.participants.add(student_profile)
                except Profile.DoesNotExist:
                    messages.warning(request, f"USN {usn} not found. Skipping.")
            event.save()
            messages.success(request, "Participants uploaded successfully.")
        except Exception as e:
            messages.error(request, "Error processing the file.")
        return redirect('club_dashboard')

    return render(request, 'upload_participants.html', {'event': event})

@login_required
def generate_event_certificates(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure only clubs can generate certificates
    if request.user.profile.role != 'club':
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    # Check if a certificate template exists for the event
    if not event.certificate_template:
        messages.error(request, "Please upload a certificate template before generating certificates.")
        return redirect('upload_certificate_template', event_id=event_id)

    # Get all participants for the event
    participants = Participant.objects.filter(event=event)

    if not participants.exists():
        messages.error(request, "No participants found for this event.")
        return redirect('club_dashboard')

    # Generate certificates for each participant
    for participant in participants:
        try:
            # Generate certificate logic (replace with actual implementation)
            certificate_content = f"Certificate for {participant.student.username} in event {event.name}"

            # Save certificate to the database
            Certificate.objects.create(
                event=event,
                participant=participant,
                generated_file=certificate_content.encode()  # Placeholder binary content
            )
        except Exception as e:
            messages.error(request, f"Error generating certificate for {participant.student.username}: {str(e)}")
            continue

    # Mark the event as finished
    event.status = 'finished'
    event.save()

    messages.success(request, "Certificates generated successfully.")
    return redirect('club_dashboard')


@login_required
def update_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


# 1. Student Role's Views

@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

@login_required
def view_events(request):
    events = Event.objects.filter(status='not_started')
    return render(request, 'view_events.html', {'events': events})

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    student_profile = request.user.profile

    # Ensure only students can register for events
    if student_profile.role != 'student':
        messages.error(request, "Only students can register for events.")
        return redirect('home')

    # Check if the event is open for registration
    if event.status != 'not_started':
        messages.error(request, "This event is not open for registration.")
        return redirect('view_events')

    # Check participant limit
    participant_count = Participant.objects.filter(event=event).count()
    if participant_count >= event.participant_limit:
        messages.error(request, "This event has reached its participant limit.")
        return redirect('view_events')

    # Check if the student is already registered
    if Participant.objects.filter(event=event, student=request.user).exists():
        messages.error(request, "You are already registered for this event.")
        return redirect('view_events')

    # Register the student as a participant
    Participant.objects.create(event=event, student=request.user)

    # Update AICTE points
    student_profile.aicte_points += event.aicte_points
    student_profile.save()

    messages.success(request, "You have successfully registered for the event.")
    return redirect('view_events')

@login_required
def view_aicte_points_and_certificates(request):
    profile = Profile.objects.get(user=request.user)
    certificates = Certificate.objects.filter(owner=profile)

    return render(request, 'view_aicte_points_and_certificates.html', {
        'profile': profile,
        'certificates': certificates
    })
    
@login_required
def event_history(request):
    """
    Displays the event participation history for the logged-in student.
    """
    if request.user.profile.role != 'student':
        messages.error(request, "Only students can access their event history.")
        return redirect('home')

    # Get events the student has participated in
    participated_events = Participant.objects.filter(student=request.user).select_related('event')

    return render(request, 'event_history.html', {
        'participated_events': participated_events,
    })

# 1. Mentor Role's Views

@login_required
def mentor_dashboard(request):
    if request.user.profile.role != 'mentor':
        return HttpResponseForbidden("Access denied.")
    students = Profile.objects.filter(role='student')
    return render(request, 'mentor_dashboard.html', {'students': students})

@login_required
def verify_certificate(request, certificate_id):
    try:
        certificate = Certificate.objects.get(id=certificate_id)
        return render(request, 'verify_certificate.html', {'certificate': certificate})
    except Certificate.DoesNotExist:
        messages.error(request, "Certificate not found.")
        return redirect('mentor_dashboard')
    
@login_required
def mentor_students(request):
    """
    View the list of students assigned to the logged-in mentor.
    """
    if request.user.profile.role != 'mentor':
        messages.error(request, "Only mentors can access this page.")
        return redirect('home')

    # Get the students assigned to this mentor
    assigned_students = Profile.objects.filter(role='student', mentor=request.user)

    return render(request, 'mentor_students.html', {
        'students': assigned_students,
    })
    
    
"""
To be decided
"""

@login_required
def register_club(request):
    if request.method == 'POST':
        form = ClubCreationForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.admin = request.user  # Link current user as the admin
            club.save()
            # Update the user's profile role to 'club'
            profile = Profile.objects.get(user=request.user)
            profile.role = 'club'
            profile.save()
            return redirect('club_dashboard')  # Redirect to club dashboard
    else:
        form = ClubCreationForm()
    return render(request, 'register_club.html', {'form': form})