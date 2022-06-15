from ast import Try
from datetime import date, datetime
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
    ('Président du club','Président du club'),
]
#rapport states
states = [
    ('brouillon', 'Brouillon'),
    ('publié', 'Publié'),
    ('validé','validé'),
    ('incomplet','incomplet'),
]


num_only = RegexValidator(r'^[0-9]*$','only numbers are allowed')
num_comma = RegexValidator(r'^[0-9]+(,[0-9]+)+$','num separated by comma')

# madrasatic USER model
class Myuser(AbstractUser):   
    first_name = None
    last_name = None
    role = models.CharField(max_length=30 , choices=role_choices , default=role_choices[0])
    address = models.CharField(max_length=150, blank=True)
    tel = models.CharField(max_length=10,validators=[num_only],blank=True)
    is_banned = models.BooleanField(default=False)
    img = models.ImageField(upload_to='profile_images/', max_length=100, blank = True , null = True , verbose_name='user_img')

# declaration category
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    service = models.ForeignKey(get_user_model(), related_name='service', on_delete=models.CASCADE, blank=True, null=True, default=None)
    created_on = models.DateTimeField(auto_now_add=True)

# localisation model
# site model
class Site(models.Model):
    
    site = models.CharField(max_length=100, null = True)

    def __str__(self):
        return self.site

# bloc model
class Bloc(models.Model):
    site = models.ForeignKey(Site,on_delete=models.CASCADE, null=True)
    blocc = models.CharField(max_length=100, null = True)

    def __str__(self):
        return self.blocc

#endroit model
class Endroit(models.Model):
    blocc = models.ForeignKey(Bloc,on_delete=models.CASCADE, null=True) 
    endroit = models.CharField(max_length=50, null = True)

    def __str__(self):
        return self.endroit

#identification model
class Identification(models.Model):
    endroit = models.ForeignKey(Endroit,on_delete=models.CASCADE, null=True)
    identification = models.CharField(max_length=100, null = True)

    def __str__(self):
        return self.identification

# declaration model
class MDeclaration(models.Model):

    options = (

        ('brouillon', 'Brouillon'),
        ('publiée', 'Publiée'),
        ('non traitée','non traitée'),
        ('en cours de traitement','en cours de traitement'),
        ('traitée','traitée'),
        ('rejetée','rejetée'),
        ('incompléte','incompléte'),

    )
    niveaux = (

        (1, 'Urgence'),
        (2, 'Etat critique'),
        (3, 'Etat normal'),

    )

    catégorie = models.ForeignKey(Category,related_name='declaration_categorie',on_delete=models.CASCADE, null=True,default=None)
    site = models.ForeignKey(Site, related_name='declaration_site',on_delete= models.CASCADE,null=True,default=None)
    bloc = models.ForeignKey(Bloc, related_name='declaration_bloc',on_delete= models.CASCADE,null=True,default=None)
    endroit = models.ForeignKey(Endroit, related_name='declaration_endroit_type',on_delete= models.CASCADE,null=True,default=None)
    lieu = models.ForeignKey(Identification, related_name='declaration_place',on_delete= models.CASCADE,null=True,default=None)
    priorité = models.CharField(max_length=30, choices=niveaux, default='Etat normal')
    objet = models.TextField(null=True)
    corps = models.TextField(null=True)
    publiée = models.DateTimeField(default=timezone.now)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #cascade: supprimer un  compte c'est supprimer toutes les déclarations faites par lui
    etat = models.CharField(max_length=100, choices=options, default='brouillon')
    image = models.ImageField(upload_to='declaration_images/', null = True)
    parent_declaration = models.ForeignKey('self', default=None, null=True, related_name='declaration.parent_declaration+', on_delete=models.CASCADE)
    confirmée_par = models.ManyToManyField(get_user_model(),related_name='users_who_confirmed' )
    signalée_par = models.ManyToManyField(get_user_model(),related_name='users_who_signaled')

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


# Notification model
class Notification(models.Model):
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    user = models.ForeignKey(get_user_model(), related_name='notification.user+', on_delete=models.CASCADE, blank=True, null=True)
    responsable = models.ForeignKey(get_user_model(), related_name='notification.responsable+', on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(get_user_model(), related_name='notification.service+', on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

#rapport 
class Report(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()
    service = models.ForeignKey(get_user_model(),related_name='reports', on_delete=models.CASCADE)
    declaration = models.OneToOneField(MDeclaration , related_name='report', on_delete= models.CASCADE)
    status = models.CharField(max_length=200, choices=states, default ='publié')
    image = models.ImageField(upload_to='report_images/', blank = True , null = True , verbose_name='report_image')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    validated_at = models.DateTimeField(blank=True, null=True)

# report rejection
class ReportRejection(models.Model):
    responsable = models.ForeignKey(get_user_model(), related_name='report_rejection', on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    report = models.OneToOneField(Report, related_name='rejection', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

class ReportComplementdemand(models.Model):
    responsable = models.ForeignKey(get_user_model(), related_name='reports_complement_demands', on_delete=models.CASCADE)
    report = models.ForeignKey(Report, related_name='complement_demands', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

# annonce model
class AnnonceModel(models.Model):

    options = (

        ('brouillon', 'Brouillon'),
        ('publiée', 'Publiée'),
        ('validé','validé'),
        ('rejeté','rejeté'),

    )

    objet = models.TextField(null=True)
    corps = models.TextField(null=True)
    pubDate = models.DateTimeField(auto_now_add=True)#creation date
    datedebut = models.DateField(default=datetime.now,blank=True, null=True) #start appear for users
    dateFin = models.DateField(blank=False , null=False) #stop appearing
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    etat = models.CharField(max_length=100, choices=options, default='brouillon')
    image = models.ImageField(upload_to='annonces_images/', null = True,blank = True)

    objects = models.Manager()

    class Meta:

        ordering = ('-pubDate',)
    def __str__(self):

        return self.objet
# annonce rejection
class AnnonceRejection(models.Model):
    responsable = models.ForeignKey(get_user_model(), related_name='annonce_rejection', on_delete=models.CASCADE)
    raison = models.CharField(max_length=200)
    annonce = models.OneToOneField(AnnonceModel, related_name='rejection', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
