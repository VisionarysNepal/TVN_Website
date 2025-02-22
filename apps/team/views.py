from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from apps.team.models import Member


# Create your views here.
class TeamDetailView(DetailView):
    model = Member
    template_name = "team/team_detail.html"

    def get_object(self, queryset=None):
        qs = Member.objects.prefetch_related("works", "member_socials")
        return get_object_or_404(qs, slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        member = self.get_object()
        context["member"] = member
        context["works"] = member.works.all()
        context["social_links"] = member.member_socials.all()
        return context
