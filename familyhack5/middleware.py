class FirstInteractionIDMiddleware:
    """
    Middleware to set a 'first_interaction_id' in the session when a new session starts.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the session is new and 'first_interaction_id' is not already set
        if not request.session.session_key or 'first_interaction_id' not in request.session:
            request.session['first_interaction_id'] = -1

        response = self.get_response(request)
        return response