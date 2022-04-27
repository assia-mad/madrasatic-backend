from email.policy import default
from imp import NullImporter
from turtle import title
from unicodedata import numeric
from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
#role choices
role_choices = [('Utilisateur','User'),
                ('Responsable','Responsable'),
                ('Admin','Admin'),
                ('Service','Service'),
                      ]
# priority levels 
levels = [
        (1, 'critical'),
        (2, 'important'),
        (3, 'normal'),
        (4, 'low'),
    ]
# state choices
states = [
        ('draft', 'draft'),
        ('not_validated', 'not_validated'),
        ('lack_of_info', 'lack_of_info'),
        ('validated', 'validated'),
        ('refused', 'refused'),
        ('under_treatment', 'under_treatment'),
        ('treated', 'treated'),
        
    ]

num_only = RegexValidator(r'^[0-9]*$','only numbers are allowed')

class Myuser(AbstractUser):    
    first_name = None
    last_name = None
    role = models.CharField(max_length=30 , choices=role_choices , default=role_choices[0])
    address = models.CharField(max_length=150, blank=True)
    tel = models.CharField(max_length=10,validators=[num_only])
    is_banned = models.BooleanField(default=False)
    img = models.ImageField(upload_to='profile_images/', max_length=100, blank = True , null = True , verbose_name='user_img')

class Declaration(models.Model):
    user = models.ForeignKey(Myuser,related_name='user.declarations+', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description  = models.TextField()
    location = models.CharField(max_length=300)
    priority = models.CharField(max_length=200, choices=levels, default='normal')
    status = models.CharField(max_length=200, choices=states, default='not_validated')
    image = models.ImageField(upload_to='declaration_images/', max_length=100, blank = True , null = True , verbose_name='user_img')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    validated_at = models.DateTimeField(blank=True, null=True)
    