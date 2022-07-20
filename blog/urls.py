from django.urls import path
from .views import BlogDetailView, BlogListView

app_name = "blog"
urlpatterns = [
    path('<slug>/', BlogDetailView.as_view(), name = 'detail'),
    path('', BlogListView.as_view(), name = 'index'),
]
