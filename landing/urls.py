from django.urls import path
from .views import LandingDetailView, LandingListView

app_name = "landing"
urlpatterns = [
    path('<slug>/', LandingDetailView.as_view(), name = 'detail'),
    path('', LandingListView.as_view(), name = 'index'),
]
