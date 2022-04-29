from rest_framework import permissions , authentication
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, BasePermission
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

#modification par l'auteur
class DeclarationUserWritePermission(BasePermission):
    message = 'Modifier une déclaration ne peut être fait que par son auteur.'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user

class ResponsableAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [authentication.BasicAuthentication, authentication.TokenAuthentication]
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and (user.role == 'Responsable') )