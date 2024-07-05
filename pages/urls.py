from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('blogs/', views.blogs, name="blogs"),
    path('about/', views.about, name="about"),
    path('search/', views.search, name="search"),
    path('blog/<slug:slug>', views.post_page, name="post_page"),
    path('tag/<slug:slug>', views.tag_page, name="tag_page"),
    path('category/<slug:slug>', views.category_page, name="category_page"),
    path('author/<slug:slug>', views.author, name="author")
]
