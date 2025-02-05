from django.contrib import admin
from .models import Product, Order, OrderItem, Customer, Faq # Importujemy nasze modele
# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(Faq) # Głównie do wykorzystania przez Chatbota, ewentualnie dynamiczna strona FAQ do edycji dla administratora