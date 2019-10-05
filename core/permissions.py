from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        #if request.method in permissions.SAFE_METHODS:
        #     return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.userprofile.is_teacher:
            return True
        else:
            return False