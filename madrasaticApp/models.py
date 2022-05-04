from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

#role choices
role_choices = [
    
    ('Utilisateur','User'),
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

    options = (

        ('brouillon', 'Brouillon'),
        ('publiée', 'Publiée'),

    )

    niveaux = (

        (1, 'Urgence'),
        (2, 'Etat critique'),
        (3, 'Etat normal'),

    )

    catégories = (

        ('higène', 'Higène'),
        ('entretien', 'Entretien'),
        ('santé', 'Santé'),
        ('sécurité', 'Sécurité'),
        ('technique', 'Technique'),
        ('objet perdu', 'Objet perdu'),
        ('autre', 'Autre'),

    )

    catégorie = models.CharField(max_length=50, choices=catégories, default='Autre')
    lieu = models.CharField(max_length=50, null = True)
    priorité = models.CharField(max_length=30, choices=niveaux, default='Etat normal')
    objet = models.TextField(null=True)
    corps = models.TextField(null=True)
    publiée = models.DateTimeField(default=timezone.now)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #cascade: supprimer un  compte c'est supprimer toutes les déclarations faites par lui
    etat = models.CharField(max_length=10, choices=options, default='brouillon')
    image = models.ImageField(upload_to='declaration_images/', null = True)

    objects = models.Manager()  # default manager

    class Meta:

        ordering = ('-publiée', '-priorité') #ordre par date de déclaration

    def __str__(self):

        return self.objet


# declaration complement rejection
class MDeclarationRejection(models.Model):

    responsable = models.ForeignKey(get_user_model(), related_name='declarations_rejections', on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    declaration = models.OneToOneField(MDeclaration, related_name='rejection', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


# declaration complement demand model
class DeclarationComplementDemand(models.Model):

    responsable = models.ForeignKey(get_user_model(), related_name='declarations_complement_demands', on_delete=models.CASCADE)
    declaration = models.ForeignKey(MDeclaration, related_name='complement_demands', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

