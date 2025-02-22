from django.contrib import admin

from apps.blog.models import Blog, Category, Comment, Tag

# Register your models here.
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
