from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Create your models here.
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
    headline = models.CharField(max_length=255, blank=True, null=True)
    content = RichTextUploadingField()
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="blogs/")
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_author",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="blog_tags")
    view_count = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="blog_category",
    )

    def __str__(self):
        return f"{self.title}"

    @property
    def get_author_name(self):
        return self.author.profile.get_name


class Comment(models.Model):
    user_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="replies",
    )

    def __str__(self):
        return f"{self.user_name}"
