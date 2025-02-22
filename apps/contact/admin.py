from django.contrib import admin

from apps.contact.models import Contact, SocialIcon, SocialLink, WebsiteMeta

# Register your models here.
admin.site.register(SocialIcon)
admin.site.register(SocialLink)
admin.site.register(WebsiteMeta)
admin.site.register(Contact)
