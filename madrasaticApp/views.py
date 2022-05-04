from rest_framework import  viewsets
from .serializers import *
from .models import *
from rest_framework import permissions , mixins
from .permissions import AdminAuthenticationPermission , IsAuthenticatedAndOwner , ResponsableAuthenticationPermission
from .permissions import DeclarationUserWritePermission
from .pagination import *
from rest_framework.filters import  OrderingFilter , SearchFilter 
from django_filters import rest_framework as filters 
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
import pusher
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
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = 'UpdatedeclarationByResponsable'
        return serializer_class
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

class ServiceDeclarationsView(generics.ListAPIView , generics.UpdateAPIView):
    queryset = MDeclaration.objects.filter(etat__in = ['en cours de traitement','traitée','non traitée'] )
    serializer_class = ServiceDeclarationsSerializer



# Pusher Beams AUTH
class BeamsAuthView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        from pusher_push_notifications import PushNotifications
        push_client = PushNotifications(
            instance_id='ab307d73-4586-4400-9add-179772d785bc',
            secret_key='5ED9A60B53DDAA7DF5B55E6A1B08ED5881289C1D2B6B039D04F78C277E5ECD02',
            )
        user_id = str(request.user.uid)
        beams_token = push_client.generate_token(user_id)      
        # content = {
        #     'user': request.user.first_name,
        #     'user_id': request.user.uid,
        #     'beams_token': beams_token,
        #     'auth': request.auth,
        # }
        return Response(beams_token)

class NotificationView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['id', 'title', 'body', 'user', 'responsable', 'service', 'created_on']
    filterset_fields = ['id', 'title', 'body', 'user', 'responsable', 'service', 'created_on']
    search_fields = ['id', 'title', 'body', 'user', 'responsable', 'service', 'created_on']
    ordering_fields = ['id', 'title', 'body', 'user', 'responsable', 'service', 'created_on']
    authentication_classes = []
    permission_classes = []
    pagination_class = NotificationCustomPagination


class PusherAuthView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    pusher_client = pusher.Pusher(
        app_id= settings.PUSHER_APP_ID,
        key= settings.PUSHER_KEY,
        secret= settings.PUSHER_SECRET,
        cluster= settings.PUSHER_CLUSTER
            )

    def get(self, request, format=None):
        channel_name = self.request.query_params.get('channel_name')
        socket_id = self.request.query_params.get('socket_id')

        auth = self.pusher_client.authenticate(
            channel = channel_name,
            socket_id = socket_id
            )
        
        return Response(auth)
    
    def post(self, request):
        channel_name = self.request.data['channel_name']
        socket_id = self.request.data['socket_id']

        auth = self.pusher_client.authenticate(
            channel = channel_name,
            socket_id = socket_id
            )
        
        return Response(auth)
