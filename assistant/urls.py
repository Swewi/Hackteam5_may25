from django.urls import path
from . import views

urlpatterns = [
    path('assistant/', views.assistant_view, name='assistant'),
    path('assistant/save-conversation/', views.save_conversation, name='save_conversation'),
]
