from django import forms
from .models import Club, Event

class ClubCreationForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name']
        labels = {
            'name': 'Club Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter a unique club name'}),
        }
        
class EventRegistrationForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput())
    
class EventForm(forms.ModelForm):
    certificate_template = forms.FileField(required=False)  # Optional file upload
    
    # Specify the widget for the date field explicitly
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Event
        fields = ['name', 'date', 'description', 'club', 'status', 'certificate_template']