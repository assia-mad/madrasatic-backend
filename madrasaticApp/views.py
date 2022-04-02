from urllib import request
from rest_framework import  viewsets
from .serializers import ManageusersSerializer, UpdateUsersByAdminSerializer , UpdateProfileSerializer
from .models import Myuser
from dj_rest_auth.views import PasswordResetConfirmView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import permissions , mixins
from .permissions import AdminAuthenticationPermission , IsAuthenticatedAndOwner

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