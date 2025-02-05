"""
URL configuration for chatbot_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Import panelu administracyjnego
from django.urls import path, include  # Import funkcji obsługujących URL-e
from django.conf import settings  # Import ustawień
from django.conf.urls.static import static  # Import funkcji obsługujących pliki multimedialne
from django.shortcuts import redirect  # Import funkcji przekierowującej
from django.contrib.auth import views as auth_views  # Import widoków uwierzytelniania

def redirect_to_index(request, unused_path=None): #Copilot twierdzi, że jest nieużywany, ale bez tego nie działa całkowite przekierowanie
    # Przekierowanie na stronę główną (np. /core/index/)
    return redirect('/core/index/')

urlpatterns = [
    path('admin/', admin.site.urls),  # Panel administracyjny
    path('core/', include('core.urls')),  # Aplikacja core
    path('api/', include('api.urls')),  # Aplikacja api
    # Dodanie ścieżek logowania i wylogowywania
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            http_method_names=['get', 'post'],  # Akceptuj GET oraz POST
            next_page='/core/index/'  # Po wylogowaniu przekierowanie na stronę główną
        ),
        name='logout'
    ),
    path('', redirect_to_index, name='home'),  # Strona główna
    path('<path:unused_path>/', redirect_to_index)  # Przekierowanie nieznanych adresów na stronę główną
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Obsługa plików multimedialnych
