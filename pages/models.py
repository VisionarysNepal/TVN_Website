from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

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
    icon = models.ForeignKey(SocialIcon, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True, related_name="member")

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

class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(blank=True, null=True, upload_to="authors/")
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.author.username)
        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.author.first_name} {self.author.last_name}"


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        return super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} Tag"

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField()
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="blogs/")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="post")
    view_count = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    website = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Blog, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey("self", on_delete = models.DO_NOTHING, blank=True, null=True, related_name="replies")

    def __str__(self):
        return f"{self.user_name}"

class Subscribe(models.Model):
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} Newsletter"

class WebsiteMeta(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    about = models.TextField()

    def __str__(self):
        return "Website Meta"

#class Volunteer(models.Model):
#    email = models.EmailField(max_length=200)
#    full_name = models.CharField(max_length=255)
#    temporary_residence = models.CharField(max_length=255)
#    permanent_residence = models.CharField(max_length=255)
#    ph_number = models.IntegerField(max_length=10)

