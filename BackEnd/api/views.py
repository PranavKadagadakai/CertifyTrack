from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum
from django.utils.timezone import now
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode

from .models import (
    User, Student, Mentor, Club, Event, EventRegistration, Certificate,
    Hall, HallBooking, AICTECategory, AICTEPointTransaction, Notification, AuditLog
)
from .serializers import (
    UserSerializer, RegisterSerializer, EventSerializer,
    CertificateSerializer, EventRegistrationSerializer, ClubSerializer,
    HallSerializer, HallBookingSerializer, AICTECategorySerializer, AICTEPointTransactionSerializer,
    NotificationSerializer, AuditLogSerializer
)
from .permissions import IsClubAdmin, IsStudent, IsMentor


def log_action(user, action):
    AuditLog.objects.create(user=user, action=action)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        log_action(user, f"User registered: {user.username}")


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        mentor = getattr(self.request.user, "mentor_profile", None)
        if mentor is None:
            raise PermissionDenied("Only mentors can create clubs.")
        instance = serializer.save(faculty_coordinator=mentor)
        log_action(self.request.user, f"Created Club: {instance.name}")


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'generate_certificates', 'start_event', 'end_event']:
            self.permission_classes = [IsClubAdmin]
        elif self.action == 'register':
            self.permission_classes = [IsStudent]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        student = getattr(self.request.user, "student_profile", None)
        if student is None:
            raise PermissionDenied("Only club organizers can create events.")
        club = Club.objects.filter(club_head=student).first()
        if club is None:
            raise PermissionDenied("You are not the head of any club.")
        event = serializer.save(club=club)
        log_action(self.request.user, f"Created Event: {event.name}")

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = self.get_object()
        student = getattr(request.user, "student_profile", None)
        if student is None:
            raise PermissionDenied("Only students can register for events.")
        if event.status != 'scheduled':
            raise ValidationError("Event registration is closed.")
        if event.max_participants and event.registrations.count() >= event.max_participants:
            raise ValidationError("Event is full.")
        if EventRegistration.objects.filter(event=event, student=student).exists():
            raise ValidationError("Already registered.")
        EventRegistration.objects.create(event=event, student=student)
        log_action(request.user, f"Registered for event: {event.name}")
        return Response({'status': 'Successfully registered.'}, status=201)

    @action(detail=True, methods=['post'], url_path='generate-certificates')
    def generate_certificates(self, request, pk=None):
        event = self.get_object()
        participants = event.registrations.all()
        if not participants:
            raise ValidationError("No participants for this event.")
        for reg in participants:
            student = reg.student
            certificate, created = Certificate.objects.get_or_create(event=event, student=student)
            qr_data = f"Certificate Verification - Event {event.id}, USN {student.usn}"
            qr = qrcode.make(qr_data)
            qr_io = BytesIO()
            qr.save(qr_io, format="PNG")
            # PDF generation not implemented here - integrate worker later
            ContentFile(qr_io.getvalue(), f"{student.usn}_qr.png")
        event.status = 'completed'
        event.save()
        log_action(request.user, f"Generated certificates for event: {event.name}")
        return Response({'status': 'Certificates generated successfully.'})

    @action(detail=True, methods=['post'], url_path='start')
    def start_event(self, request, pk=None):
        event = self.get_object()
        if event.status != 'scheduled':
            raise ValidationError("Only scheduled events can be started.")
        event.status = 'ongoing'
        event.save()
        log_action(request.user, f"Started event: {event.name}")
        return Response({'status': 'Event started.'})

    @action(detail=True, methods=['post'], url_path='end')
    def end_event(self, request, pk=None):
        event = self.get_object()
        if event.status != 'ongoing':
            raise ValidationError("Only ongoing events can be ended.")
        event.status = 'completed'
        event.save()
        log_action(request.user, f"Ended event: {event.name}")
        return Response({'status': 'Event ended.'})


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAuthenticated]


class HallBookingViewSet(viewsets.ModelViewSet):
    queryset = HallBooking.objects.all()
    serializer_class = HallBookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        student = getattr(self.request.user, "student_profile", None)
        if student is None:
            raise PermissionDenied("Only club members can book halls.")
        instance = serializer.save(booked_by=student)
        log_action(self.request.user, f"Hall booking created for {instance.hall.name}")


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


class AICTECategoryViewSet(viewsets.ModelViewSet):
    queryset = AICTECategory.objects.all()
    serializer_class = AICTECategorySerializer
    permission_classes = [IsAuthenticated]


