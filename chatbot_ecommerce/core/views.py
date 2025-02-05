from django.shortcuts import render
from .models import Product  # Importujemy model Product z naszej aplikacji core
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Strona główna
def index(request):
    products = Product.objects.all()
    return render(request, 'core/index.html', {'products': products})

def cart(request):

    cart_items = request.session.get('cart', [])
    
    total = sum(item.get('price', 0) for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'core/cart.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after registration
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'core/profile.html')