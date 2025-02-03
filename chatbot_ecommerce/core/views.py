from django.shortcuts import render
from django.http import JsonResponse
from .models import Product  # Import the Product model


# Create your views here.
def hello(request):
    products = Product.objects.all()
    return render(request, 'core/hello.html', {'products': products})