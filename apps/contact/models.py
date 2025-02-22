from django.contrib.auth.models import User
from django.db import models

from apps.team.models import Member


# Create your models here.
class SocialIcon(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class SocialLink(models.Model):
    link_url = models.URLField(max_length=255)
    icon = models.ForeignKey(SocialIcon, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="user"
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="member_socials",
    )

    def __str__(self):
        if self.author:
            return f"{self.author}'s social link"
        else:
            return f"{self.member}'s social link"


class WebsiteMeta(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    about = models.TextField()
    ph_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Website Meta"


class Contact(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    subject = models.CharField(max_length=255, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
