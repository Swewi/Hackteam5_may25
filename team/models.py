from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fiName = models.CharField(max_length=155)
    laName = models.CharField(max_length=155)
    email = models.CharField(max_length=250)
    image = CloudinaryField('image')
    bio = models.TextField(max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    