from django.shortcuts import render
from .models import Note

# Render the notes app's main page
def notes_view(request):
    """Renders the notes app's main page."""
    # Get the user's notes
    user_notes = Note.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'notes/notes.html', {'notes': user_notes})
