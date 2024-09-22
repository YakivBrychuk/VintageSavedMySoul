import os
import subprocess
from django.core.exceptions import ValidationError
from django.db import models
from pillow_avif import AvifImagePlugin
from PIL import Image


# Create your models here.

class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


def validate_image_extension(value):
    ext = value.name.split('.')[-1].lower()
    valid_extensions = ['jpg', 'jpeg', 'png', 'avif', 'webp']
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}. Supported formats: jpg, jpeg, png, avif, webp.')


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/', validators=[validate_image_extension])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Convert WebP to PNG before converting to AVIF
        if self.image.path.endswith('.webp'):
            with Image.open(self.image.path) as img:
                png_image_path = self.image.path.rsplit('.', 1)[0] + '.png'
                img.save(png_image_path, 'PNG')

            # Replace the path of the image with the PNG version
            self.image.name = f'images/{os.path.basename(png_image_path)}'
            self.save()

        # Convert JPEG/PNG/WebP (after conversion to PNG) to AVIF
        if self.image.path.endswith(('.jpg', '.jpeg', '.png')):
            avif_image_path = self.image.path.rsplit('.', 1)[0] + '.avif'

            try:
                # Run the AVIF conversion
                subprocess.run(['avifenc', self.image.path, avif_image_path], check=True)

                # Remove the original image file after conversion
                if os.path.exists(self.image.path):
                    os.remove(self.image.path)

                # Update the image field to point to the AVIF file
                self.image.name = f'images/{os.path.basename(avif_image_path)}'
                self.save()

            except subprocess.CalledProcessError as e:
                print(f"Error converting to AVIF: {e}")

    # Dynamic URL access for images
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None
