from django import forms
from .models import Blog
from .models import Comment
from .models import Contact

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'writer', 'body', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['writer', 'body']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
