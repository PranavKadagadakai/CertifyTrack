from django.urls import path
from django.contrib.auth import views as auth_views
from Cert import views

urlpatterns = [
    # Base URLs
    path('', views.home, name='home'),
    path('landingpage/', views.landingpage, name='landingpage'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.custom_logout_view, name='logout'),

    # Role-specific Dashboard URLs
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('club_dashboard/', views.club_dashboard, name='club_dashboard'),
    path('mentor_dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    
    # Club role's URLs
    path('create_event/', views.create_event, name='create_event'),
    path('upload_participants/<int:event_id>/', views.upload_participants, name='upload_participants'),
    path('generate_certificates/<int:event_id>/', views.generate_event_certificates, name='generate_certificates'),
    path('update_event_status/<int:event_id>/', views.update_event_status, name='update_event_status'),
    path('upload_certificate_template/<int:event_id>/', views.upload_certificate_template, name='upload_certificate_template'),
    # path('register_club/', views.register_club, name='register_club'),
    
    # Student role's URLs
    path('events/', views.view_events, name='view_events'),
    path('register-for-event/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('aicte-points/', views.view_aicte_points_and_certificates, name='view_aicte_points_and_certificates'),
    path('event_history/', views.event_history, name='event_history'),
    # path('certificate/<int:certificate_id>/', views.view_certificate, name='view_certificate'),
    
    # Mentor role's URLs
    path('verify-certificate/<int:certificate_id>/', views.verify_certificate, name='verify_certificate'),
    path('mentor_students/', views.mentor_students, name='mentor_students'),
    path('assign_students/', views.assign_students, name='assign_students'),
    path('generate_certificate/<int:event_id>/', views.generate_certificate, name='generate_certificate'),
    path('assign_event/', views.assign_event, name='assign_event'),
]
