from django.shortcuts import render
from .models import Note
from assistant.models import Interaction

# Render the notes app's main page
def notes_view(request):
    """Renders the notes app's main page with optional filtering."""
    query = request.GET.get('q', '').strip()
    user_notes = Note.objects.filter(user=request.user).order_by('-created_at')

    if query:
        from django.db.models import Q
        matching_note_ids = set()
        for note in user_notes:
            title_match = query.lower() in note.title.lower()
            interactions = Interaction.objects.filter(
                usr=request.user,
                id__gte=note.interaction_start_id.id,
                id__lte=note.interaction_end_id.id
            ).filter(Q(question__icontains=query) | Q(answer__icontains=query))
            if title_match or interactions.exists():
                matching_note_ids.add(note.id)
        user_notes = user_notes.filter(id__in=matching_note_ids)

    return render(request, 'notes/notes.html', {'notes': user_notes, 'query': query})

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

# Delete a note
def delete_note(request, note_id):
    """Deletes a note."""
    # Get the note object
    note = Note.objects.get(id=note_id)
    # Check if the note belongs to the user
    if note.user != request.user:
        return render(request, 'notes/notes.html', {'error': 'You do not have permission to delete this note.'})
    # Delete the note
    note.delete()

    # Redirect to the notes view
    return render(request, 'notes/notes.html', {'message': 'Note deleted successfully.'})