from django.shortcuts import render,redirect
from .models import Collab,Goal,Program,Highlight,Event,Member,SocialLink,SocialIcon,Feedback,Contact,FeatureImage,Feature,Blog,Comment,Tag,User,WebsiteMeta,Category
from django.db.models import Count
from .forms import ContactForm,CommentForm, SubscribeForm
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    context = {}

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

    blogs = Blog.objects.all()
    top_blogs = Blog.objects.all().order_by("-view_count")[0:3]
    recent_blogs = Blog.objects.all().order_by("-last_updated")[0:3]

    member_social = {}
    feature_images = {}
    subscribe_message = None
    contact_message = None

    for feature in features:
        images = list(FeatureImage.objects.filter(feature=feature))
        feature_images[feature.title] = {
            "feature" : feature,
            "images" : images
        }


    for member in members:
        social_links = SocialLink.objects.filter(member=member)

        member_social[member.name] = {
            "member" : member,
            "social_links" : social_links,
        }


    context = {
        "collabs" : collabs,
        "goals" : goals,
        "programs" : programs,
        "events" : events,
        "highlights" : highlights,
        "members" : member_social ,
        "feedbacks" : feedbacks,
        "contact_form" : contact_form,
        "feature_images" : feature_images,
        "blogs" : blogs,
        "top_blogs" : top_blogs,
        "recent_blogs" : recent_blogs,
        "subscribe_form" : subscribe_form,
        "subscribe_message" : subscribe_message,
        "contact_message" : contact_message,
        "meta" : meta
    }

    if request.method == "POST":
        if request.POST.get('contact'):
            contact = ContactForm(request.POST)
            if contact.is_valid():
                contact.save()
                contact_message = "Thank Your For Contacting Us"
                contact_form = ContactForm()

        elif request.POST.get('newsletter'):
            subscribe_form = SubscribeForm(request.POST)
            if subscribe_form.is_valid:
                subscribe_form.save()
                subscribe_message = "Subscribed Successfully"
                request.session["is_subscribed"] = True
                subscribe_form = SubscribeForm()
        return redirect("home")

    return render(request, "pages/index.html", context)

def blogs(request):
    context = {}
    blogs = Blog.objects.all()
    page_num = request.GET.get("q")
    paginator = Paginator(blogs, 6)
    page_obj = paginator.get_page(page_num)

    context = {
        "blogs" : page_obj
    }

    return render(request, "pages/blogs.html", context)

def post_page(request, slug):
    context = {}
    post = Blog.objects.get(slug=slug)
    recent_blogs = Blog.objects.all().order_by("-last_updated")
    tags = Tag.objects.all()
    comments = Comment.objects.filter(post=post, parent=None)
    total_comments = comments.count()
    comment_form = CommentForm()
    author_socials = SocialLink.objects.filter(author=post.author)
    categories = Category.objects.all()

    category_dict = {}

    for category in categories:
        count = Blog.objects.filter(category=category).annotate(Count("category")).count()
        category_dict[category.name] = {
            "category" : category,
            "count" : count
        }

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            parent = None
            if request.POST.get("parent_id"):
                #save the reply
                parent_id = request.POST.get("parent_id")
                parent = Comment.objects.get(id=parent_id)
                if parent:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent
                    comment_reply.post = post
                    comment_reply.save()

            else:
                comment = comment_form.save(commit=False)
                post_id = request.POST.get('post_id')
                post = Blog.objects.get(id=post_id)
                comment.post = post
                comment.save()
            return redirect(reverse('post_page', kwargs={'slug' : slug}))

    if (post.view_count is None):
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()


    if request.GET:
        query = request.GET.get("q")
        blogs = Blog.objects.filter(title__icontains=query)
        print(blogs)

    context = {
        "post" : post,
        "comment_form" : comment_form,
        "comments" : comments,
        "total_comments": total_comments,
        "recent_blogs" : recent_blogs,
        "tags" : tags,
        "author_socials" : author_socials,
        "categories" : category_dict
    }

    return render(request, "pages/post_page.html", context)

def tag_page(request, slug):
    tags = Tag.objects.exclude(slug=slug)

    tag = Tag.objects.get(slug=slug)
    top_blogs = Blog.objects.filter(tags__in=[tag.id]).order_by("-view_count")[0:3]
    recent_blogs = Blog.objects.filter(tags__in=[tag.id]).order_by("-last_updated")[0:3]

    context = {
        "tag" : tag,
        "top_blogs" : top_blogs,
        "recent_blogs" : recent_blogs,
        "tags" : tags
    }

    return render(request, "pages/tag_page.html", context)

def author(request, slug):
    author = User.objects.get(profile__slug=slug)
    top_authors = User.objects.annotate(number=Count("blog")).order_by("-number")
    top_blogs = Blog.objects.filter(author__profile__slug=slug).order_by("-view_count")[0:3]
    recent_blogs = Blog.objects.filter(author__profile__slug=slug).order_by("-last_updated")[0:3]
    context = {
        "author" : author,
        "top_blogs" : top_blogs,
        "recent_blogs" : recent_blogs,
        "top_authors" : top_authors,
    }

    return render(request, "pages/author.html", context)

def about(request):
    context = {}
    member_social = {}
    social_links = None
    members = Member.objects.all()

    for member in members:
        social_links = SocialLink.objects.filter(member=member)

        member_social[member.name] = {
            "member" : member,
            "social_links" : social_links,
        }

    website_meta = None
    if WebsiteMeta.objects.all().exists():
        website_meta = WebsiteMeta.objects.all()[0]
    context = {
        "website_meta" : website_meta,
        "members" : member_social
    }

    return render(request, "pages/about.html", context)

def category_page(request, slug):
    categories = Category.objects.exclude(slug=slug)

    category = Category.objects.get(slug=slug)
    top_blogs = Blog.objects.filter(category__in=[category.id]).order_by("-view_count")[0:3]
    recent_blogs = Blog.objects.filter(category__in=[category.id]).order_by("-last_updated")[0:3]

    context = {
        "category" : category,
        "top_blogs" : top_blogs,
        "recent_blogs" : recent_blogs,
        "categories" : categories
    }

    return render(request, "pages/category_page.html", context)

def search(request):
    context = {}

    if request.GET.get("search"):
        query = request.GET.get("search")
        blogs = Blog.objects.filter(title__icontains=query)
        context = {
            "blogs" : blogs,
            "query" : query
        }

    return render(request, "pages/search.html", context)
