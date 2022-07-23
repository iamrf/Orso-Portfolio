from django.shortcuts import render, redirect
from django.utils.translation import activate

# Language change toggle
def changeLang(request):
    activate(request.GET.get('lang'))
    return redirect(request.GET.get('next'))

# Home index view
def home(request):
    context = None
    return render(request, 'home/home.html', context)
