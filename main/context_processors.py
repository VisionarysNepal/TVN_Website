from apps.contact.models import WebsiteMeta


def website_meta(request):
    return {"website_meta": WebsiteMeta.objects.all().last()}
