from django import forms
from blog.models import Post, Comment
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    auto_id = True
    class Meta:
        model = Post
        fields = ("title", "text")

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)

        widget = {
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text=False)
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')