from django.db import models


# Create your models here.
class Collab(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="collabs/")

    def __str__(self):
        return f"{self.title}"


class Goal(models.Model):
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


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    quote = models.TextField()
    profile_img = models.ImageField(upload_to="feedbacks/")

    def __str__(self):
        return f"{self.name}"


class Feature(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"


class FeatureImage(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="features/")

    def __str__(self):
        return f"{self.image}"


class Subscribe(models.Model):
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} Newsletter"


# class Volunteer(models.Model):
#    email = models.EmailField(max_length=200)
#    full_name = models.CharField(max_length=255)
#    temporary_residence = models.CharField(max_length=255)
#    permanent_residence = models.CharField(max_length=255)
#    ph_number = models.IntegerField(max_length=10)
