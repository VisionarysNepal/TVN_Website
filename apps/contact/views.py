from django.shortcuts import render

from apps.contact.models import SocialLink, WebsiteMeta
from apps.team.models import Member


# Create your views here.
def about(request):
    context = {}
    member_social = {}
    social_links = None
    members = Member.objects.all()

    for member in members:
        social_links = SocialLink.objects.filter(member=member)

        member_social[member.name] = {
            "member": member,
            "social_links": social_links,
        }

    website_meta = None
    if WebsiteMeta.objects.all().exists():
        website_meta = WebsiteMeta.objects.all()[0]
    context = {"website_meta": website_meta, "members": member_social}

    return render(request, "contact/about.html", context)
