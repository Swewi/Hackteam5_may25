import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
import re
from .models import Interaction
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
    print("WARNING: Google libraries not installed. Install with: pip install google-auth google-generativeai")
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
    if request.method == "POST":
        user_question = request.POST.get("question")

        
        if GEMINI_AVAILABLE:
            question_preamp = (
                "The user asking the question is a 5-year-old child. Please send the response in html format inside a div element with class='gemini-response'. "
                "Here is what the user asked: "
            )
            prompt = question_preamp + user_question
            ai_response = get_gemini_response(prompt)

            cleaned_ai_response = clean_ai_response(ai_response)
            # Save the interaction to the database
            Interaction.objects.create(
                question=user_question,
                answer=cleaned_ai_response,
                timestamp=time.time(),
                usr=request.user if request.user.is_authenticated else None,
            )
        else:
            ai_response = "<div class='gemini-response'>Sorry, the assistant is not available right now. Please check the configuration.</div>"
            
        return JsonResponse({"response": ai_response})
    interactions = Interaction.objects.all().order_by("timestamp")
    return render(request, "assistant/assistant.html", {"history": interactions})

def clean_ai_response(text):
    # Remove triple backticks and optional language tags (like ```html)
    text = re.sub(r'^```[a-z]*\n?', '', text)
    text = re.sub(r'```$', '', text)

    # Strip HTML tags, so only plain text remains
    text = strip_tags(text)

    return text.strip()

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
        