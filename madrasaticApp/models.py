from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

# Create your models here.
#role choices
role_choices = [('Utilisateur','User'),
                ('Responsable','Responsable'),
                ('Admin','Admin'),
                ('Service','Service'),
                      ]
num_only = RegexValidator(r'^[0-9]*$','only numbers are allowed')
# madrasatic USER model
class Myuser(AbstractUser):    
    first_name = None
    last_name = None
    role = models.CharField(max_length=30 , choices=role_choices , default=role_choices[0])
    address = models.CharField(max_length=150, blank=True)
    tel = models.CharField(max_length=10,validators=[num_only])
    is_banned = models.BooleanField(default=False)
    img = models.ImageField(upload_to='profile_images/', max_length=100, blank = True , null = True , verbose_name='user_img')

# declaration model
class MDeclaration(models.Model):
    
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
# declaration complement rejection
class MDeclarationRejection(models.Model):
    responsable = models.ForeignKey(get_user_model(), related_name='declarations_rejections', on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    declaration = models.OneToOneField(MDeclaration, related_name='rejection', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
# declaration complement demand model
class DeclarationComplementDemand(models.Model):
    responsable = models.ForeignKey(get_user_model(), related_name='declarations_complement_demands',
                              on_delete=models.CASCADE)
    declaration = models.ForeignKey(MDeclaration, related_name='complement_demands', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

