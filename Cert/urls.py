from django.urls import path
from Cert import views

urlpatterns = [
    path('', views.home, name='home'),
    path('landingpage', views.landingpage, name='landingpage'),
    path('profile', views.profile, name='profile')
    
]
