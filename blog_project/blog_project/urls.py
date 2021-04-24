"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as vs
from blog import views

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', include('blog.urls')),
    path(r'accounts/login/', vs.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path(r'accounts/logout/', vs.LogoutView.as_view(), name="logout", kwargs={'next_page':'/'}),
    path(r'accounts/register/', views.user_register, name="register"),
    path(r'user/<int:pk>/detail', views.UserDetailView.as_view(), name="user_detail"),
    path(r'user/<int:pk>/edit', views.UserUpdateView.as_view(), name="user_edit"),
    path(r'user/<int:pk>/posts', views.UserPostList.as_view(), name="user_posts"),
    path(r'users/', views.UserListView.as_view(), name="user_list"),
]
