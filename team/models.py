from django.db import models
from django.urls import reverse

# Create your models here.

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200)
    photo = models.ImageField(
        upload_to='team_photos/',
        blank=True,
        null=True,
        help_text="Upload a square photo (600x600 works best)"
    )
    join_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Higher numbers appear first"
    )

    class Meta:
        ordering = ['-display_order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.role}"

    def get_absolute_url(self):
        return reverse('team:team')

    def github_username(self):
        """Extracts the username from GitHub URL"""
        if self.github_url:
            return self.github_url.split('/')[-1]
        return ""