class AICTEPointTransactionViewSet(viewsets.ModelViewSet):
    queryset = AICTEPointTransaction.objects.all()
    serializer_class = AICTEPointTransactionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        tx = self.get_object()
        tx.status = 'APPROVED'
        tx.save()
        log_action(request.user, f"Approved AICTE transaction ID {tx.id}")
        return Response({'status': 'Transaction approved.'})

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        tx = self.get_object()
        tx.status = 'REJECTED'
        tx.save()
        log_action(request.user, f"Rejected AICTE transaction ID {tx.id}")
        return Response({'status': 'Transaction rejected.'})


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        notifications = self.get_queryset()
        notifications.update(is_read=True)
        log_action(request.user, "Marked all notifications as read")
        return Response({'status': 'All notifications marked as read.'})


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
def event_statistics(request):
    stats = Event.objects.annotate(total_registrations=Count('registrations')).values('id', 'name', 'total_registrations')
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    return Response({"id": user.id, "username": user.username, "email": user.email, "role": user.user_type})


from .models import User as CustomUser

@api_view(['POST'])
def register_user(request):
    data = request.data
    try:
        user = CustomUser.objects.create_user(username=data['username'], email=data['email'], password=data['password'], user_type=data['role'])
        log_action(user, "User registered (legacy route)")
        return Response({"message": "User registered successfully!"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def aicte_summary(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    total_points = AICTEPointTransaction.objects.filter(student=student, status="APPROVED").aggregate(total=Sum('points_allocated'))['total'] or 0
    categories = AICTECategory.objects.all()
    category_data = []
    for category in categories:
        tx = AICTEPointTransaction.objects.filter(student=student, category=category)
        category_data.append({
            "category": category.name,
            "approved_points": tx.filter(status='APPROVED').aggregate(sum=Sum('points_allocated'))['sum'] or 0,
            "pending_points": tx.filter(status='PENDING').aggregate(sum=Sum('points_allocated'))['sum'] or 0,
            "rejected_points": tx.filter(status='REJECTED').aggregate(sum=Sum('points_allocated'))['sum'] or 0,
        })
    last_tx = AICTEPointTransaction.objects.filter(student=student).order_by('-id').first()
    last_updated = last_tx.id if last_tx else None
    return Response({"student_id": student.id, "student_usn": student.usn, "total_points": total_points, "categories": category_data, "last_updated": last_updated})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mentor_dashboard(request):
    mentor = getattr(request.user, 'mentor_profile', None)
    if mentor is None:
        raise PermissionDenied("Only mentors may access this endpoint.")
    mentees = Student.objects.filter(mentor=mentor)
    result = []
    for s in mentees:
        tx = AICTEPointTransaction.objects.filter(student=s)
        result.append({
            'student_id': s.id,
            'student_usn': s.usn,
            'approved_points': tx.filter(status='APPROVED').aggregate(sum=Sum('points_allocated'))['sum'] or 0,
            'pending_points': tx.filter(status='PENDING').aggregate(sum=Sum('points_allocated'))['sum'] or 0,
            'rejected_points': tx.filter(status='REJECTED').aggregate(sum=Sum('points_allocated'))['sum'] or 0,
        })
    return Response({'mentees': result})


@api_view(['GET'])
@permission_classes([AllowAny])
def certificate_verify(request, file_hash):
    cert = Certificate.objects.filter(file_hash=file_hash).select_related('student', 'event').first()
    if not cert:
        return Response({'verified': False, 'message': 'Certificate not found.'}, status=404)
    data = {
        'verified': True,
        'certificate_id': cert.id,
        'student_usn': cert.student.usn,
        'event_name': cert.event.name,
        'issue_date': cert.issue_date,
        'file_hash': cert.file_hash,
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_aicte_points(request):
    """
    Returns:
    - total points
    - approved transactions
    - pending transactions
    - category-wise summary
    """

    user = request.user

    if user.user_type != "student":
        return Response({"error": "Only students can access AICTE points"}, status=403)

    student = user.student_profile

    transactions = student.aicte_transactions.select_related("category").all()

    approved = transactions.filter(status="APPROVED")
    pending = transactions.filter(status="PENDING")

    category_summary = {}
    for tx in approved:
        cat = tx.category.name
        category_summary.setdefault(cat, 0)
        category_summary[cat] += tx.points_allocated

    return Response({
        "total_points": student.total_aicte_points,
        "approved_transactions": [
            {
                "id": tx.id,
                "event": tx.event.name,
                "category": tx.category.name,
                "points": tx.points_allocated,
                "status": tx.status,
            }
            for tx in approved
        ],
        "pending_transactions": [
            {
                "id": tx.id,
                "event": tx.event.name,
                "category": tx.category.name,
                "points": tx.points_allocated,
                "status": tx.status,
            }
            for tx in pending
        ],
        "category_summary": category_summary,
    })