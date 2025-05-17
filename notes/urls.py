from django.urls import path
from .views import notes_view

urlpatterns = [
    path('', notes_view, name='notes'),  # Render the notes app's main page
]
