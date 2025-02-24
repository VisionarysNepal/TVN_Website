from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.blog.models import Tag


# Create your models here.
class Profile(models.Model):
    profile_image = models.ImageField(blank=True, null=True, upload_to="profiles/")
    bio = models.CharField(max_length=200)
    member = models.OneToOneField(
        "team.Member", on_delete=models.SET_NULL, null=True, blank=True
    )
    author = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify("profile")
            if self.member:
                self.slug = slugify(self.member)
            elif self.author:
                self.slug = slugify(self.author)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.member:
            return f"{self.member}'s profile"
        else:
            return f"{self.author}'s profile"

    @property
    def get_name(self):
        if self.member:
            return self.member.name
        else:
            if self.author.first_name:
                return f"{self.author.first_name} {self.author.last_name}"
            return self.author


class Member(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    description = models.TextField()
    cv = models.FileField(
        upload_to="members/cv/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"


class Work(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    year = models.DateField(default=timezone.localdate)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    member = models.ForeignKey(
        Member, on_delete=models.SET_NULL, null=True, blank=True, related_name="works"
    )

    def __str__(self):
        return f"{self.member.name} - {self.title} work"
