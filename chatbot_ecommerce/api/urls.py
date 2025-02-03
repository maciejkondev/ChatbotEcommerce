from django.urls import path
from .views import top_products

urlpatterns = [
    path('top-products/', top_products, name="top-products"),
]