from django.urls import path
from blog import views

urlpatterns = [
    path("posts/", views.PostAPIView.as_view(), name="post_views"),
    path("comments/", views.CommentAPIView.as_view(), name="comment_views"),
]
