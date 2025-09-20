from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    RegisterView, ProfileView, EventViewSet, 
    CertificateViewSet, DashboardDataView, MentorViewSet,
    CustomTokenObtainPairView,
)

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'mentor', MentorViewSet, basename='mentor')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', DashboardDataView.as_view(), name='dashboard-data'),
]