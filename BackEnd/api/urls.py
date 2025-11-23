from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import (
    # Authentication
    RegisterView, VerifyEmailView, ResendVerificationEmailView, LoginView, RequestPasswordResetView, ResetPasswordView,
    
    # Profile Management
    ProfileView, StudentProfileView, MentorProfileView, ClubOrganizerProfileView,
    
    # Student Management
    StudentViewSet,
    
    # Mentor Management
    MentorViewSet,
    
    # Club Organizer Management
    ClubOrganizerViewSet,
    
    # User Management
    AdminUserCreationView, BulkUserCreationView,
    
    # Mentor-Mentee
    MentorMenteeAssignmentView, BulkMenteeAssignmentView,
    
    # Admin Management
    AdminUserListViewSet, AdminClubManagementViewSet, AdminMenteeAssignmentViewSet,
    AdminAICTEConfigViewSet, AdminReportingViewSet,
    
    # Club Management
    ClubViewSet, ClubMemberViewSet, ClubRoleViewSet,
    
    # Event Management
    EventViewSet, EventAttendanceViewSet,
    
    # Hall Booking
    HallViewSet, HallBookingViewSet,
    
    # Certificates
    CertificateTemplateViewSet, CertificateViewSet,
    
    # AICTE
    AICTECategoryViewSet, AICTEPointTransactionViewSet,
    
    # Notifications & Audit
    NotificationViewSet, AuditLogViewSet,
    
    # Reports
    dashboard_stats
)

router = DefaultRouter()

# ViewSet registrations
router.register(r'students', StudentViewSet, basename='student')
router.register(r'mentors', MentorViewSet, basename='mentor')
router.register(r'club-organizers', ClubOrganizerViewSet, basename='club-organizer')
router.register(r'admin/users', AdminUserListViewSet, basename='admin-user-list')
router.register(r'admin/clubs', AdminClubManagementViewSet, basename='admin-club-management')
router.register(r'admin/mentees', AdminMenteeAssignmentViewSet, basename='admin-mentee-assignment')
router.register(r'admin/aicte', AdminAICTEConfigViewSet, basename='admin-aicte-config')
router.register(r'admin/reports', AdminReportingViewSet, basename='admin-reports')
router.register(r'events', EventViewSet, basename='event')
router.register(r'event-attendance', EventAttendanceViewSet, basename='event-attendance')
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'certificate-templates', CertificateTemplateViewSet, basename='certificate-template')
router.register(r'clubs', ClubViewSet, basename='club')
router.register(r'club-members', ClubMemberViewSet, basename='club-member')
router.register(r'club-roles', ClubRoleViewSet, basename='club-role')
router.register(r'halls', HallViewSet, basename='hall')
router.register(r'hall-bookings', HallBookingViewSet, basename='hall-booking')
router.register(r'aicte-categories', AICTECategoryViewSet, basename='aicte-category')
router.register(r'aicte-transactions', AICTEPointTransactionViewSet, basename='aicte-transaction')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('auth/resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/password-reset/request/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('auth/password-reset/confirm/', ResetPasswordView.as_view(), name='reset-password'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/token/obtain/', TokenObtainPairView.as_view(), name='token-obtain'),
    
    # Profile endpoints
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/student/', StudentProfileView.as_view(), name='student-profile'),
    path('profile/mentor/', MentorProfileView.as_view(), name='mentor-profile'),
    path('profile/club-organizer/', ClubOrganizerProfileView.as_view(), name='club-organizer-profile'),
    
    # Admin user management
    path('admin/users/create/', AdminUserCreationView.as_view(), name='admin-create-user'),
    path('admin/users/bulk-create/', BulkUserCreationView.as_view(), name='admin-bulk-create-users'),
    
    # Admin Club management
    path('admin/clubs/create/', AdminClubManagementViewSet.as_view({'post': 'create'}), name='admin-create-club'),
    path('admin/clubs/<int:pk>/assign-organizer/', AdminClubManagementViewSet.as_view({'post': 'assign_organizer'}), name='assign-organizer'),
    path('admin/clubs/<int:pk>/assign-coordinator/', AdminClubManagementViewSet.as_view({'post': 'assign_coordinator'}), name='assign-coordinator'),
    
    # Mentor-mentee management
    path('admin/mentees/assign/', MentorMenteeAssignmentView.as_view(), name='admin-assign-mentees'),
    path('admin/mentees/bulk-assign/', BulkMenteeAssignmentView.as_view(), name='admin-bulk-assign-mentees'),
    
    # Reports & Statistics
    path('dashboard/stats/', dashboard_stats, name='dashboard-stats'),
]