from django.urls import path
from Cert import views

urlpatterns = [
    path('', views.home, name='Home')
]
