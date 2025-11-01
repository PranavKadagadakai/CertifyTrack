# api/views.py

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Club, Event, Participant, Certificate, CertificateTemplate
from .serializers import (
    UserSerializer, RegisterSerializer, EventSerializer, 
    CertificateSerializer, ParticipantSerializer, ProfileSerializer
)
from .permissions import IsClubAdmin, IsStudent, IsMentor
import os
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfWriter, PdfReader
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# --- RegisterView, LoginView (No Changes) ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# --- ProfileView (Updated to use ProfileSerializer for updates) ---
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def get_serializer_context(self):
        return {'request': self.request}

# --- EventViewSet (No Changes) ---
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'upload_template', 'generate_certificates']:
            self.permission_classes = [IsClubAdmin]
        elif self.action == 'register':
            self.permission_classes = [IsStudent]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        club = get_object_or_404(Club, admin=self.request.user)
        serializer.save(club=club)

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = self.get_object()
        student = request.user
        
        if event.status != 'not_started':
            return Response({'error': 'Event registration is closed.'}, status=status.HTTP_400_BAD_REQUEST)
        if event.participants.count() >= event.participant_limit:
            return Response({'error': 'Event is full.'}, status=status.HTTP_400_BAD_REQUEST)
        if Participant.objects.filter(event=event, student=student).exists():
            return Response({'error': 'Already registered.'}, status=status.HTTP_400_BAD_REQUEST)
        
        Participant.objects.create(event=event, student=student)
        student.profile.aicte_points += event.aicte_points
        student.profile.save()
        
        return Response({'status': 'Successfully registered.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='upload-template')
    def upload_template(self, request, pk=None):
        event = self.get_object()
        file = request.FILES.get('template_file')
        if not file:
            return Response({'error': 'Template file is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        template = CertificateTemplate.objects.create(template_file=file)
        
        event.template = template
        event.save()
        
        return Response(EventSerializer(event, context={'request': request}).data)

    @action(detail=True, methods=['post'], url_path='generate-certificates')
    def generate_certificates(self, request, pk=None):
        event = self.get_object()
        if not event.template:
            return Response({'error': 'Certificate template not found.'}, status=status.HTTP_400_BAD_REQUEST)

        participants = event.participants.all()
        if not participants:
            return Response({'error': 'No participants for this event.'}, status=status.HTTP_400_BAD_REQUEST)

        template_path = event.template.template_file.path
        file_ext = os.path.splitext(template_path)[1].lower()

        for participant in participants:
            student_profile = participant.student.profile
            full_name = student_profile.full_name or participant.student.username
            usn = student_profile.usn or 'N/A'
            
            output_buffer = BytesIO()

            try:
                if file_ext == '.pdf':
                    packet = BytesIO()
                    can = canvas.Canvas(packet, pagesize=letter)
                    can.drawString(200, 400, f"Name: {full_name}")
                    can.drawString(200, 380, f"USN: {usn}")
                    can.save()
                    packet.seek(0)
                    new_pdf = PdfReader(packet)
                    existing_pdf = PdfReader(open(template_path, "rb"))
                    output = PdfWriter()
                    page = existing_pdf.pages[0]
                    page.merge_page(new_pdf.pages[0])
                    output.add_page(page)
                    output.write(output_buffer)

                elif file_ext in ['.png', '.jpg', '.jpeg']:
                    img = Image.open(template_path)
                    draw = ImageDraw.Draw(img)
                    try:
                        font = ImageFont.truetype("arial.ttf", 40)
                    except IOError:
                        font = ImageFont.load_default()
                    draw.text((300, 200), full_name, font=font, fill="black")
                    if usn != 'N/A':
                        draw.text((300, 250), usn, font=font, fill="black")
                    img.save(output_buffer, format='PNG')
                else:
                    continue

                output_buffer.seek(0)
                file_name = f'cert_{event.id}_{participant.id}{file_ext}'
                
                cert, created = Certificate.objects.update_or_create(
                    event=event,
                    participant=participant,
                    defaults={'certificate_file': ContentFile(output_buffer.read(), name=file_name)}
                )

            except Exception as e:
                return Response({'error': f"Error generating certificate for {full_name}: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        event.status = 'finished'
        event.save()
        return Response({'status': 'Certificates generated successfully.'})


# --- CertificateViewSet (No Changes) ---
class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CertificateSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.profile.role == 'student':
            return Certificate.objects.filter(participant__student=user)
        elif user.profile.role == 'mentor':
            mentee_ids = Profile.objects.filter(mentor=user).values_list('user_id', flat=True)
            return Certificate.objects.filter(participant__student_id__in=mentee_ids)
        return Certificate.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[IsMentor])
    def verify(self, request, pk=None):
        certificate = self.get_object()
        if certificate.participant.student.profile.mentor != request.user:
            return Response({'error': 'Not authorized to verify this certificate.'}, status=status.HTTP_403_FORBIDDEN)
        
        certificate.verified = True
        certificate.save()
        return Response(CertificateSerializer(certificate, context={'request': self.request}).data)

# --- DashboardDataView (No Changes) ---
class DashboardDataView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.profile.role == 'student':
            registered_events = Event.objects.filter(participants__student=user)
            available_events = Event.objects.filter(status='not_started').exclude(id__in=registered_events.values_list('id', flat=True))
            return Response({
                'profile': UserSerializer(user).data,
                'registered_events': EventSerializer(registered_events, many=True, context={'request': request}).data,
                'available_events': EventSerializer(available_events, many=True, context={'request': request}).data
            })
        elif user.profile.role == 'club':
            club = get_object_or_404(Club, admin=user)
            events = Event.objects.filter(club=club)
            return Response({
                'club': {'name': club.name},
                'events': EventSerializer(events, many=True, context={'request': request}).data
            })
        elif user.profile.role == 'mentor':
            mentees = Profile.objects.filter(mentor=user)
            mentee_users = User.objects.filter(profile__in=mentees)
            return Response({
                'profile': UserSerializer(user).data,
                'mentees': UserSerializer(mentee_users, many=True).data
            })
        return Response({})

# +++ NEW: MentorViewSet +++
class MentorViewSet(viewsets.ViewSet):
    permission_classes = [IsMentor]

    def list(self, request):
        """ Lists the current mentor's mentees """
        mentees = Profile.objects.filter(mentor=request.user)
        mentee_users = User.objects.filter(profile__in=mentees)
        serializer = UserSerializer(mentee_users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='certificates')
    def mentee_certificates(self, request, pk=None):
        """ Lists certificates for a specific mentee of the current mentor """
        try:
            mentee_user = User.objects.get(pk=pk)
            if mentee_user.profile.mentor != request.user:
                return Response({'error': 'This student is not your mentee.'}, status=status.HTTP_403_FORBIDDEN)
            
            certificates = Certificate.objects.filter(participant__student=mentee_user)
            serializer = CertificateSerializer(certificates, many=True, context={'request': request})
            return Response({
                'mentee': UserSerializer(mentee_user).data,
                'certificates': serializer.data
            })

        except User.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

# --- Custom Token Obtainment (NEW) ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer