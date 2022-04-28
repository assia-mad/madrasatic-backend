from email.policy import default
from imp import NullImporter
from unicodedata import numeric
from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


from django.utils import timezone
from django.conf import settings


class Declaration(models.Model):

    #selectionner et afficher seulement les déclarations publiées (pour tout le monde)
    class DeclarationPObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(etat='publiée')

    #selectionner et afficher seulement les déclarations enregistrées (la liste des brouillon pour l'utilisateur)
    class DeclarationBObjects(models.Manager):
        def get_object(self):
            return super().get_queryset().filter(etat='brouillon') 

    options = (
        ('brouillon', 'Brouillon'),
        ('publiée', 'Publiée'),
    )

    titre = models.CharField(max_length=250)
    objet = models.TextField(null=True)
    corps = models.TextField()
    publiée = models.DateTimeField(default=timezone.now)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_Declarations')
        #cascade: supprimer un  compte c'est supprimer toutes les déclarations faites par lui

    etat = models.CharField(max_length=10, choices=options, default='brouillon')
    objects = models.Manager()  # default manager
    declarationpobjects = DeclarationPObjects()  # custom manager
    declarationbobjects = DeclarationBObjects()  # custom manager

    class Meta:
        ordering = ('-publiée',) #ordre par date de déclaration

    def __str__(self):
        return self.titre




# Create your models here.

role_choices = [('Utilisateur','User'),
                ('Responsable','Responsable'),
                ('Admin','Admin'),
                ('Service','Service'),
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
