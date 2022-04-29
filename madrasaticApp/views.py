from rest_framework import  viewsets
from .serializers import *
from .models import *
from rest_framework import permissions , mixins
from .permissions import AdminAuthenticationPermission , IsAuthenticatedAndOwner , ResponsableAuthenticationPermission
from .permissions import DeclarationUserWritePermission
from .pagination import CustomPagination
from rest_framework.filters import  OrderingFilter , SearchFilter 
from django_filters import rest_framework as filters 
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import JSONParser , MultiPartParser , FormParser

# manage users by Admin
class ManageUsersView(viewsets.ModelViewSet):
    queryset = Myuser.objects.all()
    serializer_class = ManageusersSerializer
    permission_classes = [permissions.IsAuthenticated, AdminAuthenticationPermission]
    parser_classes = [FormParser, JSONParser, MultiPartParser]
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
    
# update profile View
class UpdateprofileView(viewsets.GenericViewSet , mixins.UpdateModelMixin,mixins.RetrieveModelMixin):
    queryset = Myuser.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticatedAndOwner]
    parser_classes = [FormParser, JSONParser, MultiPartParser]

class DeclarationList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = MDeclaration.declarationpobjects.all()
    serializer_class = DeclarationSerializer

class SavedDeclarationList(generics.ListAPIView, DeclarationUserWritePermission):
    permission_classes = [DeclarationUserWritePermission]
    queryset = MDeclaration.declarationbobjects.all()
    serializer_class = DeclarationSerializer

# declaration non draft for responsable
class ResponsableDeclarationslist(viewsets.ModelViewSet):
    queryset = MDeclaration.objects.exclude(etat='brouillon')
    serializer_class = ResponsableDeclarationSerializer
    permission_classes = [ResponsableAuthenticationPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['titre', 'etat','auteur' ,'publiée']
    filterset_fields = ['titre', 'etat','auteur', 'publiée']
    search_fields = ['auteur__uid', 'titre', 'etat','publiée']
    ordering_fields = ['auteur', 'titre', 'etat','publiée']
# reject declaration view
class DeclarationRejectionView(generics.CreateAPIView, generics.ListAPIView):
    queryset = MDeclarationRejection.objects.all()
    serializer_class = DeclarationRejectionSerializer
    permission_classes = [ResponsableAuthenticationPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['responsable', 'declaration', 'created_on']
    filterset_fields = ['responsable', 'declaration', 'created_on']
    search_fields = ['responsable__id', 'declaration__id', 'created_on']
    ordering_fields = ['responsable', 'declaration', 'created_on']

# declaration complement demand View
class DeclarationComplementDemandView(generics.CreateAPIView , generics.ListAPIView):
    queryset = DeclarationComplementDemand.objects.all()
    serializer_class = DeclarationComplementDemandSerializer
    permission_classes = [ResponsableAuthenticationPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['responsable', 'declaration', 'created_on']
    filterset_fields = ['responsable', 'declaration', 'created_on']
    search_fields = ['responsable__uid', 'declaration__did', 'created_on']
    ordering_fields = ['responsable', 'declaration', 'created_on']
