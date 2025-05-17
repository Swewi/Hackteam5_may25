from django.urls import path
from .views import notes_view
from .views import view_note
from .views import delete_note

urlpatterns = [
    path('', notes_view, name='notes'),  # Render the notes app's main page
    path('view/<int:note_id>/', view_note, name='view_note'),  # Retrieve the conversation history in the selected note
    path('delete/<int:note_id>/', delete_note, name='delete_note'),  # Delete a note
]
