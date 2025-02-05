import json
import spacy
import re

from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.serializers import ProductSerializer, OrderSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from core.models import Product, Order, Customer, Faq

# Ładujemy model języka polskiego z biblioteki spaCy
nlp = spacy.load('pl_core_news_lg')

# Przykładowe frazy dla każdej intencji
intent_examples = {
    "PRODUCT": [
        "Jakie macie produkty?",
        "Pokaż mi dostępne produkty.",
        "Szukam produktów.",
        "Co macie w ofercie?",
        "Przegląd oferty produktów.",
        "Czy macie świeże owoce?",
        "Chciałbym zobaczyć katalog produktów.",
        "Jaka jest lista dostępnych produktów?",
        "Co jest obecnie w sprzedaży?",
        "Interesują mnie Wasze produkty.",
        "Czy mogę zobaczyć ofertę produktów?",
    ],
    "FAQ": [
        "Mam pytanie dotyczące FAQ.",
        "Gdzie znajdę informacje?",
        "FAQ",
        "Pytanie",
        "Ekologiczne",
        "Certyfikat",
        "Chciałbym poznać warunki współpracy.",
        "Szukam odpowiedzi na pytania.",
        "Jak działają Wasze usługi?",
        "Czy macie jakieś FAQ?",
        "Gdzie mogę znaleźć szczegółowe informacje?",
        "Potrzebuję pomocy, proszę o FAQ.",
    ],
    "DELIVERY": [
        "Ile kosztuje dostawa?",
        "Jaki jest koszt wysyłki?",
        "Dostawa",
        "Wysyłka",
        "Czy wysyłacie zamówienia za darmo?",
        "Jaki jest czas dostawy?",
        "Jakie są opcje dostawy?",
        "Czy oferujecie ekspresową dostawę?",
        "Jakie są koszty przesyłki?",
        "Czy mogę śledzić przesyłkę?",
        "Kiedy otrzymam zamówienie?",
    ],
}

# Funkcja do klasyfikacji intencji z progiem trafności
def classify_intent(user_message):
    doc = nlp(user_message)
    best_intent = "DEFAULT"
    best_score = 0.0

    # Przechodzimy przez wszystkie intencje oraz ich przykładowe frazy
    for intent, examples in intent_examples.items():
        for example in examples:
            example_doc = nlp(example)
            score = doc.similarity(example_doc)
            if score > best_score:
                best_score = score
                best_intent = intent

    # Jeśli trafność jest zbyt niska, ustawiamy intencję na domyślną
    if best_score < 0.5:
        best_intent = "DEFAULT"

    return best_intent

# Widok API do obsługi zapytań chatbota
def chatbot_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        # Klasyfikujemy intencję na podstawie uniwersalnego podejścia
        intent = classify_intent(user_message)
        
        response_text = "Cześć! Jak mogę Ci pomóc?"
        
        if intent == "PRODUCT":
            # Próba wyłapania konkretnego zapytania o produkt, np. "czy macie poziomki"
            product_search = re.search(r'czy\s+macie\s+(.+)', user_message, flags=re.IGNORECASE)
            if product_search:
                # Pobieramy wyszukiwany termin i usuwamy ewentualne białe znaki
                product_query = product_search.group(1).strip()
                # Wyszukujemy produkty, których nazwa zawiera podaną frazę (niezależnie od wielkości liter)
                products = Product.objects.filter(name__icontains=product_query)
                if products.exists():
                    product_names = ", ".join([p.name for p in products])
                    response_text = f"Mamy następujące produkty: {product_names}."
                else:
                    response_text = f"Przykro nam, nie znaleziono produktów zawierających '{product_query}'."
            else:
                # Jeśli nie udało się wyłapać konkretnego zapytania, zwracamy przykładową listę produktów
                products = Product.objects.all()[:3]
                product_names = ", ".join([p.name for p in products])
                response_text = f"Mamy następujące produkty: {product_names}."
        
        elif intent == "FAQ":
            faqs = Faq.objects.all()[:3]
            faq_texts = " | ".join([f"{faq.question}: {faq.answer}" for faq in faqs])
            response_text = f"Oto kilka FAQ: {faq_texts}."
        
        elif intent == "DELIVERY":
            faq_delivery = Faq.objects.filter(question__icontains="dostawa").first()
            if faq_delivery:
                response_text = f"Informacje o dostawie: {faq_delivery.answer}"
            else:
                response_text = "Przepraszamy, nie znaleziono informacji o dostawie."
        
        else:
            response_text = "Przepraszam, nie rozumiem pytania. Proszę sprecyzować zapytanie." # Domyślna odpowiedź
    
        return JsonResponse({'response': response_text})
    
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@api_view(['GET']) # Dekorator dla widoku API
@permission_classes([AllowAny]) # Pozwalamy na dostęp dla wszystkich
def top_products(request): # Widok API dla topowych produktów
    products = Product.objects.order_by('-stock')[:3] # Pobieramy 3 produkty z największą ilością na stanie
    serializer = ProductSerializer(products, many=True) # Serializujemy dane
    return Response(serializer.data) # Zwracamy dane w formacie JSON

@permission_classes([AllowAny])
class ProductViewSet(viewsets.ModelViewSet): # Widok zbioru dla produktów
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Przykład: GET /api/products/by-letter/?letter=A
    @action(detail=False, methods=['get'], url_path='by-letter')
    def by_letter(self, request):
        letter = request.query_params.get('letter', '').upper()
        if not letter:
            return Response({"detail": "Podaj parametr 'letter'."}, status=status.HTTP_400_BAD_REQUEST)
        qs = self.get_queryset().filter(name__istartswith=letter)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet): # Widok zbioru dla zamówień
    queryset = Order.objects.all()

    serializer_class = OrderSerializer

    @action(detail=False, methods=['get'], url_path='monthly-summary', # Dodajemy akcję dla podsumowania miesięcznego
            permission_classes=[permissions.IsAdminUser]) # Tylko dla administratora
    def monthly_summary(self, request):
        summary = ( # Pobieramy podsumowanie dla każdego miesiąca
            Order.objects
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total_orders=Count('id'), total_value=Sum('total_value'))
            .order_by('month')
        )
        return Response(summary)

@api_view(['POST'])
@permission_classes([])  # Pozwalamy anonimowym użytkownikom na rejestrację
def register(request): # Widok rejestracji użytkownika
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    if not username or not password:
        return Response({"detail": "Username oraz password są wymagane."},
                        status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({"detail": "Użytkownik o takim username już istnieje."},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        validate_password(password)
    except ValidationError as e:
        return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password, email=email)
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_201_CREATED)