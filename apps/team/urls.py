from django.urls import path

from apps.team.views import TeamDetailView

app_name = "team"
urlpatterns = [
    path("team/<slug:slug>/", TeamDetailView.as_view(), name="team"),
]
