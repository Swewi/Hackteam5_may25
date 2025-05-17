from django.shortcuts import render

# Render the notes app's main page
def notes_view(request):
    """Renders the notes app's main page."""
    return render(request, 'notes/notes.html')
