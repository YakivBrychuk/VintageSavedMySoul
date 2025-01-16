from django.contrib.auth.models import User
import os
import subprocess
from django.core.exceptions import ValidationError
from django.db import models
from pillow_avif import AvifImagePlugin
from PIL import Image


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
    short_description = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(default=False, null=True, blank=True)
    has_sizes = models.BooleanField(default=False, null=True, blank=True) 
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/', validators=[validate_image_extension])
    
    condition = models.CharField(max_length=254, blank=True, null=True)
    tag_size = models.CharField(max_length=100, blank=True, null=True)
    fabric_info = models.CharField(max_length=254, blank=True, null=True)
    estimated_fit = models.CharField(max_length=254, blank=True, null=True)
    
    # Measurements (in cm)
    shoulders = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sleeve = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    armpit_to_armpit = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    hips = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Stock
    stock = models.PositiveIntegerField(default=0)

    # Many-to-Many relationship with User model for favoriting products
    favorited_by = models.ManyToManyField(
        User, related_name='favorite_products', blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Save the model first to ensure the image is available
        super().save(*args, **kwargs)
