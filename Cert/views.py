from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'base.html')

def landingpage(request):
    return render(request, 'landingpage.html')

def profile(request):
    return render(request, 'profile.html')