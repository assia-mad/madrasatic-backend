
from django.contrib import admin
from django.urls import path , include 
from madrasaticApp import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('madrasatic/',include('madrasaticApp.urls')),
    
   
]
