from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.views.generic.edit import DeleteView
from blog.forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser
from .models import UserInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView)


def logout_required(function=None, logout_url=settings.LOGOUT_URL):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# Create your views here.
class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostListAPI(APIView):
    serializer_class = PostSerializer
    def post(self, request, format=None):
        data = request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class UserListAPI(APIView):
    serializer_class = UserSerializer
    def post(self, request, format=None):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        posts = UserInfo.objects.all()
        serializer = UserSerializer(posts, many=True)
        return Response(serializer.data)

class CommentListAPI(APIView):
    serializer_class = CommentSerializer
    def post(self, request, format=None):
        data = request.data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise status.Http404

    def get(self, request, slug, format=None):
        post = self.get_object(slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        post = self.get_object(slug)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        post = self.get_object(slug)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentDetail(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise status.Http404

    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePostView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return redirect('post_list')
        return super().post(request, *args, **kwargs)


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
class SearchPostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) & Q(published_date__lte=timezone.now())
            ).order_by('-published_date')
        return object_list

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user, published_date__isnull=True).order_by('create_date')


class UserListView(ListView):
    model = UserInfo
    template_name = 'user/user_list.html'

    def get_queryset(self):
        return UserInfo.objects.order_by('?')


class UserPostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(author__id=self.kwargs.get('pk'), published_date__lte=timezone.now()).order_by(
            '-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = Post.objects.filter(author__id=self.kwargs.get('pk')).count()
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'
    model = UserInfo
    template_name = 'user/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_post'] = Post.objects.filter(author__id=self.kwargs.get('pk')).count()
        context['posts'] = Post.objects.filter(author__id=self.kwargs.get('pk'))
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = UserForm
    model = UserInfo
    template_name = "user/user_form.html"

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if str(obj.username) != str(self.request.user):
            return redirect('post_list')
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


#######################################################################################################
#######################################################################################################

@login_required
def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect('post_detail', slug=slug)


@login_required
def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, "blog/post_detail.html", {"form": form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.slug
    comment.delete()
    return redirect('post_detail', post_pk)


@logout_required
def user_register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            login(request, user)
            return HttpResponseRedirect(reverse('post_list'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, "registration/registration.html", {'registered': registered, 'form': user_form})
