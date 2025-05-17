from django.db import models

from django.contrib.auth.models import User
from assistant.models import Interaction

class Note(models.Model):
    """
    The class incapsulates a saved conversation between the user and the assistant.
    It contains the title of the conversation, the user who created it, and the start and end interactions.
    """

    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interaction_start_id = models.ForeignKey(Interaction, related_name='start_interaction', on_delete=models.CASCADE)
    interaction_end_id = models.ForeignKey(Interaction, related_name='end_interaction', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
