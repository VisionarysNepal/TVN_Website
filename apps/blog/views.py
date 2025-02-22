from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, TemplateView

from apps.blog.forms import CommentForm
from apps.blog.models import Blog, Category, Comment, Tag
from apps.contact.models import SocialLink


# Create your views here.
class BlogPageView(TemplateView):
    template_name = "blog/blogs.html"

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        blogs = Blog.objects.all().order_by("-view_count")
        page_num = self.request.GET.get("q")
        paginator = Paginator(blogs, 6)
        page_obj = paginator.get_page(page_num)

        context = {"blogs": page_obj}
        return context


class BlogDetailPageView(DetailView):
    model = Blog
    template_name = "blog/blog_detail.html"

    def get_object(self, queryset=None):
        qs = Blog.objects.annotate(
            total_comments=Count("comments", filter=Q(comments__parent=None))
        ).prefetch_related("comments")

        return get_object_or_404(qs, slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        blog_post = self.get_object()
        recent_blogs = Blog.objects.all().order_by("-last_updated")
        tags = Tag.objects.all()
        comments = Comment.objects.filter(post=blog_post, parent=None)
        comment_form = CommentForm()
        author_socials = SocialLink.objects.filter(author=blog_post.author)
        categories = Category.objects.all()

        category_dict = {}
        for category in categories:
            count = (
                Blog.objects.filter(category=category)
                .annotate(Count("category"))
                .count()
            )
            category_dict[category.name] = {"category": category, "count": count}

        if blog_post.view_count is None:
            blog_post.view_count = 1
        else:
            blog_post.view_count = blog_post.view_count + 1
        blog_post.save()

        if self.request.GET:
            query = self.request.GET.get("q")
            if query != "":
                blogs = Blog.objects.filter(title__icontains=query)

        context = {
            "post": blog_post,
            "comment_form": comment_form,
            "comments": comments,
            "recent_blogs": recent_blogs,
            "tags": tags,
            "author_socials": author_socials,
            "categories": category_dict,
        }

        return context

    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        blog_post = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            parent = None
            if request.POST.get("parent_id"):
                parent_id = request.POST.get("parent_id")
                parent = Comment.objects.get(id=parent_id)
                if parent:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent
                    comment_reply.post = blog_post
                    comment_reply.save()
                    return render(
                        request,
                        "blog/includes/comments.html",
                        {
                            "comments": Comment.objects.all(),
                        },
                    )
            else:
                comment = comment_form.save(commit=False)
                comment.post = blog_post
                comment.save()
                print(comment)
                return render(
                    request,
                    "blog/includes/comments.html",
                    {
                        "comments": Comment.objects.all(),
                    },
                )
        return JsonResponse({"error": "Invalid Form", "status": "500"})


def tag_page(request, slug):
    tags = Tag.objects.exclude(slug=slug)

    tag = Tag.objects.get(slug=slug)
    top_blogs = Blog.objects.filter(tags__in=[tag.id]).order_by("-view_count")[0:3]
    recent_blogs = Blog.objects.filter(tags__in=[tag.id]).order_by("-last_updated")[0:3]

    context = {
        "tag": tag,
        "top_blogs": top_blogs,
        "recent_blogs": recent_blogs,
        "tags": tags,
    }

    return render(request, "blog/tag_page.html", context)


def author(request, slug):
    author = User.objects.get(profile__slug=slug)
    top_authors = User.objects.annotate(number=Count("blog")).order_by("-number")
    top_blogs = Blog.objects.filter(author__profile__slug=slug).order_by("-view_count")[
        0:3
    ]
    recent_blogs = Blog.objects.filter(author__profile__slug=slug).order_by(
        "-last_updated"
    )[0:3]
    context = {
        "author": author,
        "top_blogs": top_blogs,
        "recent_blogs": recent_blogs,
        "top_authors": top_authors,
    }

    return render(request, "blog/author.html", context)


def category_page(request, slug):
    categories = Category.objects.exclude(slug=slug)

    category = Category.objects.get(slug=slug)
    top_blogs = Blog.objects.filter(category__in=[category.id]).order_by("-view_count")[
        0:3
    ]
    recent_blogs = Blog.objects.filter(category__in=[category.id]).order_by(
        "-last_updated"
    )[0:3]

    context = {
        "category": category,
        "top_blogs": top_blogs,
        "recent_blogs": recent_blogs,
        "categories": categories,
    }

    return render(request, "blog/category_page.html", context)


def search(request):
    context = {}

    if request.GET.get("search"):
        query = request.GET.get("search")
        blogs = Blog.objects.filter(title__icontains=query)
        context = {"blogs": blogs, "query": query}

    return render(request, "blog/search.html", context)
