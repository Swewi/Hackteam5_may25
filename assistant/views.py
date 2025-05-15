import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(question):
    """Sends a question to the Gemini API and returns the response."""
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error: {e}"

@csrf_exempt
def assistant_view(request):
    if request.method == 'POST':
        user_question = request.POST.get('question')
        ai_response = get_gemini_response(user_question)
        return JsonResponse({'response': ai_response})
    return render(request, 'assistant/assistant.html')