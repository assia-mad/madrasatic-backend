from django.contrib import admin
from .models import Myuser , MDeclaration

# Register your models here.
#to do
admin.site.register(Myuser)

@admin.register(MDeclaration)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('titre', 'id', 'etat', 'auteur')