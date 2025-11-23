from rest_framework import serializers
from django.utils.timezone import now, timedelta
from django.contrib.auth.hashers import make_password
import uuid
import secrets
import string

from .models import (
    User, Student, Mentor, ClubOrganizer, Club, Event, EventRegistration, Certificate,
    Hall, HallBooking, AICTECategory, AICTEPointTransaction,
    Notification, AuditLog, ClubMember, ClubRole, EventAttendance,
    CertificateTemplate
)
from .email_utils import send_verification_email, send_password_reset_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'is_email_verified', 'date_joined']


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    mentor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'usn', 'department', 'semester', 
            'phone_number', 'date_of_birth', 'address', 'profile_photo',
            'emergency_contact_name', 'emergency_contact_phone',
            'profile_completed', 'profile_completed_at', 'mentor_name'
        ]
        read_only_fields = ['user', 'profile_completed_at']
    
    def get_mentor_name(self, obj):
        if obj.mentor:
            return obj.mentor.user.get_full_name() or obj.mentor.user.username
        return None


class MentorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Mentor
        fields = [
            'id', 'user', 'employee_id', 'department', 'designation',
            'phone_number', 'date_of_birth', 'address', 'profile_photo',
            'qualifications', 'bio', 'profile_completed', 'profile_completed_at'
        ]
        read_only_fields = ['user', 'profile_completed_at']


class ClubOrganizerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for club organizer (student club head or coordinator) profiles.
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ClubOrganizer
        fields = [
            'id', 'user', 'phone_number', 'date_of_birth', 'address', 
            'profile_photo', 'designation_in_club', 'bio', 
            'profile_completed', 'profile_completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'profile_completed_at', 'created_at', 'updated_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    # Student-specific fields
    usn = serializers.CharField(required=False, allow_blank=True)
    semester = serializers.IntegerField(required=False)
    department = serializers.CharField(required=False, allow_blank=True)
    
    # Mentor-specific fields
    employee_id = serializers.CharField(required=False, allow_blank=True)
    designation = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name',
            'user_type', 'usn', 'semester', 'department', 'employee_id', 'designation'
        ]
    
    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        request = self.context.get("request")
        user_type = data.get("user_type")
        
        if user_type == "student":
            usn = data.get("usn") or (request.data.get("usn") if request else None)
            dept = data.get("department") or (request.data.get("department") if request else None)
            sem = data.get("semester") or (request.data.get("semester") if request else None)
            
            if not usn:
                raise serializers.ValidationError({"usn": "USN is required for student registration."})
            
            if Student.objects.filter(usn=usn).exists():
                raise serializers.ValidationError({"usn": "This USN is already registered."})
            
            if sem and (int(sem) < 1 or int(sem) > 8):
                raise serializers.ValidationError({"semester": "Semester must be between 1 and 8."})
        
        elif user_type == "mentor":
            emp_id = data.get("employee_id") or (request.data.get("employee_id") if request else None)
            desig = data.get("designation") or (request.data.get("designation") if request else None)
            
            if not emp_id:
                raise serializers.ValidationError({"employee_id": "Employee ID is required for mentor registration."})
            
            if Mentor.objects.filter(employee_id=emp_id).exists():
                raise serializers.ValidationError({"employee_id": "This Employee ID is already registered."})
            
            if not desig:
                raise serializers.ValidationError({"designation": "Designation is required for mentor registration."})
        
        # club_organizer doesn't require additional fields - they can be filled in profile completion
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm', None)
        
        # Extract role-specific fields that aren't part of User model
        usn = validated_data.pop('usn', None)
        semester = validated_data.pop('semester', None)
        employee_id = validated_data.pop('employee_id', None)
        designation = validated_data.pop('designation', None)
        department = validated_data.pop('department', None)
        
        # Generate email verification token
        verification_token = secrets.token_urlsafe(32)
        
        # Create user with remaining validated data
        user = User.objects.create(
            **validated_data,
            email_verification_token=verification_token,
            is_email_verified=False
        )
        user.set_password(password)
        user.save()
        
        # Send verification email
        send_verification_email(user)
        
        # Create role-specific profile
        if user.user_type == 'student':
            Student.objects.create(
                user=user,
                usn=usn or '',
                department=department or '',
                semester=int(semester) if semester else 1
            )
        
        elif user.user_type == 'mentor':
            Mentor.objects.create(
                user=user,
                employee_id=employee_id or '',
                department=department or '',
                designation=designation or ''
            )
        
        elif user.user_type == 'club_organizer':
            ClubOrganizer.objects.create(
                user=user
            )
        
        return user


class StudentSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            "id", "user_details", "usn", "department", "semester", 
            "phone_number", "date_of_birth", "address", "profile_photo",
            "emergency_contact_name", "emergency_contact_phone"
        ]


class ClubRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubRole
        fields = '__all__'


class ClubMemberSerializer(serializers.ModelSerializer):
    student_usn = serializers.CharField(source='student.usn', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = ClubMember
        fields = ['id', 'club', 'student', 'student_usn', 'role', 'role_name', 'joined_date', 'is_active']


class ClubSerializer(serializers.ModelSerializer):
    members = ClubMemberSerializer(many=True, read_only=True, source='members.all')
    faculty_coordinator_name = serializers.CharField(source='faculty_coordinator.user.get_full_name', read_only=True)
    club_head_name = serializers.CharField(source='club_head.user.get_full_name', read_only=True)
    
    class Meta:
        model = Club
        fields = [
            'id', 'name', 'description', 'faculty_coordinator', 'faculty_coordinator_name',
            'club_head', 'club_head_name', 'established_date', 'is_active', 'created_at', 'updated_at', 'members'
        ]


class EventAttendanceSerializer(serializers.ModelSerializer):
    student_usn = serializers.CharField(source='student.usn', read_only=True)
    
    class Meta:
        model = EventAttendance
        fields = ['id', 'event', 'student', 'student_usn', 'marked_at', 'is_present', 'marked_by']
        read_only_fields = ['marked_at', 'marked_by']


class EventRegistrationSerializer(serializers.ModelSerializer):
    student_usn = serializers.CharField(source='student.usn', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)
    
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'event_name', 'student', 'student_usn', 'registration_date', 'status']


class EventSerializer(serializers.ModelSerializer):
    registrations = EventRegistrationSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'club', 'name', 'description', 'event_date', 'start_time', 'end_time',
            'max_participants', 'status', 'created_at', 'updated_at', 'created_by', 'created_by_username',
            'registrations'
        ]


class CertificateTemplateSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = CertificateTemplate
        fields = ['id', 'name', 'template_file', 'created_by', 'created_by_username', 'created_at', 'updated_at', 'is_active', 'version']
        read_only_fields = ['created_at', 'updated_at']


class CertificateSerializer(serializers.ModelSerializer):
    student_usn = serializers.CharField(source='student.usn', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)
    
    class Meta:
        model = Certificate
        fields = [
            'id', 'event', 'event_name', 'student', 'student_usn',
            'file', 'file_hash', 'issue_date'
        ]
        read_only_fields = ['file', 'file_hash', 'issue_date']


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'


class HallBookingSerializer(serializers.ModelSerializer):
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    booked_by_username = serializers.CharField(source='booked_by.student.user.username', read_only=True, allow_null=True)
    approved_by_username = serializers.CharField(source='approved_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = HallBooking
        fields = [
            'id', 'hall', 'hall_name', 'event', 'booked_by', 'booked_by_username',
            'booking_date', 'start_time', 'end_time', 'booking_status',
            'approved_by', 'approved_by_username', 'created_at', 'updated_at', 'rejection_reason'
        ]
        read_only_fields = ['approved_by', 'created_at', 'updated_at']


class AICTECategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AICTECategory
        fields = '__all__'


class AICTEPointTransactionSerializer(serializers.ModelSerializer):
    student_usn = serializers.CharField(source='student.usn', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    approved_by_username = serializers.CharField(source='approved_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = AICTEPointTransaction
        fields = [
            'id', 'student', 'student_usn', 'event', 'event_name', 'category', 'category_name',
            'points_allocated', 'status', 'approved_by', 'approved_by_username',
            'approval_date', 'rejection_reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['approved_by', 'approval_date', 'created_at', 'updated_at']
    
    def validate(self, data):
        category = data.get('category') or getattr(self.instance, 'category', None)
        points = data.get('points_allocated') or getattr(self.instance, 'points_allocated', None)
        if category and points is not None:
            minp = category.min_points_required
            maxp = category.max_points_allowed
            if minp is not None and points < minp:
                raise serializers.ValidationError(f"points_allocated ({points}) is below category minimum ({minp}).")
            if maxp is not None and points > maxp:
                raise serializers.ValidationError(f"points_allocated ({points}) exceeds category maximum ({maxp}).")
        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['created_at']


class AuditLogSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_username', 'action', 'timestamp']
        read_only_fields = ['timestamp']

