from posixpath import basename
from django.urls import path, re_path
from rest_framework import routers
from django.http import HttpResponse
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView , ConfirmEmailView
from dj_rest_auth.views import UserDetailsView, LoginView, LogoutView , PasswordResetView , PasswordResetConfirmView , PasswordChangeView
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(

   openapi.Info(

      title="madrasatic API",
      default_version='v1',
      description="madrasatic is  a project to manage esi-sba's members declaration ",
      contact=openapi.Contact(email="madrasatic@gmail.com"),
      license=openapi.License(name="BSD License"),

   ),

   public=True,
   permission_classes=[permissions.AllowAny],

)

router = routers.DefaultRouter()
router.register(r'manageusers', ManageUsersView , basename='manageusers')
router.register(r'updateprofile',UpdateprofileView , basename='updateprofile')
router.register(r'responsable_declarations',ResponsableDeclarationslist, basename='declaration_view')
router.register(r'notifications', NotificationView)
router.register(r'categories',CategorieView)
router.register(r'service_declarations', ServiceDeclarationsView, basename='service_declarations')
router.register(r'services_list',ServiceListView, basename='service list')
router.register(r'draft_reports',DraftReportsView, basename='draft_reports')
router.register(r'reports',ReportsView, basename='reports')
router.register(r'lieux',LocalisationView)
router.register(r'endroits',EndroitView)
router.register(r'blocs',BlocView)
router.register(r'sites',SiteView)


urlpatterns = [

    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',VerifyEmailView.as_view(), name='account_confirm_email'),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-change/',PasswordChangeView.as_view()),
    path('user/', UserDetailsView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #selectionner les déclarations enregistrées comme brouillon
    path('saveddeclarationslist/', SavedDeclarationList.as_view()), 

    #selectionner toutes les déclarations publiées
    path('declarationslist/', DeclarationList.as_view()),

    # declaration rejection endpoint
    path('declaration_rejection/',DeclarationRejectionView.as_view()),

    #créer une déclaration
    path('declarationcreate/', DeclarationCreate.as_view()),

    #Modifier un brouillon
    path('declarationedit/<int:pk>/', EditDeclaration.as_view()),

    #Supprimer une déclaration
    path('declarationdelete/<int:pk>/', DeleteDeclaration.as_view()),

    # declaration complement demand endpoint
    path('declaration_complement_demand/',DeclarationComplementDemandView.as_view()),
    #report rejection
    path('report_rejection/',ReportRejectionView.as_view()),
    # report complement demand
    path('report_complement_demand/',ReportComplementDemandView.as_view()),
     # Beams
    path('beams_auth/', BeamsAuthView.as_view(), name='beams_auth'),
    # Pusher
    path('pusher/auth', PusherAuthView.as_view() , name='pusher_auth'),

      #selectionner les annonces enregistrées comme brouillon
   path('savedannonces/', SavedAnnonceList.as_view()), 

   #selectionner toutes les annonces publiées
   path('annonceslist/', AnnonceList.as_view()),

   #selectionner toutes les annonces publiées d'un annonceur
   path('mesannonces/', AnnonceurList.as_view()),

   #créer une annonce
   path('annoncecreate/', AnnonceCreate.as_view()),

   #Modifier un brouillon
   path('annonceedit/<int:pk>/', EditAnnonce.as_view()),

   #Supprimer une annonce
   path('annoncedelete/<int:pk>/', DeleteAnnonce.as_view()),
   #annonce rejection
   path('annonce_rejection/', AnnonceRejectionView.as_view()),
   #statistique
   path('declaration_stat/',DeclarationStatisticsView.as_view()),
   path('user_stat/',UserStatisticsView.as_view()),


]

urlpatterns += router.urls
