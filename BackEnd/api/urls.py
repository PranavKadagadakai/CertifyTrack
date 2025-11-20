from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, ProfileView, EventViewSet, 
    CertificateViewSet, ClubViewSet, HallViewSet, 
    HallBookingViewSet, AICTECategoryViewSet, AICTEPointTransactionViewSet,
    NotificationViewSet, event_statistics, AuditLogViewSet, get_user_profile,
    register_user
)

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'clubs', ClubViewSet, basename='club')
router.register(r'halls', HallViewSet, basename='hall')
router.register(r'hall-bookings', HallBookingViewSet, basename='hall-booking')
router.register(r'aicte-categories', AICTECategoryViewSet, basename='aicte-category')
router.register(r'aicte-transactions', AICTEPointTransactionViewSet, basename='aicte-transaction')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('reports/event-statistics/', event_statistics, name='event-statistics'),
    path('auth/profile', get_user_profile, name='get_user_profile'),
    path('auth/register', register_user, name='register_user'),
]