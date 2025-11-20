# api/views.py

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import User, Student, Mentor, Club, Event, EventRegistration, Certificate, Hall, HallBooking, AICTECategory, AICTEPointTransaction, Notification, AuditLog
from .serializers import (
    UserSerializer, RegisterSerializer, EventSerializer, 
    CertificateSerializer, EventRegistrationSerializer, ClubSerializer, 
    HallSerializer, HallBookingSerializer, AICTECategorySerializer, AICTEPointTransactionSerializer,
    NotificationSerializer, AuditLogSerializer
)
from .permissions import IsClubAdmin, IsStudent, IsMentor
from django.utils.timezone import now

# --- RegisterView ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# --- ProfileView ---
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# --- ClubViewSet ---
class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(faculty_coordinator=self.request.user.mentor_profile)

# --- EventViewSet ---
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'generate_certificates']:
            self.permission_classes = [IsClubAdmin]
        elif self.action == 'register':
            self.permission_classes = [IsStudent]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        club = get_object_or_404(Club, club_head=self.request.user.student_profile)
        serializer.save(club=club)

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = self.get_object()
        student = request.user.student_profile

        if event.status != 'scheduled':
            return Response({'error': 'Event registration is closed.'}, status=status.HTTP_400_BAD_REQUEST)
        if event.eventregistration_set.count() >= event.max_participants:
            return Response({'error': 'Event is full.'}, status=status.HTTP_400_BAD_REQUEST)
        if EventRegistration.objects.filter(event=event, student=student).exists():
            return Response({'error': 'Already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        EventRegistration.objects.create(event=event, student=student)
        return Response({'status': 'Successfully registered.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='generate-certificates')
    def generate_certificates(self, request, pk=None):
        event = self.get_object()

        participants = event.eventregistration_set.all()
        if not participants:
            return Response({'error': 'No participants for this event.'}, status=status.HTTP_400_BAD_REQUEST)

        for participant in participants:
            student = participant.student
            certificate, created = Certificate.objects.get_or_create(
                event=event,
                student=student,
                defaults={
                    'file_path': f"certificates/{event.id}_{student.usn}.pdf",
                    'issue_date': now()
                }
            )

        event.status = 'completed'
        event.save()
        return Response({'status': 'Certificates generated successfully.'})

# --- HallViewSet ---
class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAuthenticated]

# --- HallBookingViewSet ---
class HallBookingViewSet(viewsets.ModelViewSet):
    queryset = HallBooking.objects.all()
    serializer_class = HallBookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(booked_by=self.request.user)

# --- CertificateViewSet ---
class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CertificateSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'student':
            return Certificate.objects.filter(student=user.student_profile)
        elif user.user_type == 'mentor':
            mentees = Student.objects.filter(mentor=user.mentor_profile)
            return Certificate.objects.filter(student__in=mentees)
        return Certificate.objects.none()

# --- AICTECategoryViewSet ---
class AICTECategoryViewSet(viewsets.ModelViewSet):
    queryset = AICTECategory.objects.all()
    serializer_class = AICTECategorySerializer
    permission_classes = [IsAuthenticated]

# --- AICTEPointTransactionViewSet ---
class AICTEPointTransactionViewSet(viewsets.ModelViewSet):
    queryset = AICTEPointTransaction.objects.all()
    serializer_class = AICTEPointTransactionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        transaction = self.get_object()
        transaction.status = 'APPROVED'
        transaction.save()
        return Response({'status': 'Transaction approved.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        transaction = self.get_object()
        transaction.status = 'REJECTED'
        transaction.save()
        return Response({'status': 'Transaction rejected.'}, status=status.HTTP_200_OK)

# --- NotificationViewSet ---
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return notifications for the logged-in user
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        notifications = self.get_queryset()
        notifications.update(is_read=True)
        return Response({'status': 'All notifications marked as read.'}, status=status.HTTP_200_OK)

# --- AuditLogViewSet ---
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
def event_statistics(request):
    stats = Event.objects.annotate(
        total_registrations=Count('registrations')
    ).values('id', 'name', 'total_registrations')
    return Response(stats, status=status.HTTP_200_OK)