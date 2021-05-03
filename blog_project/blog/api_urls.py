from django.urls import path
from blog import views

urlpatterns = [
    path("users/", views.UserListAPI.as_view(), name="user_views"),
    path("posts/", views.PostListAPI.as_view(), name="post_views"),
    path("posts/<slug:slug>", views.PostDetail.as_view(), name="post_detail"),
    path("comments/", views.CommentListAPI.as_view(), name="comment_views"),
    path("comments/<int:pk>", views.CommentDetail.as_view(), name="comment_detail"),
]
