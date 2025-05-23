"""
URL configuration for familyhack5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home.views import home
from django.conf import settings

urlpatterns = [
    path('', home, name='home'),
    path('baton/', include('baton.urls')),  # baton admin
    path('admin/', admin.site.urls),
    path('', include('assistant.urls')),  #  Include the 'assistant' app URLs
    path('accounts/', include('allauth.urls')),  # Add django-allauth URLs
    path('notes/', include('notes.urls')),  # Include the 'notes' app URLs
    path('team/', include('team.urls')),  # Include the 'team' app URLs
    path("contact/", include("contact.urls")), # Include the 'contact' app URLs
]

if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
