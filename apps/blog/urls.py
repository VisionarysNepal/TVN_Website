from django.urls import path

from apps.blog.views import BlogDetailPageView, BlogPageView

from . import views

app_name = "blog"
urlpatterns = [
    path("", BlogPageView.as_view(), name="blogs"),
    path("blog/<slug:slug>/", BlogDetailPageView.as_view(), name="blog_detail_page"),
    path("tag/<slug:slug>/", views.TagDetailView.as_view(), name="tag_detail_page"),
    path(
        "category/<slug:slug>/",
        views.CategoryDetailView.as_view(),
        name="category_detail_page",
    ),
    path("author/<slug:slug>/", views.BlogAuthorView.as_view(), name="author"),
    path("search/", views.SearchView.as_view(), name="search"),
]
