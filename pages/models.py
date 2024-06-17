from django.db import models

# Create your models here.
class Collab(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="collabs/")

    def __str__(self):
        return f"{self.title}"

class Feature(models.Model):
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"{self.title}"

class Program(models.Model):
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"{self.title}"

class Event(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="events/")

    def __str__(self):
        return f"{self.title}"

class Highlight(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="highlights/")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class Member(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    description = models.TextField()
    profile_img = models.ImageField(upload_to="members/")

    def __str__(self):
        return f"{self.name}"

class SocialIcon(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class SocialLink(models.Model):
    link_url = models.URLField(max_length=255)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    icon = models.ForeignKey(SocialIcon, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.icon.name}"

class Feedback(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    quote = models.TextField()
    profile_img = models.ImageField(upload_to="feedbacks/")

    def __str__(self):
        return f"{self.name}"

class Contact(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    subject = models.CharField(max_length=255, blank=False, null=False)
    message = models.TextField(blank=False, null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

