from django.contrib import admin

from apps.home.models import (
    Collab,
    Event,
    Feature,
    FeatureImage,
    Feedback,
    Goal,
    Highlight,
    Program,
    Subscribe,
)

# Register your models here.
admin.site.register(Collab)
admin.site.register(Goal)
admin.site.register(Program)
admin.site.register(Highlight)
admin.site.register(Event)
admin.site.register(Feature)
admin.site.register(FeatureImage)
admin.site.register(Subscribe)
admin.site.register(Feedback)
