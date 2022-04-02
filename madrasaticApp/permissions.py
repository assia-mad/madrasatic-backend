from rest_framework import permissions , authentication
#is authenticated and owner for profile so that just owner of profile can modify it
class IsAuthenticatedAndOwner(permissions.BasePermission):
    message = 'You must be the owner of this object.'
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj == request.user

# admin permission
class AdminAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [authentication.BasicAuthentication, authentication.TokenAuthentication]
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and user.is_superuser )