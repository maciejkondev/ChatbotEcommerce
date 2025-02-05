import json
import spacy

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Product, Faq
from core.serializers import ProductSerializer


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

# Funkcja do klasyfikacji intencji na podstawie podobieństwa fraz
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
            response_text = "Przepraszam, nie rozumiem pytania. Jak mogę Ci pomóc?" # Domyślna odpowiedź
        return JsonResponse({'response': response_text})
    
    return JsonResponse({'error': 'Invalid request method.'}, status=400) # Błąd dla innych metod HTTP

@api_view(['GET']) # Dekorator dla widoku API
def top_products(request): # Widok API dla topowych produktów
    products = Product.objects.order_by('-stock')[:3] # Pobieramy 3 produkty z największą ilością na stanie
    serializer = ProductSerializer(products, many=True) # Serializujemy dane
    return Response(serializer.data) # Zwracamy dane w formacie JSON