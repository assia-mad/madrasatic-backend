
from django.contrib import admin
from django.urls import path , include 
from madrasaticApp import urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('madrasatic/',include('madrasaticApp.urls')),
    
   
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
