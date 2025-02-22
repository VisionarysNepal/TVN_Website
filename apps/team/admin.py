from django.contrib import admin

from apps.team.models import Member, Profile, Work

# Register your models here.
admin.site.register(Profile)
admin.site.register(Member)
admin.site.register(Work)
