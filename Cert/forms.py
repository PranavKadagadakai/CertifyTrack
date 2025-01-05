from django import forms
from .models import Club, Event, Profile, CertificateTemplate
from django.contrib.auth.models import User
import re

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
        fields = ['name', 'date', 'description', 'club', 'status', 'aicte_points', 'participant_limit', 'certificate_template']
        
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['phone', 'address', 'usn']
#         widgets = {
#             'usn': forms.TextInput(attrs={'placeholder': 'Enter USN, e.g., 2GI22IS001'}),
#         }

#     def clean_usn(self):
#         usn = self.cleaned_data.get('usn')
#         role = self.cleaned_data.get('role')

#         if role == 'student' and usn:
#             pattern = r"^\d{2}[A-Z]{2}\d{2}[A-Z]{2}\d{3}$"
#             if not re.match(pattern, usn):
#                 raise forms.ValidationError("USN must follow the format: 2GI22IS001.")
#         return usn

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone', 'address', 'usn']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'cols': 20}),
        }

    def __init__(self, *args, **kwargs):
        profile = kwargs.get('instance')  # Get the profile instance from kwargs
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        # If the user is not a student, remove the 'usn' field
        if profile and profile.role != 'student':
            self.fields.pop('usn')

class ParticipantUploadForm(forms.Form):
    participant_file = forms.FileField()
    
class AssignStudentsForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(profile__role='student'),
        widget=forms.CheckboxSelectMultiple,
        label="Select Students"
    )
    mentor = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='mentor'),
        label="Select Mentor"
    )

class CertificateTemplateForm(forms.ModelForm):
    class Meta:
        model = CertificateTemplate
        fields = ['template_file']