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
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200',
                'placeholder': 'Enter a unique club name'
            }),
        }

class EventRegistrationForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput())

class EventForm(forms.ModelForm):
    certificate_template = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200'
        })
    )

    date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200'
    }))

    class Meta:
        model = Event
        fields = [
            'name',
            'date',
            'description',
            'club',
            'status',
            'aicte_points',
            'participant_limit',
            'certificate_template'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200',
                'placeholder': 'Enter event name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200',
                'rows': 4,
                'placeholder': 'Enter event description'
            }),
            'club': forms.Select(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200'
            }),
            'aicte_points': forms.NumberInput(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200',
                'placeholder': 'Enter AICTE points'
            }),
            'participant_limit': forms.NumberInput(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200',
                'placeholder': 'Enter participant limit'
            }),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone', 'address', 'usn']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200',
                'placeholder': 'Enter your full name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200',
                'placeholder': 'Enter your phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200',
                'rows': 3,
                'placeholder': 'Enter your address'
            }),
            'usn': forms.TextInput(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200',
                'placeholder': 'Enter your USN'
            }),
        }

    def __init__(self, *args, **kwargs):
        profile = kwargs.get('instance')
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        if profile and profile.role != 'student':
            self.fields.pop('usn')

class ParticipantUploadForm(forms.Form):
    participant_file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200'
    }))

class AssignStudentsForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(profile__role='student'),
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200',
            'size': '6'  # Set size to show 6 students at a time
        }),
        label="Select Students"
    )
    mentor = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='mentor'),
        widget=forms.Select(attrs={
            'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200'
        }),
        label="Select Mentor"
    )


class CertificateTemplateForm(forms.ModelForm):
    class Meta:
        model = CertificateTemplate
        fields = ['template_file']
        widgets = {
            'template_file': forms.FileInput(attrs={
                'class': 'w-full p-2 bg-gray-50 border rounded-lg dark:bg-gray-700 dark:text-gray-200'
            }),
        }
