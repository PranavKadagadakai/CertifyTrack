from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LoginView, ProfileView, EventViewSet, 
    CertificateViewSet, DashboardDataView, MentorViewSet
)

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'mentor', MentorViewSet, basename='mentor')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', DashboardDataView.as_view(), name='dashboard-data'),
]