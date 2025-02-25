import requests
from django.conf import settings
from django.db.models import Count
from django.http import JsonResponse
from django.views.generic import TemplateView

from apps.blog.models import Blog
from apps.contact.forms import ContactForm
from apps.home.forms import SubscribeForm
from apps.home.models import Collab, Event, Feature, Feedback, Goal, Highlight, Program
from apps.team.models import Member


# Create your views here.
class HomePageView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collabs = Collab.objects.all()
        goals = Goal.objects.all()
        programs = Program.objects.all()
        event_locations = Event.objects.values_list("location", flat=True).distinct()
        highlights = Highlight.objects.select_related("event")
        members = (
            Member.objects.select_related("profile")
            .prefetch_related("member_socials__icon")
            .order_by("order")
        )
        feedbacks = Feedback.objects.all()
        features = (
            Feature.objects.all()
            .prefetch_related("feature_images")
            .annotate(feature_images_count=Count("feature_images"))
        )

        contact_form = ContactForm()
        subscribe_form = SubscribeForm()

        all_blogs = Blog.objects.select_related("author__profile").prefetch_related(
            "category"
        )
        top_blogs = all_blogs.order_by("-view_count")[0:3]
        recent_blogs = all_blogs.order_by("-last_updated")[0:3]

        context.update(
            {
                "collabs": collabs,
                "goals": goals,
                "programs": programs,
                "features": features,
                "event_locations": event_locations,
                "highlights": highlights,
                "members": members,
                "feedbacks": feedbacks,
                "contact_form": contact_form,
                "blogs": all_blogs,
                "top_blogs": top_blogs,
                "recent_blogs": recent_blogs,
                "subscribe_form": subscribe_form,
            }
        )

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
                # request.session["is_subscribed"] = True
                return JsonResponse({"message": subscribe_message})
            else:
                return JsonResponse({"error": "Validation Error, Try Again..."})
        return JsonResponse({"error": "Invalid Form Type"})
