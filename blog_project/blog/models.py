from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserInfo(AbstractUser):
    username = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    slug = models.SlugField(default=slugify(username))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.username
class Post(models.Model):
    author = models.ForeignKey('blog.UserInfo', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(allow_unicode=True, unique=True, default=slugify(title))

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name="comments", on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
