from django.urls import path
from . import views

urlpatterns = [
    path('assistant/', views.assistant_view, name='assistant'),
]
