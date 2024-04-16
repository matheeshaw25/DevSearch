from django.contrib import admin
from django.urls import path, include

from django.conf import settings #have access to sttings.py to connect media root and media url
from django.conf.urls.static import static # helps to create a url for static files

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/',include('projects.urls')), #go to projects folder --> go to urls.py file
    path('',include('users.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #goto settings, grab the url and connect to media root
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #url path from static url to static root