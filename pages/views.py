from django.shortcuts import render,redirect
from .models import Collab,Feature,Program,Highlight,Event,Member,SocialLink,SocialIcon,Feedback,Contact
from .forms import ContactForm

# Create your views here.
def home(request):
    context = {}

    collabs = Collab.objects.all()
    features = Feature.objects.all()
    programs = Program.objects.all()
    events = Event.objects.all()
    highlights = Highlight.objects.all()
    members = Member.objects.all()
    icons = SocialIcon.objects.all()
    member_social = {}
    feedbacks = Feedback.objects.all()
    contact_form = ContactForm()

    for member in members:
        social_links = SocialLink.objects.filter(member=member)

        member_social[member.name] = {
            "member" : member,
            "social_links" : social_links,
        }

    if request.method == "POST":
        contact = ContactForm(request.POST)
        if contact.is_valid():
            contact.save()
        return redirect("home")


    context = {
        "collabs" : collabs,
        "features" : features,
        "programs" : programs,
        "events" : events,
        "highlights" : highlights,
        "members" : member_social ,
        "feedbacks" : feedbacks,
        "contact_form" : contact_form
    }

    return render(request, "pages/index.html", context)
