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
    CertificateTemplate, UserNotificationPreferences, PrincipalSignature,
    validate_usn_format, validate_employee_id_format, validate_email_domain,
    DEPARTMENT_BRANCH_MAPPING
)
from .email_utils import send_verification_email, send_password_reset_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'user_type', 'is_email_verified', 'date_joined'
        ]
        read_only_fields = ['email', 'user_type', 'date_joined']


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    mentor_name = serializers.SerializerMethodField(read_only=True)
    profile_photo = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)
    total_aicte_points = serializers.SerializerMethodField(read_only=True)
    required_aicte_points = serializers.SerializerMethodField(read_only=True)
    is_aicte_completed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'usn', 'department', 'semester', 'admission_type',
            'phone_number', 'date_of_birth', 'address', 'profile_photo',
            'emergency_contact_name', 'emergency_contact_phone',
            'profile_completed', 'profile_completed_at', 'mentor_name',
            'total_aicte_points', 'required_aicte_points', 'is_aicte_completed'
        ]
        read_only_fields = ['profile_completed_at']

    def get_mentor_name(self, obj):
        return obj.mentor.user.get_full_name() if obj.mentor else None

    def get_total_aicte_points(self, obj):
        return obj.total_aicte_points

    def get_required_aicte_points(self, obj):
        return obj.required_aicte_points

    def get_is_aicte_completed(self, obj):
        return obj.is_aicte_completed
    
    def to_internal_value(self, data):
        """
        Allow username / first_name / last_name to be passed at root level.
        """
        user_fields = ['username', 'first_name', 'last_name']

        data = data.copy()

        user_data = {}

        for f in user_fields:
            if f in data:
                value = data.get(f)          # returns the FIRST value as a string
                user_data[f] = value
                data.pop(f)

        ret = super().to_internal_value(data)

        if user_data:
            ret['user'] = user_data

        return ret

    def validate(self, data):
        """
        Validate USN format and branch consistency for profile updates
        """
        request = self.context.get("request")
        user_data = data.get("user", {})

        # Email validation - only if provided in data
        if "email" in user_data and user_data["email"]:
            is_valid, error_msg = validate_email_domain(user_data["email"], 'student')
            if not is_valid:
                raise serializers.ValidationError({"email": error_msg})

        # USN validation - only if provided in data
        if "usn" in data and "department" in data and data.get("department"):
            is_valid, error_msg, admission_type = validate_usn_format(data["usn"], data["department"])
            if not is_valid:
                raise serializers.ValidationError({"usn": error_msg})

        return data

    def update(self, instance, validated_data):
        # Extract nested user updates from sourced fields
        user_data = validated_data.pop("user", {})  # comes from source='user.*'
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Remove file fields that are None to prevent overwriting existing files
        if "profile_photo" in validated_data and validated_data["profile_photo"] is None:
            del validated_data["profile_photo"]

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Check profile completion
        required_fields = [
            'phone_number', 'date_of_birth', 'address',
            'emergency_contact_name', 'emergency_contact_phone'
        ]
        if all(getattr(instance, field, None) for field in required_fields) and not instance.profile_completed:
            instance.profile_completed = True
            instance.profile_completed_at = now()
            instance.save()

        return instance


class MentorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    profile_photo = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)
    signature = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)

    class Meta:
        model = Mentor
        fields = [
            'id', 'user', 'employee_id', 'department', 'designation',
            'phone_number', 'date_of_birth', 'address', 'profile_photo',
            'qualifications', 'bio', 'signature', 'profile_completed', 'profile_completed_at'
        ]
        read_only_fields = ['profile_completed_at']

    def to_internal_value(self, data):
        """
        Allow username / first_name / last_name to be passed at root level.
        """
        user_fields = ['username', 'first_name', 'last_name']

        data = data.copy()

        user_data = {}

        for f in user_fields:
            if f in data:
                value = data.get(f)          # returns the FIRST value as a string
                user_data[f] = value
                data.pop(f)

        ret = super().to_internal_value(data)

        if user_data:
            ret['user'] = user_data

        return ret

    def validate(self, data):
        """
        Validate Employee ID format and branch consistency for profile updates
        """
        user_data = data.get("user", {})

        # Email validation - only if provided in data
        if "email" in user_data and user_data["email"]:
            is_valid, error_msg = validate_email_domain(user_data["email"], 'mentor')
            if not is_valid:
                raise serializers.ValidationError({"email": error_msg})

        # Employee ID validation - only if provided in data
        if "employee_id" in data and "department" in data and data.get("department"):
            is_valid, error_msg = validate_employee_id_format(data["employee_id"], data["department"])
            if not is_valid:
                raise serializers.ValidationError({"employee_id": error_msg})

        return data

    def update(self, instance, validated_data):
        # Extract nested user updates from sourced fields
        user_data = validated_data.pop("user", {})  # comes from source='user.*'
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Remove file fields that are None to prevent overwriting existing files
        if "profile_photo" in validated_data and validated_data["profile_photo"] is None:
            del validated_data["profile_photo"]
        if "signature" in validated_data and validated_data["signature"] is None:
            del validated_data["signature"]

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Check profile completion
        required_fields = [
            'phone_number', 'date_of_birth', 'address', 'qualifications'
        ]
        if all(getattr(instance, field, None) for field in required_fields) and not instance.profile_completed:
            instance.profile_completed = True
            instance.profile_completed_at = now()
            instance.save()

        return instance


class ClubOrganizerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    profile_photo = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)

    class Meta:
        model = ClubOrganizer
        fields = [
            'id', 'user', 'phone_number', 'date_of_birth', 'address', 
            'profile_photo', 'designation_in_club', 'bio', 
            'profile_completed', 'profile_completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['profile_completed_at', 'created_at', 'updated_at']
        
    def to_internal_value(self, data):
        """
        Allow username / first_name / last_name to be passed at root level.
        """
        user_fields = ['username', 'first_name', 'last_name']

        data = data.copy()

        user_data = {}

        for f in user_fields:
            if f in data:
                value = data.get(f)          # returns the FIRST value as a string
                user_data[f] = value
                data.pop(f)

        ret = super().to_internal_value(data)

        if user_data:
            ret['user'] = user_data

        return ret

    def update(self, instance, validated_data):
        # Extract nested user updates from sourced fields
        user_data = validated_data.pop("user", {})  # comes from source='user.*'
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Check profile completion
        required_fields = [
            'phone_number', 'date_of_birth', 'address', 'designation_in_club'
        ]
        if all(getattr(instance, field, None) for field in required_fields) and not instance.profile_completed:
            instance.profile_completed = True
            instance.profile_completed_at = now()
            instance.save()

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    # Student-specific fields
    usn = serializers.CharField(required=False, allow_blank=True)
    semester = serializers.IntegerField(required=False)
    department = serializers.CharField(required=False, allow_blank=True)
    admission_type = serializers.ChoiceField(choices=Student.ADMISSION_TYPE_CHOICES, required=False)

    # Mentor-specific fields
    employee_id = serializers.CharField(required=False, allow_blank=True)
    designation = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name',
            'user_type', 'usn', 'semester', 'department', 'employee_id', 'designation', 'admission_type'
        ]
    
    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords do not match."})

        request = self.context.get("request")
        user_type = data.get("user_type")

        # Validate email domain
        email = data.get("email")
        if email:
            is_valid, error_msg = validate_email_domain(email, user_type)
            if not is_valid:
                raise serializers.ValidationError({"email": error_msg})

        if user_type == "student":
            usn = data.get("usn") or (request.data.get("usn") if request else None)
            dept = data.get("department") or (request.data.get("department") if request else None)
            sem = data.get("semester") or (request.data.get("semester") if request else None)

            if not usn:
                raise serializers.ValidationError({"usn": "USN is required for student registration."})

            # Validate USN format and branch consistency
            if dept:
                is_valid, error_msg, _ = validate_usn_format(usn, dept)
                if not is_valid:
                    raise serializers.ValidationError({"usn": error_msg})

            if Student.objects.filter(usn=usn).exists():
                raise serializers.ValidationError({"usn": "This USN is already registered."})

            if sem and (int(sem) < 1 or int(sem) > 8):
                raise serializers.ValidationError({"semester": "Semester must be between 1 and 8."})

        elif user_type == "mentor":
            emp_id = data.get("employee_id") or (request.data.get("employee_id") if request else None)
            dept = data.get("department") or (request.data.get("department") if request else None)
            desig = data.get("designation") or (request.data.get("designation") if request else None)

            if not emp_id:
                raise serializers.ValidationError({"employee_id": "Employee ID is required for mentor registration."})

            # Validate Employee ID format and branch consistency
            if dept:
                is_valid, error_msg = validate_employee_id_format(emp_id, dept)
                if not is_valid:
                    raise serializers.ValidationError({"employee_id": error_msg})

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
        admission_type = validated_data.pop('admission_type', None)
        
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
            # Determine admission type from USN validation
            admission_type = 'regular'  # Default
            if usn and department:
                _, _, admission_type = validate_usn_format(usn, department)

            Student.objects.create(
                user=user,
                usn=usn or '',
                department=department or '',
                semester=int(semester) if semester else 1,
                admission_type=admission_type
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
    name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            "id", "user_details", "name", "usn", "department", "semester", "admission_type",
            "phone_number", "date_of_birth", "address", "profile_photo",
            "emergency_contact_name", "emergency_contact_phone"
        ]

    def get_name(self, obj):
        """Return full name as a single field for easier access"""
        return obj.user.get_full_name() or obj.user.username
        
        
class MentorSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Mentor
        fields = [
            "id", "user_details", "employee_id", "department", "phone_number", 
            "profile_photo"
        ]


class ClubOrganizerSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    club_name = serializers.CharField(source='club.name', read_only=True)

    class Meta:
        model = ClubOrganizer
        fields = [
            "id", "user_details", "club_name", "phone_number", "profile_photo"
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
    aicte_category_name = serializers.CharField(source='aicte_category.name', read_only=True, allow_null=True)
    primary_hall_name = serializers.CharField(source='primary_hall.name', read_only=True, allow_null=True)
    secondary_hall_name = serializers.CharField(source='secondary_hall.name', read_only=True, allow_null=True)
    assigned_hall_name = serializers.CharField(source='assigned_hall.name', read_only=True, allow_null=True)
    club = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'club', 'name', 'description', 'event_date', 'end_date',
            'start_time', 'end_time', 'max_participants', 'status',
            'needsVenueCampus', 'awardsAictePoints',
            'aicte_category', 'aicte_category_name', 'points_awarded',
            'primary_hall', 'primary_hall_name', 'secondary_hall', 'secondary_hall_name',
            'assigned_hall', 'assigned_hall_name', 'hall_assigned_at',
            'created_at', 'updated_at', 'created_by', 'created_by_username',
            'registrations'
        ]
        read_only_fields = ['created_at', 'updated_at', 'assigned_hall', 'hall_assigned_at']


class StudentEventSerializer(serializers.ModelSerializer):
    registrations = EventRegistrationSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    aicte_category_name = serializers.CharField(source='aicte_category.name', read_only=True, allow_null=True)
    primary_hall_name = serializers.CharField(source='primary_hall.name', read_only=True, allow_null=True)
    secondary_hall_name = serializers.CharField(source='secondary_hall.name', read_only=True, allow_null=True)
    assigned_hall_name = serializers.CharField(source='assigned_hall.name', read_only=True, allow_null=True)
    registration_status = serializers.SerializerMethodField()
    club = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_registration_status(self, obj):
        """Get registration status for the current user"""
        request = self.context.get('request')
        if request and hasattr(request.user, 'student_profile'):
            registration = obj.registrations.filter(student=request.user.student_profile).first()
            return registration.status if registration else None
        return None

    class Meta:
        model = Event
        fields = [
            'id', 'club', 'name', 'description', 'event_date', 'end_date',
            'start_time', 'end_time', 'max_participants', 'status',
            'needsVenueCampus', 'awardsAictePoints',
            'aicte_category', 'aicte_category_name', 'points_awarded',
            'primary_hall', 'primary_hall_name', 'secondary_hall', 'secondary_hall_name',
            'assigned_hall', 'assigned_hall_name', 'hall_assigned_at',
            'created_at', 'updated_at', 'created_by', 'created_by_username',
            'registrations', 'registration_status'
        ]
        read_only_fields = ['created_at', 'updated_at', 'assigned_hall', 'hall_assigned_at']
    
    def validate(self, data):
        if data.get('end_date') and data.get('end_date') < data.get('event_date'):
            raise serializers.ValidationError("End date must be after or equal to start date")
        if data.get('aicte_category') and not data.get('points_awarded'):
            raise serializers.ValidationError("Points awarded must be specified when AICTE category is selected")
        # Validate minimum 80 hours for AICTE events (per VTU rules)
        if data.get('aicte_category'):
            # For multi-day events, validate total duration >= 80 hours
            if data.get('end_date'):
                # Multi-day event: calculate total hours
                from datetime import datetime, timedelta
                start_date = data.get('event_date')
                end_date = data.get('end_date')
                start_time = data.get('start_time', datetime.min.time())
                end_time = data.get('end_time', datetime.min.time())

                if start_date and end_date:
                    days = (end_date - start_date).days + 1
                    if days > 1:
                        # Multi-day: assume 8 hours per day minimum
                        if days < 10:  # 8 hours * 10 days = 80 hours minimum
                            raise serializers.ValidationError("AICTE events must be at least 80 hours (10 days) in duration")
                    else:
                        # Single day event
                        if start_time and end_time:
                            duration = (end_time.hour * 3600 + end_time.minute * 60) - (start_time.hour * 3600 + start_time.minute * 60)
                            if duration < 28800:  # 8 hours in seconds
                                raise serializers.ValidationError("Single-day AICTE events must be at least 8 hours in duration")
                        else:
                            raise serializers.ValidationError("Start and end time required for AICTE events")
            else:
                # Single day event validation
                start_time = data.get('start_time')
                end_time = data.get('end_time')
                if start_time and end_time:
                    duration = (end_time.hour * 3600 + end_time.minute * 60) - (start_time.hour * 3600 + start_time.minute * 60)
                    if duration < 28800:  # 8 hours minimum
                        raise serializers.ValidationError("AICTE events must be at least 80 hours in duration. Single-day events require minimum 8 hours.")
                else:
                    raise serializers.ValidationError("Start and end time required for AICTE events")
        return data


class CertificateTemplateSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = CertificateTemplate
        fields = ['id', 'name', 'template_file', 'created_by', 'created_by_username', 'created_at', 'updated_at', 'is_active', 'version']
        read_only_fields = ['created_at', 'updated_at']


class PrincipalSignatureSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True, allow_null=True)

    class Meta:
        model = PrincipalSignature
        fields = [
            'id', 'signature_image', 'uploaded_by', 'uploaded_by_username',
            'uploaded_at', 'updated_at', 'is_active', 'notes'
        ]
        read_only_fields = ['uploaded_at', 'updated_at']


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
    booked_by_username = serializers.CharField(source='booked_by.username', read_only=True)
    approved_by_username = serializers.CharField(source='approved_by.username', read_only=True, allow_null=True)
    event_name = serializers.CharField(source='event.name', read_only=True)
    event_club = serializers.CharField(source='event.club.name', read_only=True)
    booked_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = HallBooking
        fields = [
            'id', 'hall', 'hall_name', 'event', 'event_name', 'event_club',
            'booked_by', 'booked_by_username', 'booking_date', 'start_time', 'end_time',
            'booking_status', 'approved_by', 'approved_by_username', 'created_at',
            'updated_at', 'rejection_reason'
        ]
        read_only_fields = ['approved_by', 'created_at', 'updated_at']
    
    def validate(self, data):
        if not data.get('event'):
            raise serializers.ValidationError("Event is required for hall booking")
        if not data.get('hall'):
            raise serializers.ValidationError("Hall is required for booking")
        return data


class AICTECategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AICTECategory
        fields = '__all__'


class AICTEPointTransactionSerializer(serializers.ModelSerializer):
    student_usn = serializers.CharField(source='student.usn', read_only=True)
    student_name = serializers.SerializerMethodField()
    event_name = serializers.CharField(source='event.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    approved_by_username = serializers.CharField(source='approved_by.username', read_only=True, allow_null=True)

    def get_student_name(self, obj):
        return obj.student.user.get_full_name() or obj.student.user.username
    
    class Meta:
        model = AICTEPointTransaction
        fields = [
            'id', 'student', 'student_name', 'student_usn', 'event', 'event_name', 'category', 'category_name',
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


class UserNotificationPreferencesSerializer(serializers.ModelSerializer):
    """Serializer for user notification preferences"""
    class Meta:
        model = UserNotificationPreferences
        fields = [
            'id', 'user', 'email_enabled', 'email_event_registrations',
            'email_event_reminders', 'email_event_cancellations',
            'email_certificate_generation', 'email_aicte_points',
            'email_hall_bookings', 'in_app_enabled',
            'in_app_event_notifications', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AuditLogSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_username', 'action', 'timestamp']
        read_only_fields = ['timestamp']
