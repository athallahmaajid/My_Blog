from django.urls import path, include
from blog import views

urlpatterns = [
    path(r"", views.PostListView.as_view(), name="post_list"),
    path(r"api/", include("blog.api_urls")),
    path("search/", views.SearchPostList.as_view(), name="search_post"),
    path(r"about/", views.AboutView.as_view(), name="about"),
    path(r"post/<slug:slug>", views.PostDetailView.as_view(), name="post_detail"),
    path(r"post/new/", views.CreatePostView.as_view(), name="post_create"),
    path(r"post/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path(r"post/<slug:slug>/remove/", views.PostDeleteView.as_view(), name="post_remove"),
    path(r"drafts/", views.DraftListView.as_view(), name="post_draft_list"),
    path(r"post/<slug:slug>/comment/", views.add_comment_to_post, name="add_comment_to_post"),
    path(r"post/<slug:slug>/publish/", views.post_publish, name="post_publish"),
    path(r"comment/<int:pk>/remove", views.comment_remove, name="comment_remove"),
]
