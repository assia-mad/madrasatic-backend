import imp
from urllib import request
from rest_framework import  viewsets
from .serializers import ManageusersSerializer, UpdateUsersByAdminSerializer , UpdateProfileSerializer
from .models import Myuser
from dj_rest_auth.views import PasswordResetConfirmView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions , mixins
from .permissions import AdminAuthenticationPermission , IsAuthenticatedAndOwner
from .pagination import CustomPagination
from rest_framework.filters import SearchFilter, OrderingFilter 
from django_filters.rest_framework import DjangoFilterBackend

class ManageUsersView(viewsets.ModelViewSet):
    queryset = Myuser.objects.all()
    serializer_class = ManageusersSerializer
    permission_classes = (permissions.IsAuthenticated, AdminAuthenticationPermission)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['username', 'email', 'tel','address','role', 'is_active', 'is_superuser']
    filterset_fields = ['username', 'email', 'tel','address','role', 'is_active', 'is_superuser']
    search_fields = ['username', 'email', 'tel','address','role', 'is_active', 'is_superuser']
    ordering_fields = ['username', 'email', 'tel','address','role', 'is_active', 'is_superuser']

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