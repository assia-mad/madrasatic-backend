
from dataclasses import fields
import email
from email.policy import default
from telnetlib import LOGOUT
from dj_rest_auth.registration.serializers import RegisterSerializer 
from dj_rest_auth.serializers import LoginSerializer , PasswordResetSerializer
from rest_framework import serializers
from .models import Myuser, role_choices 
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
from dj_rest_auth.serializers import PasswordResetSerializer

class CustomPasswordResetSerializer(PasswordResetSerializer):
    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email':getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            # here I have set my desired template to be used
            # don't forget to add your templates directory in settings to be found
            
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField()
    password1 = serializers.CharField( write_only=True,
                                    required=True,
                                    style={'input_type': 'password', })
    password2 = serializers.CharField( write_only=True,
                                    required=True,
                                    style={'input_type': 'password', })
    def validate_email(self, email):
        super().validate_email(email)
        domain = email.split('@')[1]
        domain_list = ["esi-sba.dz",]
        if domain not in domain_list:
            raise serializers.ValidationError("Please enter an Email Address with a valid domain")
        return email

class CustomLoginSerializer(LoginSerializer):
    username = None


class ManageusersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    is_active = serializers.BooleanField( default=True)
    is_banned = serializers.BooleanField(default=False)
    role  = serializers.ChoiceField(choices=role_choices , default=role_choices[0])
    username = serializers.CharField()
    is_superuser = serializers.BooleanField(default=False)
    img = serializers.ImageField(default ='/madrasatic/media/defaultuser.png')

    def validate_email(self, email):
        domain = email.split('@')[1]
        domain_list = ["esi-sba.dz",]
        if domain not in domain_list:
            raise serializers.ValidationError("Please enter an Email Address with a valid domain")
        return email

    class Meta :
        model = Myuser
        fields = ['username','email','role','is_active','is_superuser','is_banned','img']

class UpdateUsersByAdminSerializer(serializers.Serializer):
    role  = serializers.ChoiceField(choices=role_choices , default=role_choices[0])
    is_active = serializers.BooleanField( default=True)
    is_banned = serializers.BooleanField(default=False)
    def update(self, instance, validated_data):
        if instance.role != validated_data.get('role') :
            subject = ' role changed'
            message = f'Hi {instance.username} your role has been changed please logout and login again to get your suitable interface http://127.0.0.1:8000/madrasatic/logout '
            from_email = settings.EMAIL_HOST_USER 
            recipient_list = [instance.email]
            send_mail(subject, message,from_email,recipient_list , fail_silently=False)
        if validated_data.get('role') == 'Admin' :
            instance.is_superuser = True
        instance.role = validated_data.get('role', instance.role)
            
        if instance.is_banned != validated_data.get('is_banned'):
            if validated_data.get('is_active') == True:
                account = 'has been activated'
            else :
                account = 'has been desactivated'
            subject = 'MadrasaTic account'
            message = f'Hi {instance.username} your account {account}'
            from_email = settings.EMAIL_HOST_USER 
            recipient_list = [instance.email]
            send_mail(subject, message,from_email,recipient_list , fail_silently=False)
              
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_banned = validated_data.get('is_banned', instance.is_banned)
        instance.save()
        return instance   



class UpdateProfileSerializer(serializers.ModelSerializer):  
    username = serializers.CharField(max_length = 150)
    img = serializers.ImageField(default = '/madrasatic/media/defaultuser.png')
    tel = serializers.CharField(max_length = 10)
    address = serializers.CharField(max_length = 150) 

    class Meta :
        model = Myuser
        fields = ['username','address','tel','img']
        lookup_field = 'uid'
    

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'id')