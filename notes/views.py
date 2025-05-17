from django.shortcuts import render
from .models import Note
from assistant.models import Interaction

# Render the notes app's main page
def notes_view(request):
    """Renders the notes app's main page."""
    # Get the user's notes
    user_notes = Note.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'notes/notes.html', {'notes': user_notes})

# Retrive the conversation history in the selected note
def view_note(request, note_id):
    """Retrieves the conversation history in the selected note."""
    # Get the note object
    note = Note.objects.get(id=note_id)

    # Get the list of interactions in the note
    interactions = Interaction.objects.filter(
        usr=request.user,
        id__gte=note.interaction_start_id.id,
        id__lte=note.interaction_end_id.id
    ).order_by('timestamp')

    return render(request, 'notes/view_note.html', {'note': note, 'interactions': interactions})