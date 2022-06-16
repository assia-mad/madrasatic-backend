from datetime import date, datetime
from signal import signal
from unicodedata import category
from pyparsing import And
from rest_framework import  viewsets
from .serializers import *
from .models import *
from rest_framework import permissions , mixins
from .permissions import AdminAuthenticationPermission , IsAuthenticatedAndOwner , ResponsableAuthenticationPermission, ServiceAuthenticationPermission
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
from django.shortcuts import get_object_or_404

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

# list of services
class ServiceListView(viewsets.ModelViewSet):
    queryset = Myuser.objects.filter( role = 'Service')
    serializer_class = ServiceSerializer
    pagination_class = None

#categories
class CategorieView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
#localisation
class LocalisationView(viewsets.ModelViewSet):
    queryset = Identification.objects.all()
    serializer_class = LocalisationSerializer
    pagination_class = None

#endroit
class EndroitView(viewsets.ModelViewSet):
    queryset = Endroit.objects.all()
    serializer_class = EndroitSerializer
    pagination_class = None

#bloc
class BlocView(viewsets.ModelViewSet):
    queryset = Bloc.objects.all()
    serializer_class = BlocSerializer
    pagination_class = None

#site
class SiteView(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    pagination_class = None

#liste des déclarations
class DeclarationList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = MDeclaration.objects.filter(etat='publiée')
    serializer_class = DeclarationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    filterset_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    search_fields = ['auteur__id', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    ordering_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    
#Création d'une déclaration
class DeclarationCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeclarationSerializer 
    parser_classes = [FormParser, JSONParser, MultiPartParser] 

#Déclarations enregistrées comme brouillon
class SavedDeclarationList(generics.ListAPIView):

    permission_classes = [IsAuthenticatedAndOwner]
    queryset = MDeclaration.objects.filter(etat='brouillon')
    serializer_class = DeclarationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    filterset_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    search_fields = ['auteur__id', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    ordering_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']

    #afficher seulement les brouillon faits par l'utilisateur en question
    def get_queryset(self):

        user = self.request.user
        return MDeclaration.objects.filter(auteur=user, etat='brouillon')

#Modifier un brouillon
class EditDeclaration(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeclarationSerializer
    queryset = MDeclaration.objects.all()
   
#Supprimer un brouillon
class DeleteDeclaration(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeclarationSerializer
    queryset = MDeclaration.objects.all() 

    def get_queryset(self):
        user = self.request.user
        return MDeclaration.objects.filter(auteur=user, etat='brouillon')


# declaration non draft for responsable
class ResponsableDeclarationslist(viewsets.ModelViewSet):

    queryset = MDeclaration.objects.exclude(etat='brouillon')
    serializer_class = ResponsableDeclarationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    filterset_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    search_fields = ['auteur__id', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    ordering_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = UpdatedeclarationByResponsable
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

class ServiceDeclarationsView(viewsets.ModelViewSet):
    serializer_class = ServiceDeclarationsSerializer
    permission_classes = [ServiceAuthenticationPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    filterset_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    search_fields = ['auteur__id', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    ordering_fields = ['auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat']
    
    def get_queryset(self):
        return MDeclaration.objects.filter(etat__in = ['en cours de traitement','traitée','non traitée'],catégorie__service = self.request.user)



# Pusher Beams AUTH
class BeamsAuthView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        from pusher_push_notifications import PushNotifications
        push_client = PushNotifications(
            instance_id='07664670-9ac3-47fb-b92f-1f54942f1d20',
            secret_key='77D48F249287CAEFC9700E12DA6C8984DC2F37972BCBEE62D45528ECDE3F5B65',
            )
        user_id = str(request.user.id)
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

class DraftReportsView(viewsets.ModelViewSet):
    queryset = Report.objects.filter(status = 'brouillon')
    serializer_class = ReportSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['title','desc','service','declaration','status','created_on','validated_at','modified_at']
    filterset_fields = ['title','desc','service','declaration','status','created_on','validated_at','modified_at']
    search_fields = ['title','desc','service','declaration','status','created_on','validated_at','modified_at']
    ordering_fields = ['title','desc','service','declaration','status','created_on','validated_at','modified_at']

class ReportsView(viewsets.ModelViewSet):
    queryset = Report.objects.exclude(status = 'brouillon')
    serializer_class = ReportSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['title','desc','service','declaration','status','created_on','validated_at','modified_at']
    filterset_fields = ['title','desc','service','declaration','status','created_on','validated_at','modified_at']
    search_fields = ['title','desc','service','declaration','status','created_on','validated_at','modified_at']
    ordering_fields = ['title','desc','service','declaration','status','created_on','validated_at','modified_at']

class ReportRejectionView(generics.CreateAPIView, generics.ListAPIView):  
    queryset = ReportRejection.objects.all()
    serializer_class =  ReportRejectionSerializer
    #permission_classes = [ResponsableAuthenticationPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['responsable', 'report', 'created_on']
    filterset_fields = ['responsable', 'report', 'created_on']
    search_fields = ['responsable__id', 'report__id', 'created_on']
    ordering_fields = ['responsable', 'report', 'created_on']

class ReportComplementDemandView(generics.CreateAPIView , generics.ListAPIView):
    queryset = ReportComplementdemand.objects.all()
    serializer_class = ReportComplementDemandSerializer
    #permission_classes = [ResponsableAuthenticationPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['responsable', 'report', 'created_on']
    filterset_fields = ['responsable', 'report', 'created_on']
    search_fields = ['responsable__id', 'report__id', 'created_on']
    ordering_fields = ['responsable', 'report', 'created_on']


#liste des annonces d'un annonceur
class AnnonceurList(generics.ListAPIView):

    permission_classes = [IsAuthenticatedAndOwner]
    queryset = AnnonceModel.objects.filter(etat='publiée')
    serializer_class = AnnonceSerializer

    #afficher seulement les annonces faites par l'annonceur en question
    def get_queryset(self):
        user = self.request.user
        return AnnonceModel.objects.filter(auteur=user, etat='Publiée')


#liste des annonces
class AnnonceList(generics.ListAPIView):
    current = datetime.now()
    permission_classes = [permissions.IsAuthenticated]
    queryset = AnnonceModel.objects.filter(etat='publiée', datedebut__lte = current ,dateFin__gt = current )
    serializer_class = AnnonceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['auteur', 'objet','datedebut', 'pubDate','dateFin', 'etat']
    filterset_fields = ['auteur', 'objet','datedebut', 'pubDate','dateFin', 'etat']
    search_fields = ['auteur__id', 'objet','datedebut', 'pubDate','dateFin', 'etat']
    ordering_fields = ['auteur', 'objet', 'datedebut','pubDate','dateFin', 'etat']


#Création d'une annonce
class AnnonceCreate(generics.CreateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnnonceSerializer 
    parser_classes = [FormParser, JSONParser, MultiPartParser] 

#Annonces enregistrées comme brouillon
class SavedAnnonceList(generics.ListAPIView):

    permission_classes = [IsAuthenticatedAndOwner]
    queryset = AnnonceModel.objects.filter(etat='brouillon')
    serializer_class = AnnonceSerializer

    #afficher seulement les brouillon faits par l'annonceur en question
    def get_queryset(self):

        user = self.request.user
        return AnnonceModel.objects.filter(auteur=user, etat='brouillon')

#Modifier un brouillon
class EditAnnonce(generics.RetrieveUpdateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnnonceSerializer
    queryset = AnnonceModel.objects.all()

    def get_queryset(self):
        user = self.request.user
        return AnnonceModel.objects.filter(auteur=user, etat='brouillon')

#Supprimer un brouillon
class DeleteAnnonce(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnnonceSerializer
    queryset = AnnonceModel.objects.all() 

    def get_queryset(self):
        user = self.request.user
        return AnnonceModel.objects.filter(auteur=user, etat='brouillon')

class AnnonceRejectionView(generics.CreateAPIView, generics.ListAPIView):  
    queryset = AnnonceRejection.objects.all()
    serializer_class =  AnnonceRejectionSerializer
    #permission_classes = [ResponsableAuthenticationPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['responsable', 'annonce', 'created_on']
    filterset_fields = ['responsable', 'annonce', 'created_on']
    search_fields = ['responsable__id', 'annonce__id', 'created_on']
    ordering_fields = ['responsable', 'annonce', 'created_on']

class UserStatisticsView(APIView):
    def get(self, request, format=None):
        ''' Users Statistics '''
        all_users_count = Myuser.objects.all().count() # all current users
        active_users_count = Myuser.objects.filter(is_active=True).exclude(role='Admin').count() #  active users exclude Admins
        all_signaler_count = Myuser.objects.filter(role = "('Utilisateur', 'User')").count() + Myuser.objects.filter(role = "Utilisateur").count()# signalers
        current_services_count = Myuser.objects.filter(role="Service").count() # services

        data = {
            'all_users': all_users_count,
            'active_users': active_users_count,
            'signalers': all_signaler_count, 
            'current_services':  current_services_count,
            }

        return Response(data)

class DeclarationStatisticsView(APIView):
    def get(self, request, format=None):
        ''' Users Statistics '''
        urgence = dict()
        critique = dict()
        normal = dict()
        status = ["publiée","rejetée", "incompléte","traitée","en cours de traitement","non traitée"]
        for statu in status:
            urgence[statu] = MDeclaration.objects.filter(priorité =1 ).filter(etat = statu).count() # only parents
            critique[statu] = MDeclaration.objects.filter(priorité=2).filter(etat=statu).count()
            normal[statu] = MDeclaration.objects.filter(priorité=3).filter(etat=statu).count()
            
        data = {
            'urgence':urgence ,
            'critique': critique,
            'normal': normal,
        }
        return Response(data)