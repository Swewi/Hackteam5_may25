from django.urls import path
from .views import notes_view
from .views import view_note

urlpatterns = [
    path('', notes_view, name='notes'),  # Render the notes app's main page
    path('view/<int:note_id>/', view_note, name='view_note'),  # Retrieve the conversation history in the selected note
]
