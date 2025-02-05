# chatbot_ecommerce/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import top_products, chatbot_request, ProductViewSet, OrderViewSet, register
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('top-products/', top_products, name="top-products"), # Dodaj widok top_products
    path('chatbot/', chatbot_request, name="chatbot"), # Dodaj widok chatbot_request
    path('register/', register, name='api-register'), # Dodaj widok register
    path('login/', obtain_auth_token, name='api-login'), # Dodaj widok obtain_auth_token
    path('', include(router.urls)), # Dodaj adresy z routera
]
