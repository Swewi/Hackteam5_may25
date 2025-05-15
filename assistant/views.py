import google.auth
from google.auth.transport.requests import Request
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

import os
from django.views.decorators.csrf import csrf_exempt
import time

# Load service account credentials
credentials, project = google.auth.load_credentials_from_file(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)

# Configure the genai library with the credentials
genai.configure(credentials=credentials)
"Error: {e}"


def get_gemini_response(question):
    """Sends a question to the Gemini API and returns the response."""
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
        question_preamp = (
            "The user asking the question is a 5-year-old child. Please send the response in html format inside a div element with class='gemini-response'. "
            "Here is what the user asked: "
        )
        user_question = request.POST.get("question")
        prompt = question_preamp + user_question
        # Add a delay to avoid rate limiting
        ai_response = get_gemini_response(prompt)
        return JsonResponse({"response": ai_response})
    return render(request, "assistant/assistant.html")


def list_available_models():
    try:
        models = genai.list_models()
        if models:
            print("Available models:")
            for model in models:
                print(f"{model}")
    except Exception as e:
        print(f"Error listing models: {e}")
