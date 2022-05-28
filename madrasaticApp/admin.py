from django.contrib import admin
from .models import *

# Register your models here.
#to do
admin.site.register(Myuser)
admin.site.register(DeclarationComplementDemand)
admin.site.register(MDeclarationRejection)
admin.site.register(Report)
admin.site.register(ReportComplementdemand)
@admin.register(MDeclaration)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'priorité', 'catégorie', 'objet', 'corps', 'lieu', 'image', 'auteur')
@admin.register(AnnonceModel)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'objet', 'corps', 'pubDate', 'dateFin' 'image', 'auteur')