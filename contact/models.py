from django.db import models

# Create your models here.

class Contact(models.Model):

    """
    Model for contact form/email.
    """
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    message = models.TextField(max_length=500, blank=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
    