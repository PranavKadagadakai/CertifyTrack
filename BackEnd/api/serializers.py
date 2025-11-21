from rest_framework import serializers
from django.utils.timezone import now
import uuid

from .models import (
    User, Student, Mentor, Club, Event, EventRegistration, Certificate,
    Hall, HallBooking, AICTECategory, AICTEPointTransaction,
    Notification, AuditLog
)


def send_verification_email(user):
    """
    Stub to send email verification. Replace with real email backend in production.
    """
    print(f"[Email Verification] Sent verification email to {user.email} with token: {user.email_verification_token}")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'is_email_verified']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']
    
    def validate(self, data):
        request = self.context["request"]

        if data["user_type"] == "student":
            usn = request.data.get("usn")
            dept = request.data.get("department")
            sem = request.data.get("semester")

            if not usn:
                raise serializers.ValidationError({"usn": "USN is required."})

            if Student.objects.filter(usn=usn).exists():
                raise serializers.ValidationError({"usn": "USN already exists."})

            if sem and (int(sem) < 1 or int(sem) > 8):
                raise serializers.ValidationError({"semester": "Semester must be 1–8."})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Automatically create Student profile if user_type is student
        if user.user_type == 'student':
            Student.objects.create(
                user=user,
                usn=self.context['request'].data.get('usn'),
                department=self.context['request'].data.get('department', ''),
                semester=self.context['request'].data.get('semester', 1)
            )
        
        # Automatically create Mentor profile if user_type is mentor
        if user.user_type == "mentor":
            Mentor.objects.create(
                user=user,
                department=self.context["request"].data.get("department", "")
            )


        return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "usn", "department", "semester", "user"]


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'
        read_only_fields = ['file', 'file_hash', 'issue_date']


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'


class HallBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallBooking
        fields = '__all__'


class AICTECategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AICTECategory
        fields = '__all__'


class AICTEPointTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AICTEPointTransaction
        fields = '__all__'

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


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
