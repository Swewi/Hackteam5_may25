import os
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
import re
from .models import Interaction
from notes.models import Note
import time
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

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
        logger.warning("Google credentials file not found at: %s", credentials_path)
        GEMINI_AVAILABLE = False
except ImportError:
    logger.warning(
        "Google libraries not installed. Install with: pip install google-auth google-generativeai"
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
        logger.error("Error getting Gemini response: %s", str(e))
        return f"Error: {e}"


@csrf_exempt
def assistant_view(request):
    """Handles the assistant view and user interactions."""
    # If the user is not authenticated, redirect to the login page
    if not request.user.is_authenticated:
        return HttpResponse("You must be logged in to use this feature.", status=403)

    # Initialize first_interaction_id in session if it doesn't exist
    if "first_interaction_id" not in request.session:
        request.session["first_interaction_id"] = -1

    if request.method == "POST":
        user_question = request.POST.get("question")
        if not user_question or user_question.strip() == "":
            return JsonResponse({"error": "Question cannot be empty"}, status=400)

        try:
            if GEMINI_AVAILABLE:
                question_preamble = (
                    "The user asking the question is not technically inclined. If it is a technical question, then format the answer in a way that is easy to understand. "
                    "And if answering the question requires several steps, then break it down into smaller steps. "
                    "And give the user step-by-step instructions. "
                    "If the question is not technical, then answer it in a friendly and helpful manner. "
                    "Here is what the user said: "
                )
                prompt = question_preamble + user_question
                ai_response = get_gemini_response(prompt)

                cleaned_ai_response = clean_ai_response(ai_response)
                # Save the interaction to the database
                interaction = Interaction.objects.create(
                    question=user_question,
                    answer=cleaned_ai_response,
                    timestamp=time.time(),
                    usr=request.user,
                )
                
                # Store the id of the interaction that has just been created in the session
                # If session['first_interaction_id'] == -1, it means that this is the first interaction
                if request.session["first_interaction_id"] == -1:
                    # store the last interaction that belongs to the user in the request
                    request.session["first_interaction_id"] = interaction.id
                    logger.info(
                        "First interaction id set to: %s", 
                        request.session["first_interaction_id"]
                    )
            else:
                ai_response = "Sorry, the assistant is not available right now. Please check the configuration."
                return JsonResponse({"response": ai_response, "error": "Gemini not available"}, status=503)

            return JsonResponse({"response": ai_response, "status": "success"})
            
        except Exception as e:
            logger.error("Error in assistant_view POST: %s", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    try:
        if request.session.get("first_interaction_id", -1) == -1:
            # no interactions yet
            interactions = Interaction.objects.none()
        else:
            # Get all interactions starting with the id stored in the session's first_interaction_id
            # This is to avoid loading all interactions at once, which can be slow
            # and inefficient. Instead, we load them in chunks as the user scrolls.
            # The interaction must also belong to the user in the request
            interactions = Interaction.objects.filter(
                id__gte=request.session["first_interaction_id"],
                usr=request.user,
            ).order_by("timestamp")

        return render(request, "assistant/assistant.html", {"history": interactions})
    except Exception as e:
        logger.error("Error in assistant_view GET: %s", str(e))
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


def clean_ai_response(text):
    """Clean the AI response by removing markdown code blocks and HTML tags."""
    try:
        # Remove triple backticks and optional language tags (like ```html)
        text = re.sub(r"^```[a-z]*\n?", "", text)
        text = re.sub(r"```$", "", text)

        # Strip HTML tags, so only plain text remains
        text = strip_tags(text)

        return text.strip()
    except Exception as e:
        logger.error("Error in clean_ai_response: %s", str(e))
        return text  # Return original text if cleaning fails


# A view for saving the thread of interactions of the current session as a note
# The title of the note is passed in the POST request
@csrf_exempt
def save_conversation(request):
    """Saves the conversation as a note."""
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required"}, status=403)

    if request.method == "POST":
        try:
            title = request.POST.get("title")
            if not title or title.strip() == "":
                return JsonResponse({"status": "error", "message": "Title cannot be empty"}, status=400)

            # Get the first_interaction_id from the session
            first_interaction_id = request.session.get("first_interaction_id", -1)
            if first_interaction_id == -1:
                return JsonResponse({"status": "error", "message": "No conversation to save"}, status=400)

            # Get all interactions that belong to the user in the request
            interactions = Interaction.objects.filter(
                id__gte=first_interaction_id,
                usr=request.user,
            ).order_by("timestamp")

            if not interactions.exists():
                return JsonResponse({"status": "error", "message": "No interactions found to save"}, status=400)

            # Create a new note with the title and the interactions
            note = Note.objects.create(
                title=title,
                user=request.user,
                interaction_start_id=interactions.first(),
                interaction_end_id=interactions.last(),
            )

            logger.info(f"Note created with ID: {note.id} for user: {request.user.username}")
            return JsonResponse({"status": "success", "note_id": note.id})
            
        except Exception as e:
            logger.error("Error in save_conversation: %s", str(e))
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def list_available_models():
    """Lists all available Gemini models (for debugging)."""
    if not GEMINI_AVAILABLE:
        logger.warning("Gemini API is not available. Please check your configuration.")
        return

    try:
        models = genai.list_models()
        if models:
            logger.info("Available models:")
            for model in models:
                logger.info(f"{model}")
    except Exception as e:
        logger.error(f"Error listing models: {e}")
