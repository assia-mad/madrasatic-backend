from urllib import request
from rest_framework import  viewsets
from .serializers import ManageusersSerializer , UpdateUsersByAdminSerializer
from .models import Myuser
from rest_framework import permissions , authentication 

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
   