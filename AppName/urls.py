from django.urls import path
from AppName import views

urlpatterns = [
    path('', views.home, name='Home')
]
