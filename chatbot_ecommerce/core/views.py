from decimal import Decimal
from .models import Product, Order, OrderItem, Customer  # Importujemy model Product z naszej aplikacji core
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Strona główna
def index(request):
    products = Product.objects.all()
    return render(request, 'core/index.html', {'products': products})

# Koszyk
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')
    for prod_id, quantity in cart.items():
        product = get_object_or_404(Product, id=prod_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'core/cart.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Zaloguj użytkownika po rejestracji
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def profile(request):
    # Pobierz lub utwórz profil klienta
    customer, created = Customer.objects.get_or_create(user=request.user)
    # Pobierz historię zamówień dla klienta, sortując od najnowszych
    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'core/profile.html', context)

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_key = str(product_id)
    if product_key in cart:
        cart[product_key] += 1
    else:
        cart[product_key] = 1
    request.session['cart'] = cart
    return redirect('cart')

def update_cart(request):
    if request.method == 'POST':
        new_cart = {}
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                prod_id = key.split('_')[1]
                try:
                    quantity = int(value)
                    if quantity > 0:
                        new_cart[prod_id] = quantity
                except ValueError:
                    pass
        request.session['cart'] = new_cart
    return redirect('cart')

def checkout(request):
    if not request.user.is_authenticated:
        return render(request, 'core/error.html', {'message': 'Musisz być zalogowany, aby dokonać zakupu.'})
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')
    customer, _ = Customer.objects.get_or_create(user=request.user)
    cart_items = []
    total = Decimal('0.00')
    for prod_id, quantity in cart.items():
        product = get_object_or_404(Product, id=prod_id)
        if product.stock < quantity:
            return render(request, 'core/error.html', {
                'message': f'Nie ma wystarczającej ilości produktu {product.name}. Dostępna ilość: {product.stock}'
            })
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
    if request.method == 'POST':
        order = Order.objects.create(
            customer=customer,
            total_value=total,
            status=Order.OrderStatus.PENDING
        )
        for item in cart_items:
            product = item['product']
            quantity = item['quantity']
            subtotal = item['subtotal']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                item_price=subtotal
            )
            product.stock -= quantity
            product.save()
        request.session['cart'] = {}
        return redirect('profile')
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'core/checkout.html', context)
