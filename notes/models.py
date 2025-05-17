from django.db import models

from django.contrib.auth.models import User
from assistant.models import Interaction

class Note(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interaction_start_id = models.ForeignKey(Interaction, related_name='start_interaction', on_delete=models.CASCADE)
    interaction_end_id = models.ForeignKey(Interaction, related_name='end_interaction', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
