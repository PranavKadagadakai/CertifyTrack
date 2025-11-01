from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Club, Event, Participant, Certificate, CertificateTemplate
from django.core.exceptions import ValidationError

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'role', 'full_name', 'usn', 'aicte_points', 'mentor']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'full_name', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        role = self.initial_data.get('role')
        if role == 'student' and not value.endswith('@students.git.edu'):
            raise serializers.ValidationError("Student emails must end with '@students.git.edu'.")
        if role in ['club', 'mentor'] and not value.endswith('@git.edu'):
            raise serializers.ValidationError("Club and Mentor emails must end with '@git.edu'.")
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')
        full_name = validated_data.pop('full_name')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        user.profile.role = role
        user.profile.full_name = full_name
        user.profile.save()
        
        if role == 'club':
            Club.objects.create(admin=user, name=f"{user.username}'s Club")
            
        return user

class ClubSerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField()
    class Meta:
        model = Club
        fields = '__all__'
        
class CertificateTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateTemplate
        fields = ['id', 'template_file', 'uploaded_at']

class EventSerializer(serializers.ModelSerializer):
    club = serializers.StringRelatedField()
    participants_count = serializers.SerializerMethodField()
    template_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'club', 'date', 'description', 'status', 'aicte_points', 'participant_limit', 'created_at', 'participants_count', 'template_url']
        read_only_fields = ['club']

    def get_participants_count(self, obj):
        return obj.participants.count()

    def get_template_url(self, obj):
        request = self.context.get('request')
        if obj.template and obj.template.template_file:
            return request.build_absolute_uri(obj.template.template_file.url)
        return None

class ParticipantSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.profile.full_name', read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'event', 'student', 'student_name']

class CertificateSerializer(serializers.ModelSerializer):
    participant_name = serializers.CharField(source='participant.student.profile.full_name', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)
    certificate_url = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = ['id', 'event_name', 'participant_name', 'certificate_url', 'generated_at', 'verified']

    def get_certificate_url(self, obj):
        request = self.context.get('request')
        if obj.certificate_file:
            return request.build_absolute_uri(obj.certificate_file.url)
        return None