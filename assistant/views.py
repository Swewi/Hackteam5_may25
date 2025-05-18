import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
import re
from .models import Interaction
from notes.models import Note
import time

# Try to import Google libraries, but handle gracefully if not installed
try:
    import google.auth
    from google.auth.transport.requests import Request
    import google.generativeai as genai

    # Check if credentials file exists and load it
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and os.path.exists(credentials_path):
        # Load service account credentials
        credentials, project = google.auth.load_credentials_from_file(credentials_path)

        # Configure the genai library with the credentials
        genai.configure(credentials=credentials)
        GEMINI_AVAILABLE = True
    else:
        print("WARNING: Google credentials file not found at:", credentials_path)
        GEMINI_AVAILABLE = False
except ImportError:
    print(
        "WARNING: Google libraries not installed. Install with: pip install google-auth google-generativeai"
    )
    GEMINI_AVAILABLE = False


def get_gemini_response(question):
    """Sends a question to the Gemini API and returns the response."""
    if not GEMINI_AVAILABLE:
        return "Gemini API is not available. Please check your configuration."

    try:
        # Use the correct model name
        response = genai.GenerativeModel(
            "models/gemini-1.5-flash-002"
        ).generate_content(question)
        return response.text
    except Exception as e:
        return f"Error: {e}"


@csrf_exempt
def assistant_view(request):
    """Handles the assistant view and user interactions."""
    # If the user is not authenticated, redirect to the login page
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to use this feature.", status=403)

    if request.method == "POST":
        user_question = request.POST.get("question")

        if GEMINI_AVAILABLE:
            question_preamble = (
                "The user asking the question is not technically inclined. If it is a technical question, then format the answer in a way that is easy to understand. "
                "And if answering the question rerquires several steps, then break it down into smaller steps. "
                "And give the user step-by-step instructions. "
                "If the question is not technical, then answer it in a friendly and helpful manner. "
                "Here is what the user said: "
            )
            prompt = question_preamble + user_question
            ai_response = get_gemini_response(prompt)

            cleaned_ai_response = clean_ai_response(ai_response)
            # Save the interaction to the database
            Interaction.objects.create(
                question=user_question,
                answer=cleaned_ai_response,
                timestamp=time.time(),
                usr=request.user,
            )
            # Store the id of the interaction that has just been created in the session
            # If session['first_interaction_id'] == -1, it means that this is the first interaction
            if request.session["first_interaction_id"] == -1:
                # store the last interaction that belongs to the user in the request
                request.session["first_interaction_id"] = (
                    Interaction.objects.filter(usr=request.user)
                    .order_by("timestamp")
                    .last()
                    .id
                )
                print(
                    "First interaction id set to:",
                    request.session["first_interaction_id"],
                )
        else:
            ai_response = "<div class='gemini-response'>Sorry, the assistant is not available right now. Please check the configuration.</div>"

        return JsonResponse({"response": ai_response})

    if request.session["first_interaction_id"] == -1:
        # no interactions yet
        interactions = Interaction.objects.none()
    else:
        # Get all interactions starting with the id stored in the session's first_interaction_id
        # This is to avoid loading all interactions at once, which can be slow
        # and inefficient. Instead, we load them in chunks as the user scrolls.
        # The interaction must also belong to the user in the request
        interactions = Interaction.objects.filter(
            id__gte=request.session["first_interaction_id"],
            usr=request.user if request.user.is_authenticated else None,
        ).order_by("timestamp")

    return render(request, "assistant/assistant.html", {"history": interactions})


def clean_ai_response(text):
    # Remove triple backticks and optional language tags (like ```html)
    text = re.sub(r"^```[a-z]*\n?", "", text)
    text = re.sub(r"```$", "", text)

    # Strip HTML tags, so only plain text remains
    text = strip_tags(text)

    return text.strip()


# A view for saving the thread of interactions of the current session as a note
# The title of the note is passed in the POST request
@csrf_exempt
def save_conversation(request):
    """Saves the conversation as a note."""
    if request.method == "POST":
        title = request.POST.get("title")
        # Get all interactions that belong to the user in the request
        interactions = Interaction.objects.filter(
            id__gte=request.session["first_interaction_id"],
            usr=request.user if request.user.is_authenticated else None,
        ).order_by("timestamp")
        # Create a new note with the title and the interactions
        note = Note.objects.create(
            title=title,
            user=request.user,
            interaction_start_id=interactions.first(),
            interaction_end_id=interactions.last(),
        )

        return JsonResponse({"status": "success", "note_id": note.id})

    return JsonResponse({"status": "error", "message": "Invalid request."})


def list_available_models():
    """Lists all available Gemini models (for debugging)."""
    if not GEMINI_AVAILABLE:
        print("Gemini API is not available. Please check your configuration.")
        return

    try:
        models = genai.list_models()
        if models:
            print("Available models:")
            for model in models:
                print(f"{model}")
    except Exception as e:
        print(f"Error listing models: {e}")

def clear_chat_history(request):
    """Clears the chat history."""
    if request.method == "POST":
        # Clear the session variable
        request.session["first_interaction_id"] = -1
        return JsonResponse({"status": "success", "message": "Chat history cleared."})

    return JsonResponse({"status": "error", "message": "Invalid request."})