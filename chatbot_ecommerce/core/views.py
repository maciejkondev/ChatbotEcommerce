from django.shortcuts import render
from .models import Product  # Importujemy model Product z naszej aplikacji core


# Strona główna
def index(request):
    products = Product.objects.all()
    return render(request, 'core/index.html', {'products': products})