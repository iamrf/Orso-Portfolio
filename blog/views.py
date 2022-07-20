from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class BlogListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'

class BlogDetailView(DetailView):
    context_object_name = 'post'    
    queryset = Post.objects.all()
    template_name = 'blog/detail.html'
    slug_field = 'slug'