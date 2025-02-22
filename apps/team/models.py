from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.blog.models import Tag


# Create your models here.
class Profile(models.Model):
    profile_image = models.ImageField(blank=True, null=True, upload_to="profiles/")
    bio = models.CharField(max_length=200)
    social_link = models.ForeignKey(
        "contact.SocialLink", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        member = self.member
        return f"{member.name}'s Profile" if member else "Unlinked Profile"


class Member(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    cv = models.FileField(
        upload_to="members/cv/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        null=True,
        blank=True,
    )
    profile = models.OneToOneField(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Member, self).save(*args, **kwargs)

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
