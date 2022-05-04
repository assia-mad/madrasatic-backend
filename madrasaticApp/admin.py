from django.contrib import admin
from .models import *

# Register your models here.
#to do
admin.site.register(Myuser)
admin.site.register(DeclarationComplementDemand)
admin.site.register(MDeclarationRejection)
@admin.register(MDeclaration)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('titre', 'id', 'etat', 'auteur')