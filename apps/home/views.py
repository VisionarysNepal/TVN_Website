import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView

from apps.blog.models import Blog
from apps.contact.forms import ContactForm
from apps.contact.models import SocialIcon, SocialLink, WebsiteMeta
from apps.home.forms import SubscribeForm
from apps.home.models import (
    Collab,
    Event,
    Feature,
    FeatureImage,
    Feedback,
    Goal,
    Highlight,
    Program,
)
from apps.team.models import Member


# Create your views here.
class HomePageView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meta = None
        if WebsiteMeta.objects.all().exists():
            meta = WebsiteMeta.objects.all()[0]

        collabs = Collab.objects.all()
        goals = Goal.objects.all()
        programs = Program.objects.all()
        events = Event.objects.all()
        highlights = Highlight.objects.all()
        members = Member.objects.all()
        icons = SocialIcon.objects.all()
        feedbacks = Feedback.objects.all()
        features = Feature.objects.all()

        contact_form = ContactForm()
        subscribe_form = SubscribeForm()

        all_blogs = Blog.objects.all()
        top_blogs = Blog.objects.all().order_by("-view_count")[0:3]
        recent_blogs = Blog.objects.all().order_by("-last_updated")[0:3]

        member_social = {}
        feature_images = {}

        for feature in features:
            images = list(FeatureImage.objects.filter(feature=feature))
            feature_images[feature.title] = {"feature": feature, "images": images}

        for member in members:
            social_links = SocialLink.objects.filter(member=member)

            member_social[member.name] = {
                "member": member,
                "social_links": social_links,
            }

        context = {
            "collabs": collabs,
            "goals": goals,
            "programs": programs,
            "events": events,
            "highlights": highlights,
            "members": member_social,
            "feedbacks": feedbacks,
            "contact_form": contact_form,
            "feature_images": feature_images,
            "blogs": all_blogs,
            "top_blogs": top_blogs,
            "recent_blogs": recent_blogs,
            "subscribe_form": subscribe_form,
            "meta": meta,
        }

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        recaptcha = data.get("g-recaptcha-response")
        recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"

        verification_response = requests.post(
            url=recaptcha_verify_url,
            data={
                "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                "response": recaptcha,
            },
        ).json()

        if data.get("form_type") == "contact":
            contact = ContactForm(data)
            if contact.is_valid():
                if verification_response["success"]:
                    contact.save()
                    contact_message = "Thank You For Contacting Us"
                    return JsonResponse({"message": contact_message})
                else:
                    return JsonResponse({"error": "Captcha Verification Error"})
            else:
                return JsonResponse({"error": "Validation Error"})
        elif data.get("form_type") == "newsletter":
            subscribe_form = SubscribeForm(data)
            if subscribe_form.is_valid:
                subscribe_form.save()
                subscribe_message = "Subscribed Successfully"
                request.session["is_subscribed"] = True
                return JsonResponse({"message": subscribe_message})
            else:
                return JsonResponse({"error": "Validation Error"})
        return JsonResponse({"error": "Invalid Form Type"})
