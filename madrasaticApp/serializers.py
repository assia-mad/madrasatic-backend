from dj_rest_auth.registration.serializers import RegisterSerializer 
from dj_rest_auth.serializers import LoginSerializer
from requests import request
from rest_framework import serializers
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from .notification_push import *
from dj_rest_auth.serializers import PasswordResetSerializer , UserDetailsSerializer 


class CustomRegisterSerializer(RegisterSerializer):

    email = serializers.EmailField()
    password1 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password', })
    password2 = serializers.CharField( write_only=True, required=True, style={'input_type': 'password', })
    
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
    img = serializers.ImageField()

    def validate_email(self, email):
        domain = email.split('@')[1]
        domain_list = ["esi-sba.dz",]
        if domain not in domain_list:
            raise serializers.ValidationError("Please enter an Email Address with a valid domain")
        return email

    class Meta :
        model = Myuser
        fields = ['id','username','email','role','is_active','is_superuser','is_banned','img']


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
            
        if instance.is_active != validated_data.get('is_active'):
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

#service serializer
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myuser
        fields = ['id','username','email','img','is_active']


class UpdateProfileSerializer(serializers.ModelSerializer):  

    username = serializers.CharField(max_length = 150)
    img = serializers.ImageField(allow_null=True)
    tel = serializers.CharField(max_length = 10)
    address = serializers.CharField(max_length = 150) 

    class Meta :
        model = Myuser
        fields = ['username','address','tel','img','email']
        read_only_fields = ['email']


class CustomUserDetailSerializer(UserDetailsSerializer):

    username = serializers.CharField(max_length = 150)
    img = serializers.ImageField(allow_null=True)
    tel = serializers.CharField(max_length = 10)
    role = serializers.ChoiceField(choices= role_choices)
    is_superuser  = serializers.BooleanField()
    is_active = serializers.BooleanField()
    address = serializers.CharField(max_length = 150) 

    class Meta :
        model = Myuser
        fields = ['id','username','email','address','tel','img','role','is_superuser', 'is_active']
        lookup_field = 'id'
        read_only_fields = ['email', 'id','role','is_active','is_superuser']

#category serialiser
class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Category
        fields = ['id','name','service','created_on']

#localisation serialiser
class LocalisationSerializer(serializers.ModelSerializer):
    class Meta :
        model = Identification
        fields = ['id','site', 'blocc', 'endroit', 'identification']

class EndroitSerializer(serializers.ModelSerializer):
    class Meta :
        model = Endroit
        fields = ['id', 'endroit']

class BlocSerializer(serializers.ModelSerializer):
    class Meta :
        model = Bloc
        fields = ['id', 'blocc']

class SiteSerializer(serializers.ModelSerializer):
    class Meta :
        model = Site
        fields = ['id', 'site']

class DeclarationSerializer(serializers.ModelSerializer):
    confirmée_par  = serializers.PrimaryKeyRelatedField(
        queryset= Myuser.objects.all(),
        many=True,
        required=False
    )
    signalée_par  = serializers.PrimaryKeyRelatedField(
        queryset= Myuser.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = MDeclaration
        fields = ('id', 'auteur', 'publiée','priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat', 'image','parent_declaration','confirmée_par','signalée_par')
    
class ResponsableDeclarationSerializer (serializers.ModelSerializer):
    confirmée_par  = serializers.PrimaryKeyRelatedField(
        queryset= Myuser.objects.all(),
        many=True,
        required=False
    )
    signalée_par  = serializers.PrimaryKeyRelatedField(
        queryset= Myuser.objects.all(),
        many=True,
        required=False
    )
    class Meta : 
        model = MDeclaration
        fields = ['id', 'auteur','publiée', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat', 'image','parent_declaration','confirmée_par','signalée_par']
        lookup_field = ['id']
        
    
# update just priority or service
class UpdatedeclarationByResponsable(serializers.ModelSerializer):
    class Meta :
        model = MDeclaration
        fields = ['id','etat','priorité','catégorie','parent_declaration','confirmée_par','signalée_par']
        lookup_field = ['id']   
          
class DeclarationRejectionSerializer(serializers.ModelSerializer):

    class Meta :
        model = MDeclarationRejection
        fields = ['id','responsable','reason','declaration','created_on']
        lookup_field = ['id']  
    def create(self, validated_data):
        declaration = validated_data['declaration']
        reason = validated_data['reason']
        user = declaration.auteur
        responsable = validated_data['responsable']
        title = 'Rejet de votre declaration'
        body = 'La déclaration : '+ declaration.objet +' a été rejeté par ' + responsable.username +''+ 'et la raison c`est: '+ reason
        instance = super().create(validated_data)
        instance.declaration.etat = 'rejetée'
        instance.declaration.save()
        # beams notification
        print(user.id)
        push_notify(user.id, responsable.id, title, body)
        # channels notification
        data = {
            'title': title,
            'body': body
        }
        channel = u'Declaration'
        event = u'Rejet'
        channels_notify(channel, event, data)
        return validated_data 
        
# Declaration complement demand serializer
class DeclarationComplementDemandSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeclarationComplementDemand
        fields = ['id', 'responsable', 'description', 'declaration', 'created_on']
        lookup_field = ['id']
    def create(self, validated_data):
        declaration = validated_data['declaration']
        reason = validated_data['description']
        user = declaration.auteur
        responsable = validated_data['responsable']
        title = 'Completer votre déclaration'
        body = ' Le responsable' + responsable.username +'vous demande de completer votre déclaration : '+ declaration.objet + ' '+ reason
        instance = super().create(validated_data)
        instance.declaration.etat = 'incompléte'
        instance.declaration.save()
        # beams notification
        print(user.id)
        push_notify(user.id, responsable.id, title, body)
        # channels notification
        data = {
            'title': title,
            'body': body
        }
        channel = u'Declaration'
        event = u'Demande complement'
        channels_notify(channel, event, data)
        return validated_data

#service Declarations
class ServiceDeclarationsSerializer(serializers.ModelSerializer):
    class Meta : 
        model = MDeclaration
        fields = ['id', 'auteur', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'etat', 'image','parent_declaration','confirmée_par','signalée_par']
        lookup_field = 'id'

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id','body', 'user', 'responsable', 'service', 'created_on']
        lookup_field = 'id'

class ReportSerializer(serializers.ModelSerializer):
    class Meta :
        model = Report
        fields = ['id','title','desc','service','declaration','status','created_on','validated_at','modified_at']
        lookup_field = 'id'

class ReportRejectionSerializer(serializers.ModelSerializer):
    class Meta :
        model = ReportRejection
        fields = ['id','responsable', 'report','reason','created_on']
        lookup_fields = 'id'

class ReportComplementDemandSerializer(serializers.ModelSerializer):
    class Meta :
        model = ReportComplementdemand
        fields = ['id','responsable', 'report','description','created_on']
        lookup_fields = 'id'

#Annonce serializer
class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnonceModel
        fields = ('id', 'auteur', 'objet', 'corps', 'pubDate', 'etat', 'image')
