# ChatbotEcommerce

## baza produktów, zamówień i integracja z prostym modułem NLP do obsługi pytań klientów

1.Instalacja i uruchomienie
Sklonuj repozytorium (lub pobierz paczkę z plikami):


```bash
git clone https://github.com/TwojeKonto/chatbot_ecommerce.git 
cd chatbot_ecommerce
```


2.Zainstaluj wirtualne środowisko (opcjonalne, ale zalecane) i aktywuj je:

```
python -m venv venv
source venv/bin/activate  # macOS/Linux
```
lub:
```
venv\Scripts\activate     # Windows
```

3.Zainstaluj zależności:


```
pip install -r requirements.txt
```

4.Wykonaj migracje:


```
python manage.py migrate
```

5.Utwórz superużytkownika (admin):

```
python manage.py createsuperuser
```

6.Uruchom serwer deweloperski:

```
python manage.py runserver
```
Aplikacja powinna być dostępna pod adresem: http://127.0.0.1:8000/