from django.urls import path
from django.contrib.auth import views as auth_views
from Cert import views

urlpatterns = [
    path('', views.home, name='home'),
    path('landingpage/', views.landingpage, name='landingpage'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.custom_logout_view, name='logout'),

    # Role-specific Dashboard URLs
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('club_dashboard/', views.club_dashboard, name='club_dashboard'),
    path('mentor_dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    
    # Club role's urls
    path('create_event/', views.create_event, name='create_event'),
    path('upload_participants/<int:event_id>/', views.upload_participants, name='upload_participants'),
    path('generate_certificates/<int:event_id>/', views.generate_certificates, name='generate_certificates'),
    path('update_event_status/<int:event_id>/', views.update_event_status, name='update_event_status'),
    path('upload_certificate_template/<int:event_id>/', views.upload_certificate_template, name='upload_certificate_template'),
    path('register_club/', views.register_club, name='register_club'),
]
