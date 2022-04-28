from django.contrib import admin
from .models import Myuser
from . import models

# Register your models here.
#to do
admin.site.register(Myuser)

@admin.register(models.Declaration)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('titre', 'id', 'etat', 'auteur')