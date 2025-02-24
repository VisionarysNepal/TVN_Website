from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, TemplateView

from apps.blog.forms import CommentForm
from apps.blog.models import Blog, Category, Comment, Tag


# Create your views here.
class BlogPageView(TemplateView):
    template_name = "blog/blogs.html"

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        blogs = (
            Blog.objects.all()
            .select_related("author", "category")
            .order_by("-view_count")
        )
        page_num = self.request.GET.get("q")
        paginator = Paginator(blogs, 6)
        page_obj = paginator.get_page(page_num)

        context = {"blogs": page_obj}
        return context


class BlogDetailPageView(DetailView):
    model = Blog
    template_name = "blog/blog_detail.html"

    def get_object(self, queryset=None):
        qs = (
            Blog.objects.select_related("author", "category")
            .prefetch_related(
                "comments",
                "comments__parent",
                "comments__replies",
                "author__user_socials__icon",
            )
            .annotate(total_comments=Count("comments", filter=Q(comments__parent=None)))
        )
        return get_object_or_404(qs, slug=self.kwargs["slug"])

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        blog = self.get_object()
        recent_blogs = Blog.objects.all().order_by("-last_updated")
        tags = Tag.objects.all()
        comment_form = CommentForm()
        categories = Category.objects.annotate(
            total_blogs=Count("blog_category", distinct=True)
        ).order_by("-total_blogs")

        if blog.view_count is None:
            blog.view_count = 1
        else:
            blog.view_count = blog.view_count + 1
        blog.save()

        query = self.request.GET.get("q")
        if query is not None and query != "":
            blogs = Blog.objects.filter(title__icontains=query)

        context = {
            "post": blog,
            "comment_form": comment_form,
            "recent_blogs": recent_blogs,
            "tags": tags,
            "categories": categories,
        }

        return context

    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        blog_post = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
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
                            "post": self.get_object(),
                            "comment_form": CommentForm(),
                        },
                    )
            else:
                comment = comment_form.save(commit=False)
                comment.post = blog_post
                comment.save()
                return render(
                    request,
                    "blog/includes/comments.html",
                    {
                        "post": self.get_object(),
                        "comment_form": CommentForm(),
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


class BlogAuthorView(DetailView):
    template_name = "blog/author.html"
    model = User

    def get_object(self, queryset=None):
        qs = User.objects.select_related("profile").prefetch_related(
            "blog_author", "blog_author__category"
        )
        return get_object_or_404(qs, profile__slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        top_authors = (
            User.objects.select_related("profile")
            .annotate(total_blogs=Count("blog_author"))
            .order_by("-total_blogs")
        )
        top_blogs = author.blog_author.prefetch_related("category").order_by(
            "-view_count"
        )[0:3]
        recent_blogs = author.blog_author.prefetch_related("category").order_by(
            "-last_updated"
        )[0:3]
        context.update(
            {
                "author": author,
                "top_authors": top_authors,
                "top_blogs": top_blogs,
                "recent_blogs": recent_blogs,
            }
        )
        return context


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
