import os
import subprocess
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


def validate_image_extension(value):
    ext = value.name.split('.')[-1].lower()
    valid_extensions = ['jpg', 'jpeg', 'png', 'avif']
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}. Supported formats: jpg, jpeg, png, avif.')


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/', validators=[validate_image_extension])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Convert JPEG/PNG to AVIF after saving the image
        if self.image.path.endswith(('.jpg', '.jpeg', '.png')):
            avif_image_path = self.image.path.replace('.jpg', '.avif').replace('.jpeg', '.avif').replace('.png', '.avif')

            try:
                subprocess.run(['avifenc', self.image.path, avif_image_path], check=True)
                # Update the image path to the new AVIF file
                self.image.name = os.path.basename(avif_image_path)
                self.save()  # Save the model with the updated image path

            except subprocess.CalledProcessError as e:
                print(f"Error converting to AVIF: {e}")
