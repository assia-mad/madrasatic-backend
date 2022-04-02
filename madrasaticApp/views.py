from urllib import request
from rest_framework import  viewsets
from .serializers import ManageusersSerializer, UpdateUsersByAdminSerializer , UpdateProfileSerializer
from .models import Myuser
from dj_rest_auth.views import PasswordResetConfirmView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions , authentication , mixins

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
class ManageUsersView(viewsets.ModelViewSet):
    queryset = Myuser.objects.all()
    serializer_class = ManageusersSerializer
    permission_classes = (permissions.IsAuthenticated, AdminAuthenticationPermission)

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = UpdateUsersByAdminSerializer
        return serializer_class

class RequestPasswordResetEmail(PasswordResetConfirmView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'password_reset_confirm.html'
    

# update profile
class UpdateprofileView(viewsets.GenericViewSet , mixins.UpdateModelMixin,mixins.RetrieveModelMixin):
    queryset = Myuser.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticatedAndOwner]