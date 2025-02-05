from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('add-to-cart/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path(
        'logout/', 
        auth_views.LogoutView.as_view(
            template_name='core/register.html',  # Użyj szablonu register.html
            http_method_names=['get', 'post'],  # Akceptuj GET oraz POST
            next_page='/core/index/'  # Po wylogowaniu przekierowanie na stronę główną
        ),
        name='logout'
    ),
]