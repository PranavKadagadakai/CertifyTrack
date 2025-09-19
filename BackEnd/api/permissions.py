from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsClubAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'club'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'student'

class IsMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == 'mentor'