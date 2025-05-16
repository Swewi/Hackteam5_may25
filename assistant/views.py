import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
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
        else:
            ai_response = "<div class='gemini-response'>Sorry, the assistant is not available right now. Please check the configuration.</div>"
            
        return JsonResponse({"response": ai_response})
        
    return render(request, "assistant/assistant.html")


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
        