# chatbot_ecommerce/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import top_products, chatbot_request, ProductViewSet, OrderViewSet, register
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
# Jeśli chcesz dodać kolejne zestawy (np. dla Customer) – podobnie

urlpatterns = [
    # Istniejące endpointy dla chatbota:
    path('top-products/', top_products, name="top-products"),
    path('chatbot/', chatbot_request, name="chatbot"),
    # Nowe endpointy rejestracji i logowania (token):
    path('register/', register, name='api-register'),
    path('login/', obtain_auth_token, name='api-login'),
    # Endpointy CRUD i dodatkowe z routera:
    path('', include(router.urls)),
]
