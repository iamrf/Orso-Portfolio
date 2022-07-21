from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Portfolio

class PortfolioListView(ListView):
    model = Portfolio
    context_object_name = 'portfolios'
    template_name = 'portfolio/index.html'

class PortfolioDetailView(DetailView):
    context_object_name = 'portfolio'
    queryset = Portfolio.objects.all()
    template_name = 'portfolio/detail.html'