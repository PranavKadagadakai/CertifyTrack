from django import forms
from .models import Club

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