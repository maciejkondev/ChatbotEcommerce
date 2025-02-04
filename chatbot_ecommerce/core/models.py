import uuid
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Zamiast niestandardowego modelu użytkownika, odwołujemy się tutaj do wbudowanego modelu User
class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile",
        verbose_name="Użytkownik"
    )

    def __str__(self):
        return self.user.username # Zwracamy nazwę użytkownika jako reprezentację obiektu

# Model produktu z kompresją obrazów
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Nazwa produktu", max_length=100)
    description = models.TextField("Opis produktu")
    price = models.DecimalField("Cena", max_digits=10, decimal_places=2)
    stock = models.IntegerField("Stan magazynowy", default=0)
    image = models.ImageField("Obraz produktu", upload_to='product_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Zapisujemy produkt standardowo
        super().save(*args, **kwargs)

        # Jeśli został dodany obraz, dokonujemy jego kompresji
        if self.image:
            image_path = self.image.path
            img = Image.open(image_path)

            if img.mode in ("RGBA", "LA"):
                img = self._compress_transparent_image(img, image_path)
            else:
                img = self._compress_standard_image(img, image_path)
            # Nadpisujemy obraz skompresowaną wersją
            img.save(image_path)

    # Metoda do kompresji obrazu z kanałem alfa (np. PNG)
    def _compress_transparent_image(self, img, image_path):
        max_size = (800, 800)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(image_path, format='PNG', optimize=True)
        return img

    # Metoda do kompresji standardowego obrazu (np. JPEG)
    def _compress_standard_image(self, img, image_path):
        """
        Kompresja standardowego obrazu (np. JPEG) bez kanału alfa.
        """
        max_size = (800, 800)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(image_path, format='JPEG', quality=70, optimize=True)
        return img

    def __str__(self):
        return self.name

# Model kategorii produktów
class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Oczekujące'
        PROCESSING = 'processing', 'W trakcie realizacji'
        COMPLETED = 'completed', 'Zrealizowane'
        CANCELLED = 'cancelled', 'Anulowane'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Zamiast niestandardowego użytkownika, odwołujemy się teraz do klienta
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Klient"
    )
    created_at = models.DateTimeField("Data utworzenia", auto_now_add=True)
    status = models.CharField(
        "Status zamówienia",
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    total_value = models.DecimalField("Łączna wartość", max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Zamówienie {self.id} - {self.customer.user.username}"

# Model pozycji zamówienia
class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Zamówienie"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name="Produkt"
    )
    quantity = models.PositiveIntegerField("Ilość")
    item_price = models.DecimalField("Cena pozycji", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# Model FAQ (często zadawane pytania)
class Faq(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField("Pytanie", max_length=255)
    answer = models.TextField("Odpowiedź")

    def __str__(self):
        return self.question
