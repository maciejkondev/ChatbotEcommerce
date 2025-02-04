from django.urls import path
from .views import top_products, chatbot_request

urlpatterns = [
    path('top-products/', top_products, name="top-products"),
    path('chatbot/', chatbot_request, name="chatbot"),
]