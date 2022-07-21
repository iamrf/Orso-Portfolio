from django.urls import path
from .views import PortfolioListView, PortfolioDetailView

app_name = "portfolio"
urlpatterns = [
    path('<slug>/', PortfolioDetailView.as_view(), name = 'detail'),
    path('', PortfolioListView.as_view(), name = 'index'),
]
