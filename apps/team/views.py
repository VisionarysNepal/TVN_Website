from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from apps.team.models import Member


# Create your views here.
class TeamDetailView(DetailView):
    model = Member
    template_name = "team/team_detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Member.objects.prefetch_related("works"), slug=self.kwargs["slug"]
        )

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        member = self.get_object()
        context["member"] = member
        context["works"] = member.works.all()
        return context
