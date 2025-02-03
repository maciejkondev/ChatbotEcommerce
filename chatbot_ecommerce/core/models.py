from django.db import models
from PIL import Image
import os

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Save the product normally first
        super().save(*args, **kwargs)

        if self.image:
            image_path = self.image.path
            img = Image.open(image_path)

            # Check image mode to handle transparency
            if img.mode in ("RGBA", "LA"):
                img = self._compress_transparent_image(img, image_path)
            else:
                img = self._compress_standard_image(img, image_path)

            img.save(image_path)

    def _compress_transparent_image(self, img, image_path):
        """
        Compress a transparent image while retaining transparency.
        """
        max_size = (800, 800)  # Resize if necessary
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save as PNG with compression
        img.save(image_path, format='PNG', optimize=True)
        return img

    def _compress_standard_image(self, img, image_path):
        """
        Compress a standard image (e.g., RGB) without transparency.
        """
        max_size = (800, 800)  # Resize if necessary
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save as JPEG with compression
        img.save(image_path, format='JPEG', quality=70, optimize=True)
        return img

    def __str__(self):
        return self.name
