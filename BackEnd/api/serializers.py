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
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            is_email_verified=False,
            email_verification_token=str(uuid.uuid4()),
        )
        user.verification_sent_at = now()
        user.save(update_fields=['verification_sent_at'])
        send_verification_email(user)
        return user


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
