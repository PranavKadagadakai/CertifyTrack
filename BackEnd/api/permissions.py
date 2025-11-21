from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Permission class for admin users only"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'admin'

class IsClubAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'club_organizer'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'student'

class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'mentor'

class IsAdminOrReadOnly(BasePermission):
    """Allow admins full access, others read-only"""
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.user_type == 'admin'