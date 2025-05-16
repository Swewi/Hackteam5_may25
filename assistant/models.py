from django.db import models

# Create your models here.
class Interaction(models.Model):
    """Model to store user questions and AI responses."""
    id = models.AutoField(primary_key=True)
    usr = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.question