
from posixpath import basename
from django.urls import path, re_path
from rest_framework import routers
from django.http import HttpResponse
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView , ConfirmEmailView
from dj_rest_auth.views import LoginView, LogoutView , PasswordResetView , PasswordResetConfirmView , PasswordChangeView
from .views import ManageUsersView , UpdateprofileView



router = routers.DefaultRouter()
router.register(r'manageusers', ManageUsersView , basename='manageusers')
router.register(r'updateprofile',UpdateprofileView , basename='updateprofile')

urlpatterns = [
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/',
         VerifyEmailView.as_view(), name='account_email_verification_sent'),
     re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
         VerifyEmailView.as_view(), name='account_confirm_email'),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-change/',PasswordChangeView.as_view()),
   
]
urlpatterns += router.urls
