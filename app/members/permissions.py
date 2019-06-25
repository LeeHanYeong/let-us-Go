from rest_framework import permissions


class IsUserSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
