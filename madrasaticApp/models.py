from email.policy import default
from unicodedata import numeric
from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

role_choices = [('Utilisateur','User'),
                ('Responsable','Responsable'),
                ('Admin','Admin'),
                    
                    ]

num_only = RegexValidator(r'^[0-9]*$','only numbers are allowed')

class Myuser(AbstractUser):    
    first_name = None
    last_name = None
    role = models.CharField(max_length=30 , choices=role_choices , default=role_choices[0])
    address = models.CharField(max_length=150, blank=True)
    tel = models.CharField(max_length=10,validators=[num_only])
    is_banned = models.BooleanField(default=False)
    img = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,default='/madrasatic/media/defaultuser.png')
