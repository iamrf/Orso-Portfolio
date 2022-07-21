from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Landing

class LandingListView(ListView):
    model = Landing
    context_object_name = 'landings'
    template_name = 'landing/index.html'

class LandingDetailView(DetailView):
    context_object_name = 'landing'    
    queryset = Landing.objects.all()
    template_name = 'landing/detail.html'