
from wsgiref.validate import validator
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import role_choices 


email_validator = RegexValidator(r'^[a-z]*+[.]+[a-z]*+[@]+[esi-sba.dz]$','utiliser un email valide')
class CustomRegisterSerializer(RegisterSerializer):
    address = serializers.CharField(max_length = 150)
    tel = serializers.CharField(max_length = 10 )
    email = serializers.EmailField()

    def validate_email(self, email):
        super().validate_email(email)
        domain = email.split('@')[1]
        domain_list = ["esi-sba.dz",]
        if domain not in domain_list:
            raise serializers.ValidationError("Please enter an Email Address with a valid domain")
        return email




