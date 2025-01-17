from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import re
from Cert.models import Profile, Event, CertificateTemplate, Club, Certificate, Participant
import csv
from django.http import HttpResponse, Http404, FileResponse
from Cert.forms import ClubCreationForm, EventForm, ProfileEditForm, ParticipantUploadForm, AssignStudentsForm, CertificateTemplateForm
from django.core.mail import send_mail
from django.conf import settings
# from .certificate_generator import generate_certificate
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile
import logging
import os
from django.conf import settings
import tempfile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfWriter, PdfReader

logger = logging.getLogger(__name__)


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
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()  # Save the form data to the profile model
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')  # Redirect to the profile page after saving changes
        else:
            messages.error(request, "There were errors in the form.")
    else:
        form = ProfileEditForm(instance=profile)

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
            event.club = request.user.admin_club  # Assign the event to the logged-in club's admin
            event.save()

            # Handle the uploaded certificate template
            if 'certificate_template' in request.FILES:
                certificate_template = CertificateTemplate.objects.create(
                    event=event,
                    template_file=request.FILES['certificate_template']
                )
                event.template = certificate_template
                event.save()

            messages.success(request, "Event created successfully!")
            return redirect('club_dashboard')
        else:
            messages.error(request, "There were errors in the form. Please fix them and try again.")
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})

