from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.utils import timezone
from .models import Comment
from .models import Contact
from .forms import BlogForm
from .forms import CommentForm
from .forms import ContactForm
from django.contrib import messages
from django import forms
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    blogs = Blog.objects.all()
    return render(request, 'home.html', {'blogs':blogs})


def delete(request, id):
    delete_blog = Blog.objects.get(id=id)
    delete_blog.delete()
    return redirect('home')


def new(request):
    if request.method == 'POST':
        blog_form = BlogForm(request.POST, request.FILES)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.pub_date = timezone.now()
            blog.save()
            return redirect('home')
    else:
        blog_form = BlogForm()
        return render(request, 'new.html', {'blog_form':blog_form})

def edit(request, id):
    blog = get_object_or_404(Blog, pk=id)
    if request.method == 'GET':
        blog_form = BlogForm(instance=blog)
        return render(request, 'edit.html', {'edit_blog':blog_form})
    else:
        blog_form = BlogForm(request.POST, request.FILES, instance=blog)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.pub_date = timezone.now()
            blog.save()
        return redirect('/blog/' + str(id))

def detail(request, id):
    blog = get_object_or_404(Blog, pk=id)
    comments = Comment.objects.filter(blog_id=id, comment_id__isnull=True)

    re_comments = []
    for comment in comments:
        re_comments += list(Comment.onjects.filter(comment_id=comment.id))

    form = CommentForm()
    return render(request, 'detail.html', {'blog':blog, 'comments':comments, 're_comments':re_comments, 'form':form})

def create_comment(request, blog_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_id = Blog.objects.get(pk=blog_id)
            comment.save()
    return redirect('/detail/' + str(blog_id))

def create_re_comment(request, blog_id, comment_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_id = Blog.objects.get(pk=comment_id)
            comment.comment_id = Comment.objects.get(pk=comment_id)
            comment.save()
    return redirect('/detail/' + str(blog_id))

def email(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST, request.FILES)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.save()
            subject = contact.name
            message = contact.message
            email = contact.email
            mail = EmailMessage(subject, message, to=[email])
            mail.send()
            return redirect('home')
    else:
        contact_form = ContactForm()
        return render(request, 'email.html', {'contact_form':contact_form})