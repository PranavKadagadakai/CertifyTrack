from django.urls import path
from django.contrib.auth import views as auth_views
from Cert import views

urlpatterns = [
    path('', views.home, name='home'),
# <<<<<<< HEAD
#     path('landingpage', views.landingpage, name='landingpage'),
#     path('profile', views.profile, name='profile'),
#     path('signup', views.signup, name='signup')

    path('landingpage/', views.landingpage, name='landingpage'),
    path('profile/', views.profile, name='profile'),

    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.custom_logout_view, name='logout'),

    # Role-specific Dashboard URLs
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('club_dashboard/', views.club_dashboard, name='club_dashboard'),
    path('mentor_dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
]