@login_required
def upload_certificate_template(request, event_id):
    """
    Allows clubs to upload a certificate template for an event.
    """
    event = get_object_or_404(Event, id=event_id)

    # Ensure the user is a club admin
    if request.user.profile.role != 'club':
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    if request.method == 'POST':
        form = CertificateTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            if 'template_file' in request.FILES:
                # Create or update the certificate template
                template, created = CertificateTemplate.objects.get_or_create(event=event)
                template.template_file = request.FILES['template_file']
                template.save()

                messages.success(request, "Certificate template uploaded successfully.")
                return redirect('club_dashboard')
            else:
                messages.error(request, "Please upload a certificate template file.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = CertificateTemplateForm()

    return render(request, 'upload_certificate_template.html', {'form': form, 'event': event})

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

    # Ensure only club users can generate certificates
    if request.user.profile.role != 'club':
        messages.error(request, "Unauthorized access.")
        return redirect('home')

    # Check if the certificate template exists
    if not event.certificate_template or not event.certificate_template.template_file:
        messages.error(request, "Please upload a certificate template before generating certificates.")
        return redirect('upload_certificate_template', event_id=event_id)

    # Get template file and file type
    template_file = event.certificate_template.template_file
    file_type = template_file.name.split('.')[-1].lower()  # Extract file extension
    template_path = os.path.join(settings.MEDIA_ROOT, template_file.name)

    # Debugging: Check template path
    print(f"Template Path: {template_path}")

    # Read participants for the event
    participants = Participant.objects.filter(event=event)

    if not participants.exists():
        messages.error(request, "No participants found for this event.")
        return redirect('club_dashboard')

    # Create a temporary directory to store the generated certificates
    temp_dir = tempfile.mkdtemp()

    try:
        for participant in participants:
            try:
                # Debug: Ensure participant is an instance of Participant
                print(f"Processing participant: {participant} (ID: {participant.id})")

                # Get participant details
                student_profile = participant.student.profile  # Get the student's profile
                full_name = student_profile.full_name
                usn = student_profile.usn

                # Debug: Check participant details
                print(f"Participant Name: {full_name}, USN: {usn}")

                # Prepare paths for template and output
                output_path = os.path.join(temp_dir, f"certificate_{participant.id}.{file_type}")

                # Handle PDF templates
                if file_type == "pdf":
                    # Read the existing PDF template
                    with open(template_path, "rb") as pdf_file:
                        pdf_reader = PdfReader(pdf_file)
                        pdf_writer = PdfWriter()

                        # Go through each page of the PDF template
                        for page in pdf_reader.pages:
                            packet = BytesIO()
                            can = canvas.Canvas(packet, pagesize=letter)

                            # Add participant details on top of the existing template
                            can.setFont("Helvetica-Bold", 14)
                            can.drawString(200, 300, f"Name: {full_name}")
                            if usn:
                                can.drawString(200, 270, f"USN: {usn}")
                            can.save()

                            # Merge the new content with the existing page
                            packet.seek(0)
                            new_pdf = PdfReader(packet)
                            page.merge_page(new_pdf.pages[0])
                            pdf_writer.add_page(page)

                        # Write the final PDF to the output path
                        with open(output_path, "wb") as output_pdf:
                            pdf_writer.write(output_pdf)

                # Handle image templates
                elif file_type in ["png", "jpg", "jpeg"]:
                    with Image.open(template_path) as img:
                        draw = ImageDraw.Draw(img)
                        font = ImageFont.truetype("arial.ttf", 40)  # Ensure you have the font installed or update the path

                        # Positioning for text (adjust coordinates for your template)
                        draw.text((300, 200), full_name, font=font, fill="black")
                        if usn:
                            draw.text((300, 250), usn, font=font, fill="black")

                        img.save(output_path)  # Save the image to the output path

                else:
                    raise ValueError(f"Unsupported template file type: {file_type}")

                # Save the generated certificate to the database
                # Upload the generated certificate to the 'certificate_file' field
                with open(output_path, 'rb') as cert_file:
                    Certificate.objects.create(
                        event=event,
                        participant=participant,
                        certificate_file=f'generated_certificates/{participant.id}.{file_type}'
                    )
                    # Save the file to the media directory
                    certificate_media_path = os.path.join(
                        settings.MEDIA_ROOT, f'generated_certificates/{participant.id}.{file_type}'
                    )
                    with open(certificate_media_path, 'wb') as dest:
                        dest.write(cert_file.read())

            except Exception as e:
                # Debugging: Print error details
                print(f"Error generating certificate for {participant.student.username}: {str(e)}")
                messages.error(request, f"Error generating certificate for {participant.student.profile.full_name}: {str(e)}")
                continue

        # Mark the event as finished
        event.status = 'finished'
        event.save()

        messages.success(request, "Certificates generated successfully.")
    finally:
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                os.remove(file_path)
            os.rmdir(temp_dir)

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
    """
    Dashboard for students to view available events, AICTE points, and certificates.
    """
    if request.user.profile.role != 'student':
        messages.error(request, "Access denied.")
        return redirect('home')

    available_events = Event.objects.filter(status='not_started')
    profile = request.user.profile

    return render(request, 'student_dashboard.html', {
        'available_events': available_events,
        'profile': profile,
    })

@login_required
def view_events(request):
    """
    View all upcoming events.
    """
    events = Event.objects.filter(status='not_started')
    return render(request, 'view_events.html', {'events': events})

@login_required
def register_for_event(request, event_id):
    """
    Register the logged-in student for an event.
    """
    event = get_object_or_404(Event, id=event_id)
    student_profile = request.user.profile

    if student_profile.role != 'student':
        messages.error(request, "Only students can register for events.")
        return redirect('home')

    if event.status != 'not_started':
        messages.error(request, "This event is not open for registration.")
        return redirect('view_events')

    if Participant.objects.filter(event=event, student=request.user).exists():
        messages.error(request, "You are already registered for this event.")
        return redirect('view_events')

    if Participant.objects.filter(event=event).count() >= event.participant_limit:
        messages.error(request, "This event has reached its participant limit.")
        return redirect('view_events')

    Participant.objects.create(event=event, student=request.user)
    student_profile.aicte_points += event.aicte_points
    student_profile.save()

    messages.success(request, "Successfully registered for the event.")
    return redirect('view_events')

@login_required
def view_aicte_points_and_certificates(request):
    """
    Displays AICTE points and certificates for the logged-in student.
    """
    profile = request.user.profile
    if profile.role != 'student':
        messages.error(request, "Only students can view their AICTE points and certificates.")
        return redirect('home')

    certificates = Certificate.objects.filter(participant__student=request.user)
    return render(request, 'view_aicte_points_and_certificates.html', {
        'profile': profile,
        'certificates': certificates,
    })

@login_required
def event_history(request):
    """
    View the history of events the student has participated in.
    """
    if request.user.profile.role != 'student':
        messages.error(request, "Only students can view event history.")
        return redirect('home')

    participated_events = Participant.objects.filter(student=request.user).select_related('event')
    return render(request, 'event_history.html', {'participated_events': participated_events})

# 1. Mentor Role's Views

@login_required
def mentor_dashboard(request):
    """
    Dashboard for mentors to view their students and their certificates.
    """
    # Check if the logged-in user is a mentor
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'mentor':
        return HttpResponseForbidden("Access denied.")

    # Get the students assigned to the mentor (as Profiles)
    students = Profile.objects.filter(role='student', mentor=request.user)

    # Extract the User instances of these students
    student_users = students.values_list('user', flat=True)

    # Fetch certificates for these students
    certificates = Certificate.objects.filter(participant__student__in=student_users)

    return render(request, 'mentor_dashboard.html', {
        'students': students,
        'certificates': certificates,
    })

@login_required
def mentor_students(request):
    """
    View all students assigned to the logged-in mentor.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'mentor':
        return HttpResponseForbidden("Access denied.")
    
    students = Profile.objects.filter(mentor=request.user, role='student')
    
    return render(request, 'mentor_students.html', {'students': students})


@login_required
def verify_certificate(request, certificate_id):
    """
    Allows a mentor to verify a certificate.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'mentor':
        return HttpResponseForbidden("Access denied.")
    
    certificate = get_object_or_404(Certificate, id=certificate_id)
    if certificate.participant.student.profile.mentor != request.user:
        return HttpResponseForbidden("You do not have permission to verify this certificate.")
    
    certificate.verified = True
    certificate.save()
    return redirect('mentor_dashboard')

@login_required
def assign_students(request):
    """
    Allows a mentor to assign students to themselves or other mentors.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'mentor':
        return HttpResponseForbidden("Access denied.")
    
    if request.method == 'POST':
        form = AssignStudentsForm(request.POST)
        if form.is_valid():
            students = form.cleaned_data['students']
            mentor = form.cleaned_data['mentor']
            
            for student in students:
                student_profile = Profile.objects.get(user=student)
                student_profile.mentor = mentor
                student_profile.save()
            return redirect('mentor_dashboard')
    else:
        form = AssignStudentsForm()

    return render(request, 'assign_students.html', {'form': form})

@login_required
def assign_event(request):
    """
    Assigns an event to students.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'mentor':
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        students = request.POST.getlist('students')
        event_id = request.POST.get('event')
        event = get_object_or_404(Event, id=event_id)

        for student_id in students:
            student = get_object_or_404(User, id=student_id)
            participant, created = Participant.objects.get_or_create(student=student, event=event)

        return redirect('mentor_dashboard')

    students = Profile.objects.filter(role='student', mentor=request.user)
    events = Event.objects.all()

    return render(request, 'assign_event.html', {'students': students, 'events': events})

@login_required
def generate_certificate(request, event_id):
    """
    Generate a certificate for all participants in an event.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'mentor':
        return HttpResponseForbidden("Access denied.")

    event = get_object_or_404(Event, id=event_id)
    participants = Participant.objects.filter(event=event)

    for participant in participants:
        Certificate.objects.create(event=event, participant=participant)
    
    return redirect('mentor_dashboard')

@login_required
def mentor_view_student_certificates(request, student_id):
    """
    Display certificates for a specific student assigned to the mentor.
    """
    if request.user.profile.role != 'mentor':
        return HttpResponseForbidden("Access denied.")

    # Check if the student is assigned to the mentor
    student = get_object_or_404(Profile, user__id=student_id, role='student', mentor=request.user)

    # Fetch certificates for the selected student
    certificates = Certificate.objects.filter(participant__student=student.user).select_related('event', 'participant')

    return render(request, 'mentor_view_student_certificates.html', {
        'student': student,
        'certificates': certificates,
    })
    
"""
To be decided
"""

@login_required
def view_certificate(request, certificate_id):
    try:
        certificate = Certificate.objects.get(id=certificate_id)

        # Ensure the user is authorized to view the certificate
        if (
            request.user.profile.role == 'student' and certificate.participant.student != request.user or
            request.user.profile.role == 'mentor' and certificate.participant.student.profile.mentor != request.user
        ):
            return HttpResponse("Unauthorized", status=403)

        # Get the file path for the certificate
        certificate_path = certificate.certificate_file.path

        # Read the file from the file system
        with open(certificate_path, 'rb') as cert_file:
            file_data = cert_file.read()

        # Determine content type
        if file_data.startswith(b'%PDF'):
            content_type = 'application/pdf'
        elif file_data[:3] == b'\xff\xd8\xff':  # JPEG marker
            content_type = 'image/jpeg'
        elif file_data[:8] == b'\x89PNG\r\n\x1a\n':  # PNG marker
            content_type = 'image/png'
        else:
            raise Http404("Unsupported file format.")

        # Serve the file
        response = HttpResponse(file_data, content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="certificate_{certificate.id}.{content_type.split("/")[-1]}"'
        return response

    except Certificate.DoesNotExist:
        raise Http404("Certificate not found.")
    except FileNotFoundError:
        raise Http404("Certificate file not found.")

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